from django.db import models

# Create your models here.


class Capteur(models.Model):
    nom = models.CharField(max_length=50, blank=True, null=True)
    capteur_id = models.CharField(unique=True, max_length=12)
    piece = models.CharField(max_length=50)
    lieu = models.CharField(max_length=50)
    emplacement = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        if self.nom:
            return self.nom
        return self.capteur_id

    class Meta:
        managed = False
        db_table = "capteurs"


class Donnee(models.Model):
    # ID capteur ? ID entrée ?
    capteur = models.ForeignKey(Capteur, models.CASCADE, to_field="capteur_id")
    date = models.DateField()
    heure = models.TimeField()
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = False
        db_table = "donnees"
