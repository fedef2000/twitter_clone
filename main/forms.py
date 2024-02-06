from django import forms


class SearchForm(forms.Form):
    CHOICE_LIST = [
        ("Users", "utenti"),
        ("Tweets", "tweet")
    ]
    search_string = forms.CharField(label="Cosa vuoi cercare?", max_length=100, min_length=3, required=True)
    search_where = forms.ChoiceField(label="Dove lo vuoi cercare?", required=True, choices=CHOICE_LIST)
