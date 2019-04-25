from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm

User = get_user_model()


class UserRegistrationForm(RegistrationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Rename username field
        username_field = self.fields[User.USERNAME_FIELD]
        username_field.label = "Login EPITA"
        username_field.help_text = (
            "Si votre email est <code><strong>prenom.nom</strong>@epita.fr"
            "</code>, entrez <code><strong>prenom.nom</strong></code>."
        )

        # Delete email field
        email_field = User.get_email_field_name()
        del self.fields[email_field]

    def clean_username(self):
        if User.objects.filter(username=self.data['username']).exists():
            raise forms.ValidationError('Ce login est déjà enregistré.')
        return self.data['username']

    def save(self, *args, **kwargs):
        self.instance.email = self.cleaned_data['username'] + '@epita.fr'
        return super().save(*args, **kwargs)
