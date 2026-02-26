from django.test import TestCase, override_settings


class SecurityMiddlewareTest(TestCase):
    @override_settings(ALLOWED_HOSTS=['testserver'])
    def test_x_frame_options_present(self):
        """
        Verify that X-Frame-Options header is present to prevent clickjacking.
        """
        response = self.client.get('/')
        self.assertTrue(
            response.has_header('X-Frame-Options'),
            "X-Frame-Options header should be present",
        )
        self.assertEqual(response.headers['X-Frame-Options'], 'DENY')
