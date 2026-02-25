from django.test import TestCase
from quotes.forms import SearchForm, AddQuoteForm


class SearchFormTest(TestCase):
    def test_valid_search(self):
        form = SearchForm(data={'q': 'valid query'})
        self.assertTrue(form.is_valid())

    def test_too_many_words(self):
        q = ' '.join(['word'] * 31)
        form = SearchForm(data={'q': q})
        self.assertFalse(form.is_valid())
        self.assertIn('Trop de mots.', form.errors['q'])

    def test_too_many_letters(self):
        q = 'a' * 301
        form = SearchForm(data={'q': q})
        self.assertFalse(form.is_valid())
        self.assertIn('Trop de lettres.', form.errors['q'])


class AddQuoteFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'author': 'Author',
            'context': 'Context',
            'content': 'Content',
        }
        form = AddQuoteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        form = AddQuoteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('author', form.errors)
        self.assertIn('content', form.errors)
        # context is not required in model (blank=True) but widget is TextInput
        # Let's check if context is required in form. Model says blank=True.
        # So it should not be required.

    def test_context_not_required(self):
        data = {
            'author': 'Author',
            'content': 'Content',
        }
        form = AddQuoteForm(data=data)
        self.assertTrue(form.is_valid())
