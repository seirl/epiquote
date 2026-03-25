from django.test import TestCase

class ClickjackingTestCase(TestCase):
    def test_x_frame_options_header(self):
        response = self.client.get('/')
        self.assertIn('X-Frame-Options', response, "X-Frame-Options header missing")
        self.assertEqual(response['X-Frame-Options'], 'DENY')
