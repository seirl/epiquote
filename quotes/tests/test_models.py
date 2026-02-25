from django.test import TestCase
from django.contrib.auth import get_user_model
from quotes.models import Quote, QuoteVote

User = get_user_model()


class QuoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.staff_user = User.objects.create_user(
            username='staffuser', password='password', is_staff=True
        )
        self.quote = Quote.objects.create(
            author='Test Author',
            context='Test Context',
            content='Test Content',
            user=self.user,
            visible=True,
            accepted=True,
        )

    def test_quote_creation(self):
        self.assertEqual(self.quote.author, 'Test Author')
        self.assertEqual(self.quote.content, 'Test Content')
        self.assertEqual(self.quote.user, self.user)
        self.assertTrue(self.quote.visible)
        self.assertTrue(self.quote.accepted)

    def test_quote_absolute_url(self):
        self.assertEqual(self.quote.get_absolute_url(), f'/{self.quote.id}')

    def test_quote_manager_seen_by(self):
        # Create different types of quotes
        visible_accepted = self.quote

        visible_not_accepted = Quote.objects.create(
            author='A', content='C', visible=True, accepted=False
        )
        not_visible_accepted = Quote.objects.create(
            author='A', content='C', visible=False, accepted=True
        )
        not_visible_not_accepted = Quote.objects.create(
            author='A', content='C', visible=False, accepted=False
        )

        # Anonymous user (None) - should see only visible and accepted
        quotes = Quote.objects.seen_by(None)
        self.assertIn(visible_accepted, quotes)
        self.assertNotIn(visible_not_accepted, quotes)
        self.assertNotIn(not_visible_accepted, quotes)
        self.assertNotIn(not_visible_not_accepted, quotes)

        # Normal user - same as anonymous
        quotes = Quote.objects.seen_by(self.user)
        self.assertIn(visible_accepted, quotes)
        self.assertNotIn(visible_not_accepted, quotes)
        self.assertNotIn(not_visible_accepted, quotes)
        self.assertNotIn(not_visible_not_accepted, quotes)

        # Staff user - should see accepted quotes regardless of visibility
        quotes = Quote.objects.seen_by(self.staff_user)
        self.assertIn(visible_accepted, quotes)
        self.assertNotIn(visible_not_accepted, quotes)
        self.assertIn(not_visible_accepted, quotes)
        self.assertNotIn(not_visible_not_accepted, quotes)

    def test_quote_annotations(self):
        # Create votes
        QuoteVote.objects.create(user=self.user, quote=self.quote, vote=1)
        QuoteVote.objects.create(
            user=self.staff_user, quote=self.quote, vote=1
        )

        # Get quote from manager to trigger annotation
        quote = Quote.objects.get(id=self.quote.id)
        self.assertEqual(quote.num_votes, 2)
        self.assertEqual(quote.score, 2)

        # Test with negative vote
        QuoteVote.objects.create(
            user=User.objects.create_user('u3', 'p'),
            quote=self.quote,
            vote=-1,
        )
        quote = Quote.objects.get(id=self.quote.id)
        self.assertEqual(quote.num_votes, 3)
        self.assertEqual(quote.score, 1)

    def test_vote_creation(self):
        vote = QuoteVote.objects.create(
            user=self.user, quote=self.quote, vote=1
        )
        self.assertEqual(str(vote), f'{self.user}: 1 on {self.quote}')

    def test_vote_unique_constraint(self):
        QuoteVote.objects.create(user=self.user, quote=self.quote, vote=1)
        with self.assertRaises(Exception):  # IntegrityError
            QuoteVote.objects.create(user=self.user, quote=self.quote, vote=-1)
