from django.contrib.auth import get_user_model
from django import forms
from registration.forms import RegistrationForm

User = get_user_model()


class SearchForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        q = self.cleaned_data['q']
        if len(q.split()) > 30:
            raise forms.ValidationError("Trop de mots.")
        if len(q) > 300:
            raise forms.ValidationError("Trop de lettres.")
        return q


class AddQuoteForm(forms.Form):
    author = forms.CharField(label="Auteur")
    context = forms.CharField(label="Contexte", required=False)
    content = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'cols': '140',
                                     'rows': '10',
                                     'class': 'add-quote'}),
    )


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
