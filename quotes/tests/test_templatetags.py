from django.template import Context, Template
from django.test import RequestFactory, TestCase
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


class NavigationTemplateTagTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def render_template(self, pattern_or_urlname, path):
        request = self.factory.get(path)
        context = Context({'request': request})
        template = Template(
            "{% load navigation %}"
            f"{{% active '{pattern_or_urlname}' %}}"
        )
        return template.render(context)

    def test_active_with_urlname_match(self):
        # 'last_quotes' resolves to '/last'
        result = self.render_template('last_quotes', '/last')
        self.assertEqual(result, 'active rounded bg-opacity-10 bg-secondary')

    def test_active_with_urlname_no_match(self):
        # 'last_quotes' resolves to '/last', path is '/top'
        result = self.render_template('last_quotes', '/top')
        self.assertEqual(result, '')

    def test_active_with_pattern_match(self):
        # pattern '^/test' matches path '/test/abc'
        result = self.render_template('^/test', '/test/abc')
        self.assertEqual(result, 'active rounded bg-opacity-10 bg-secondary')

    def test_active_with_pattern_no_match(self):
        # pattern '^/test' does not match path '/other/test'
        result = self.render_template('^/test', '/other/test')
        self.assertEqual(result, '')
