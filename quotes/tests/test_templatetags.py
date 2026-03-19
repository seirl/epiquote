from django.test import TestCase
from django.contrib.auth import get_user_model
from quotes.models import Quote, QuoteVote
from quotes.templatetags.vote import vote_for

User = get_user_model()

class VoteTemplateTagTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password'
        )
        self.quote = Quote.objects.create(
            author='Test Author',
            context='Test Context',
            content='Test Content',
            user=self.user,
            visible=True,
            accepted=True,
        )

    def test_vote_for_with_existing_vote(self):
        QuoteVote.objects.create(user=self.user, quote=self.quote, vote=1)
        # Mock context is just an empty dict for this tag since it doesn't use it
        context = {}
        result = vote_for(context, self.user, self.quote)
        self.assertEqual(result, 1)

    def test_vote_for_with_negative_vote(self):
        QuoteVote.objects.create(user=self.user, quote=self.quote, vote=-1)
        context = {}
        result = vote_for(context, self.user, self.quote)
        self.assertEqual(result, -1)

    def test_vote_for_with_no_vote(self):
        context = {}
        result = vote_for(context, self.user, self.quote)
        self.assertIsNone(result)
