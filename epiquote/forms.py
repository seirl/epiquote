import re
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django_registration.forms import RegistrationFormCaseInsensitive

User = get_user_model()


VALID_EPITA_LOGIN_REGEX = r"^[a-zA-Z0-9\._-]+$"


class EpitaLoginValidator(RegexValidator):
    message = "Le login EPITA n'est pas valide."
    regex = re.compile(VALID_EPITA_LOGIN_REGEX)


def epita_login_to_email(login: str):
    return login + "@epita.fr"


def email_to_username_validator(email_validator):
    return lambda username: email_validator(epita_login_to_email(username))


class UserRegistrationForm(RegistrationFormCaseInsensitive):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rename username field
        username_field = self.fields[User.USERNAME_FIELD]
        username_field.label = "Login EPITA"
        username_field.help_text = (
            "Si votre email est <code><strong>prenom.nom</strong>@epita.fr"
            "</code>, entrez <code><strong>prenom.nom</strong></code>."
        )
        username_field.validators.append(EpitaLoginValidator())

        # Delete email field
        email_field = User.get_email_field_name()
        self.email_validators_backup = self.fields[email_field].validators
        del self.fields[email_field]

    def clean_username(self):
        super().clean_username()
        username = self.data["username"].lower()
        self.instance.email = epita_login_to_email(username)
        # Run email validators on the generated email
        for validator in self.email_validators_backup:
            validator(self.instance.email)
        return username
