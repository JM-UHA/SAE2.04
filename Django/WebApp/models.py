from django.db import models
from enum import Enum

# Create your models here.

class EmplacementChoices(Enum):
    murs = "Murs"
    platfond = "Plafonds"


class Capteur(models.Model):
    # ID de l'entrée ?
    id = models.CharField(primary_key=True, unique=True) # ID
    capteur_id: models.CharField(unique=True)
    nom = models.CharField()  # Maison1/Maison2
    piece = models.CharField()
    lieu = models.CharField()
    emplacement = models.CharField(choices=EmplacementChoices, null=True, blank=True)


class Donnee(models.Model):
    # ID capteur ? ID entrée ?
    id = models.BigAutoField(primary_key=True, unique=True)
    capteur: models.ForeignKey["Capteur"] = models.ForeignKey("Capteur", to_field="capteur_id", on_delete=models.CASCADE)  # ID du capteur associé
    date = models.DateField()  # Date
    time = models.TimeField()  # Time
    temperature = models.DecimalField()  # Température
