from django import forms

from quotes.models import Quote


class SearchForm(forms.Form):
    q = forms.CharField()

    def clean_q(self):
        q = self.cleaned_data['q']
        if len(q.split()) > 30:
            raise forms.ValidationError("Trop de mots.")
        if len(q) > 300:
            raise forms.ValidationError("Trop de lettres.")
        return q


class AddQuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['author', 'context', 'content']
        widgets = {
            'context': forms.TextInput(),
            'content': forms.Textarea(
                attrs={'cols': '140', 'rows': '10', 'class': 'add-quote'}),
        }
