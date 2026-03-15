from django.test import TestCase
from django.urls import reverse


class ActivationFailedTest(TestCase):
    def test_activation_failed_template(self):
        # The activation URL takes an activation key. We will just pass an invalid one.
        # Note: django_registration uses signing, so an invalid string should fail.
        # Wait, the URL format depends on django_registration backend (HMAC).
        url = reverse(
            'django_registration_activate',
            kwargs={'activation_key': 'invalid-key'},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'django_registration/activation_failed.html'
        )
