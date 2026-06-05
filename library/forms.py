from django import forms
from .models import Livre, Categorie


class LivreForm(forms.ModelForm):

    class Meta:
        model = Livre
        fields = '__all__'

        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Titre du livre'
            }),
            'auteur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Auteur'
            }),
            'categorie': forms.Select(attrs={
                'class': 'form-select'
            }),
            'annee_publication': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'quantite_disponible': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'statut': forms.Select(attrs={
                'class': 'form-select'
            }),
        }


class CategorieForm(forms.ModelForm):

    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom de la catégorie'
            }),
        }
