from django import forms


class SearchProfileForm(forms.Form):
    name = forms.CharField(label="Come si chiama l'utente che vuoi cercare?", max_length=100, min_length=3,
                           required=True)


class SearchTweetForm(forms.Form):
    choices = [
        ("Sport", "Sport"),
        ("Politica", "Politica"),
        ("Cinema", "Cinema"),
        ("Musica", "Musica"),
        ("Viaggi", "Viaggi"),
        ("Tecnologia", "Tecnologia"),
        ("Cucina", "Cucina"),
        ("Arte", "Arte"),
        ("Fotografia", "Fotografia")
    ]
    text = forms.CharField(label="Scrivi il testo che vuoi cercare (opzionale)", max_length=100, required=False)
    category = forms.ChoiceField(label="Quale categoria ti interessa?", required=True, choices=choices)
