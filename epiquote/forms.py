from django import forms
from django.contrib.auth import get_user_model
from django_registration.forms import RegistrationForm

User = get_user_model()


class UserRegistrationForm(RegistrationForm):
    username = forms.CharField(max_length=64, label='Login EPITA')
    email = None

    class Meta(RegistrationForm.Meta):
        model = User
        fields = [User.USERNAME_FIELD]

    def clean_username(self):
        if User.objects.filter(username=self.data['username']).exists():
            raise forms.ValidationError('Ce login est déjà enregistré.')
        return self.data['username']

    def save(self, *args, **kwargs):
        self.instance.email = self.cleaned_data['username'] + '@epita.fr'
        return super().save(*args, **kwargs)
