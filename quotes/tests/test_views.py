from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from quotes.models import Quote, QuoteVote

User = get_user_model()


class QuoteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.url_home = reverse('home_quotes')
        self.url_last = reverse('last_quotes')
        self.url_top = reverse('top_quotes')
        self.url_flop = reverse('flop_quotes')
        self.url_random = reverse('random_quotes')
        self.url_add = reverse('add_quote')
        self.url_search = reverse('search_quotes')

    def test_home_view(self):
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response, self.quote.content)

    def test_last_quotes_view(self):
        response = self.client.get(self.url_last)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'last.html')
        self.assertContains(response, self.quote.content)

    def test_top_quotes_view(self):
        response = self.client.get(self.url_top)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'top.html')
        self.assertContains(response, self.quote.content)

    def test_flop_quotes_view(self):
        response = self.client.get(self.url_flop)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flop.html')
        self.assertContains(response, self.quote.content)

    def test_random_quotes_view(self):
        response = self.client.get(self.url_random)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'random.html')
        self.assertContains(response, self.quote.content)

    def test_detail_view(self):
        url = reverse('show_quote', args=[self.quote.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quote.html')
        self.assertContains(response, self.quote.content)

    def test_favourite_quotes_view(self):
        self.quote.fans.add(self.user)
        url = reverse('favorite_quotes', args=[self.user.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'favourites.html')
        self.assertContains(response, self.quote.content)

    def test_add_quote_view_requires_login(self):
        response = self.client.get(self.url_add)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_add_quote_view_post(self):
        self.client.force_login(self.user)
        data = {
            'author': 'New Author',
            'context': 'New Context',
            'content': 'New Content',
        }
        response = self.client.post(self.url_add, data)
        # Should redirect after success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Quote.objects.filter(author='New Author').exists())

        # Verify user is assigned
        new_quote = Quote.objects.get(author='New Author')
        self.assertEqual(new_quote.user, self.user)

    def test_search_view(self):
        response = self.client.get(self.url_search, {'q': 'Test Content'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.quote.content)

        response = self.client.get(self.url_search, {'q': 'Nonexistent'})
        self.assertNotContains(response, self.quote.content)

    def test_ajax_vote(self):
        self.client.force_login(self.user)
        url = reverse(
            'ajax_vote_quote',
            kwargs={'quote_id': self.quote.id, 'direction': 'up'},
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['current_vote'], 1)

        # Check vote created
        self.assertTrue(
            QuoteVote.objects.filter(
                user=self.user, quote=self.quote, vote=1
            ).exists()
        )

        # Toggle vote (click up again -> remove vote)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['current_vote'], 0)
        self.assertFalse(
             QuoteVote.objects.filter(
                user=self.user, quote=self.quote
            ).exists()
        )

        # Down vote
        url_down = reverse(
            'ajax_vote_quote',
            kwargs={'quote_id': self.quote.id, 'direction': 'down'},
        )
        response = self.client.post(url_down)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['current_vote'], -1)
        self.assertTrue(
             QuoteVote.objects.filter(
                user=self.user, quote=self.quote, vote=-1
            ).exists()
        )

    def test_ajax_favourite(self):
        self.client.force_login(self.user)
        url = reverse(
            'ajax_favorite_quote', kwargs={'quote_id': self.quote.id}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

        # Check added to fans
        self.assertTrue(self.quote.fans.filter(id=self.user.id).exists())

        # Toggle off
        response = self.client.post(url)
        self.assertFalse(self.quote.fans.filter(id=self.user.id).exists())

    def test_rss_feed(self):
        url = reverse('feed_quotes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check for RSS content type or content
        self.assertIn('application/rss+xml', response['Content-Type'])
        self.assertContains(response, self.quote.content)
