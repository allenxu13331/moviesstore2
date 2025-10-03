from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title you want to see'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why should this movie be added?', 'rows': 4}),
        }
