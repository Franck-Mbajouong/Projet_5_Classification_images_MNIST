from django.db import models
from django.utils import timezone
from authentification.models import Recruteur

class Annonce(models.Model):
    STATUT_CHOICES = [
        ('En attente de publication', 'En attente de publication'),
        ('En ligne', 'En ligne'),
        ('Expirée', 'Expirée'),
    ]

    date_creat = models.DateTimeField(default=timezone.now)
    recruteur = models.ForeignKey(Recruteur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=255, default='stage professionnel')
    date_limite = models.DateField()
    dure = models.CharField(max_length=50)
    lieu = models.CharField(max_length=255, null=True, blank=True)
    domaine = models.CharField(max_length=255)
    niveau_etude = models.CharField(max_length=255)
    langue_requises = models.CharField(max_length=255)
    statut_annonce = models.CharField(
        max_length=255,
        choices=STATUT_CHOICES,
        default='En attente de publication'
    )

    def __str__(self):
        # return self.titre or f"Annonce {self.id}"
        return f"{self.titre} ({self.type})"

