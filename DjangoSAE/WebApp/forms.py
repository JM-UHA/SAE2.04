from django import forms
from django.forms import ModelForm

from . import models


class DonneeForm(forms.Form):
    capteur_id = forms.ModelChoiceField(
        queryset=models.Capteur.objects.all(), required=False, label="Capteur"
    )
    date_min = forms.DateField(
        required=False,
        label="Date min",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "datepicker", "lang": "fr-FR"}
        ),
    )
    date_max = forms.DateField(
        required=False,
        label="Date max",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "datepicker", "lang": "fr-FR"}
        ),
    )
    heure_min = forms.TimeField(
        required=False,
        label="Heure min",
        widget=forms.TimeInput(
            attrs={"type": "time", "class": "timepicker", "lang": "fr-FR"}
        ),
    )
    heure_max = forms.TimeField(
        required=False,
        label="Heure max",
        widget=forms.TimeInput(
            attrs={"type": "time", "class": "timepicker", "lang": "fr-FR"}
        ),
    )
    temperature_min = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label="Température minimum"
    )
    temperature_max = forms.DecimalField(
        max_digits=5, decimal_places=2, required=False, label="Température maximum"
    )


class CapteurForm(ModelForm):
    class Meta:
        model = models.Capteur
        fields = ("nom", "emplacement")
        labels = {
            "nom": "Nom",
            "emplacement": "Emplacement",
        }
