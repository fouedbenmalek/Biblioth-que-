from django import forms
from .models import Emprunt

class EmpruntForm(forms.ModelForm):

    class Meta:
        model = Emprunt
        fields = [
            'livre',
            'nom_emprunteur',
            'date_retour'
        ]
        widgets = {
            'livre': forms.Select(attrs={'class': 'form-select'}),
            'nom_emprunteur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de l emprunteur'
            }),
            'date_retour': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }