from django.test import TestCase
from epiquote.forms import UserRegistrationForm


class UserRegistrationFormTests(TestCase):
    def test_old_valid_login(self):
        form = UserRegistrationForm(
            data={"username": "cana_p", "password1": "foo", "password2": "foo"}
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.username, "cana_p")
        self.assertEqual(form.instance.email, "cana_p@epita.fr")

    def test_new_valid_login(self):
        form = UserRegistrationForm(
            data={
                "username": "pierre.cana1",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.username, "pierre.cana1")
        self.assertEqual(form.instance.email, "pierre.cana1@epita.fr")

    def test_invalid_login(self):
        form = UserRegistrationForm(
            data={
                "username": "a*b",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_generated_email(self):
        form = UserRegistrationForm(
            data={
                "username": ".",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertFalse(form.is_valid())

    def test_email_instead_of_login_fails(self):
        form = UserRegistrationForm(
            data={
                "username": "cana_p@epita.fr",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertFalse(form.is_valid())

    def test_login_gets_lowercased(self):
        form = UserRegistrationForm(
            data={
                "username": "Pierre.Cana",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertTrue(form.is_valid())
        self.assertEqual(form.instance.username, "pierre.cana")
        self.assertEqual(form.instance.email, "pierre.cana@epita.fr")

    def test_duplicate_logins(self):
        form1 = UserRegistrationForm(
            data={
                "username": "cana_p",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertTrue(form1.is_valid())
        form1.save()

        form2 = UserRegistrationForm(
            data={
                "username": "cana_p",
                "password1": "bar",
                "password2": "bar",
            }
        )
        self.assertFalse(form2.is_valid())

    def test_duplicate_logins_different_case(self):
        form1 = UserRegistrationForm(
            data={
                "username": "pierre.cana",
                "password1": "foo",
                "password2": "foo",
            }
        )
        self.assertTrue(form1.is_valid())
        form1.save()

        form2 = UserRegistrationForm(
            data={
                "username": "Pierre.Cana",
                "password1": "bar",
                "password2": "bar",
            }
        )
        self.assertFalse(form2.is_valid())
