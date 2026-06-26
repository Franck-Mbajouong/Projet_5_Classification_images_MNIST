from tkinter.constants import CASCADE

from django.db import models

from authentification.models import CustomUser
from stage.models import Annonce


class Signalement(models.Model):

    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('resolu', 'resolu'),
        ('Rejete', 'Rejete'),
    ]

    RAISONS_SIGNAL = [
        ("inapproprie", "Contenu inapproprié"),
        ("mensonger", "Fausse information"),
        ("harcelement", "Harcèlement"),
        ("illegal", "Contenu illégal"),
        ("spam", "Spam ou publicité"),
        ("usurpation", "Usurpation d’identité"),
        ("fraude", "Escroquerie ou fraude"),
        ("violence", "Contenu violent"),
        ("interdit", "Produit interdit"),
        ("copyright", "Violation de droits"),
    ]

    raison = models.CharField(max_length=50, choices=RAISONS_SIGNAL, blank=True, null=True)

    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, related_name='annonce')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    raison = models.CharField(choices=RAISONS_SIGNAL)
    commentaire = models.TextField(max_length=1000, blank=True)
    date_crea = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(choices=STATUT_CHOICES, default="En attente")


    def __str__(self):
        return f"{self.user} a signale {self.annonce}"
