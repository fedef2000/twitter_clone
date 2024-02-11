from django import forms
from .models import choices

class SearchProfileForm(forms.Form):
    name = forms.CharField(label="Come si chiama l'utente che vuoi cercare?", max_length=100, min_length=3, required=True)


class SearchTweetForm(forms.Form):
    choices = choices
    text = forms.CharField(label="Scrivi il testo che vuoi cercare (opzionale)", max_length=100, required=False)
    category = forms.ChoiceField(label="Quale categoria ti interessa?", required=True, choices=choices)
