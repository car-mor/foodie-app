from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Buscar recetas...",
                "class": "form-control mr-sm-2",
            }
        ),
    )
