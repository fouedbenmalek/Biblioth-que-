from django.db import models


class Categorie(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class Livre(models.Model):
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('emprunte', 'Emprunté'),
        ('reserve', 'Réservé'),
    ]

    titre = models.CharField(max_length=200)
    auteur = models.CharField(max_length=200)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.CASCADE
    )

    annee_publication = models.IntegerField()
    quantite_disponible = models.IntegerField(default=1)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='disponible'
    )

    def __str__(self):
        return self.titre

class Emprunt(models.Model):
    livre = models.ForeignKey(
        Livre,
        on_delete=models.CASCADE
    )

    nom_emprunteur = models.CharField(
        max_length=100
    )

    date_emprunt = models.DateField(
        auto_now_add=True
    )

    date_retour = models.DateField(
        null=True,
        blank=True
    )

    retourne = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.nom_emprunteur} - {self.livre.titre}"