
from django.contrib import admin
from .models import Annonce

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'recruteur', 'date_creat', 'statut_annonce')
    list_filter = ('statut_annonce', 'type', 'domaine', 'niveau_etude')
    search_fields = ('titre', 'description', 'lieu')
    date_hierarchy = 'date_creat'
