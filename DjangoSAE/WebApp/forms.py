from django import forms
from django.forms import ModelForm

from . import models


class DonneeForm(forms.Form):
    capteur_id = forms.ModelChoiceField(
        queryset=Capteur.objects.all(), 
        required=False, 
        label="Capteur"
    )
    date_min = forms.DateField(required=False, label="Avant date")
    date_max = forms.DateField(required=False, label="Après date")
    heure_min = forms.TimeField(required=False, label="Avant heure")
    heure_max = forms.TimeField(required=False, label="Après heure")
    temperature_min = forms.DecimalField(max_digits=5, decimal_places=2, required=False, label="Température minimum")
    temperature_max = forms.DecimalField(max_digits=5, decimal_places=2, required=False, label="Température maximum")


class CapteurForm(ModelForm):
    class Meta:
        model = models.Capteur
        fields = ("nom", "emplacement")
        labels = {
            "nom": "Nom",
            "emplacement": "Emplacement",
        }
