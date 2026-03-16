from django.test import TestCase
from django.urls import reverse


class ActivationFailedTest(TestCase):
    def test_activation_failed_template(self):
        url = reverse('django_registration_activate') + '?activation_key=invalid-key'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'django_registration/activation_form.html'
        )
