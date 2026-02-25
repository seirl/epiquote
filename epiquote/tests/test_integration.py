import re

from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

User = get_user_model()


class IntegrationTests(TestCase):
    def test_email_registration(self):
        """
        Task 1: Email Registration Test
        """
        register_url = reverse('register')
        username = 'newuser'
        password = 'password123'

        form_data = {
            'username': username,
            'password1': password,
            'password2': password,
        }

        response = self.client.post(register_url, form_data)
        self.assertEqual(response.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        match = re.search(r'(http://[^\s]+/activate/[a-zA-Z0-9:\-_]+)', email.body)
        self.assertTrue(match, f"Activation link not found in email body: {email.body}")
        activation_link = match.group(1)

        # Follow redirect to final success page
        response = self.client.get(activation_link, follow=True)
        self.assertEqual(response.status_code, 200)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.fail(f"User {username} not found in database")

        self.assertTrue(user.is_active, "User should be active after activation")
