from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse

from candidature.models import Candidature
from .models import Annonce

def accueil(request):
    return render(request, 'acceuil.html')

def liste_annonces_fetch(request):
    annonces = Annonce.objects.select_related('recruteur').filter(statut_annonce='En ligne').order_by('-date_creat')
    data = {
        "success": True,
        "annonce": []
    }

    for annonce in annonces:
        data["annonce"].append({
            "id_annonce": annonce.id,
            "titre": annonce.titre,
            "description": annonce.description,
            "type": annonce.type,
            "date_limite": annonce.date_limite.isoformat(),
            "date_creat": annonce.date_creat.isoformat(),
            "dure": annonce.dure,
            "lieu": annonce.lieu,
            "domaine": annonce.domaine,
            "niveau_etude": annonce.niveau_etude,
            "langue_requises": annonce.langue_requises,
            "statut_annonce": annonce.statut_annonce,
            "nom_entreprise": annonce.recruteur.nom_entreprise,
            "adresse_entreprise": annonce.recruteur.adresse_entreprise,
            "logo": annonce.recruteur.logo or "assets/default_logo.svg"  # Chemin relatif
        })

    return JsonResponse(data)

def details_annonce(request, id):

    item_id = id
    # return HttpResponse(id)

    annonce = get_object_or_404(Annonce, pk = item_id)

    return render(request, 'details_annonce.html', {"annonce" : annonce})

def dashboard (request):
    if not request.user.is_authenticated:
        return redirect('connexion')  # Redirige vers la page de login

    return render(request, 'dashboard.html')

@login_required(login_url='/')
def creer_ou_modifier_annonce(request):

    id_annonce = request.GET.get('id')
    if id_annonce:
        annonce = get_object_or_404(Annonce, pk=id_annonce)
    else:
        annonce = None

    if request.method == 'POST':
        titre = request.POST.get('title')
        description = request.POST.get('description')
        domaine = request.POST.get('domain')
        lieu = request.POST.get('location')
        type_stage = request.POST.get('type')
        duree = request.POST.get('duration')
        date_limite = request.POST.get('start-date')
        niveau_etude = request.POST.get('level')
        langue_requises = request.POST.get('languages')

        if annonce:  # Modification
            annonce.titre = titre
            annonce.description = description
            annonce.domaine = domaine
            annonce.lieu = lieu
            annonce.type = type_stage
            annonce.dure = duree
            annonce.date_limite = date_limite
            annonce.niveau_etude = niveau_etude
            annonce.langue_requises = langue_requises
            annonce.save()
            # messages.success(request, "Annonce modifiée avec succès.")
        else:  # Création
            Annonce.objects.create(
                titre=titre,
                description=description,
                domaine=domaine,
                lieu=lieu,
                type=type_stage,
                dure=duree,
                date_limite=date_limite,
                niveau_etude=niveau_etude,
                langue_requises=langue_requises,
                recruteur=request.user.recruteur  # à adapter selon votre modèle
            )
            # messages.success(request, "Annonce créée avec succès.")
        return redirect('annonce_liste')  # à adapter avec le nom de votre URL

    return render(request, 'creer_annonce.html', {'annonce': annonce})
    # return render(request, 'creer_annonce.html')

@login_required(login_url='/')
def annonce_liste(request):

    annonces = Annonce.objects.all().filter(recruteur = request.user.recruteur)
    return render(request, 'liste_annonces.html',{"annonces" : annonces} )

@login_required(login_url='/')
def supprimer_annonce(request, id):

    annonce = get_object_or_404(Annonce, pk=id)
    annonce.delete()
    return redirect('annonce_liste')

@login_required(login_url='/')
def modifier_annonce(request, pk):

    id_annonce = pk

    if id_annonce:
        annonce = get_object_or_404(Annonce, pk=id_annonce)
    else:
        annonce = None

    if request.method == 'POST':
        titre = request.POST.get('title')
        description = request.POST.get('description')
        domaine = request.POST.get('domain')
        lieu = request.POST.get('location')
        type_stage = request.POST.get('type')
        duree = request.POST.get('duration')
        date_limite = request.POST.get('start-date')
        niveau_etude = request.POST.get('level')
        langue_requises = request.POST.get('languages')

        if annonce:  # Modification
            annonce.titre = titre
            annonce.description = description
            annonce.domaine = domaine
            annonce.lieu = lieu
            annonce.type = type_stage
            annonce.dure = duree
            annonce.date_limite = date_limite
            annonce.niveau_etude = niveau_etude
            annonce.langue_requises = langue_requises
            annonce.save()
            # messages.success(request, "Annonce modifiée avec succès.")

            # messages.success(request, "Annonce créée avec succès.")
        return redirect('annonce_liste')  # à adapter avec le nom de votre URL

    return render(request, 'creer_annonce.html', {'annonce': annonce})



def parametres(request):
    pass


def mon_header(request):
    return render(request, 'header.html')


# pour ajax
def liste_notifications():
    return None


def marquer_notifications_comme_lues():
    return None


def liste_cv(request):
    # Récupérer toutes les candidatures, triées par étudiant (via user_id)
    candidatures = (
        Candidature.objects
        .select_related('etudiant')
        .order_by('etudiant__user__id', '-date')
    )

    # Garder un seul CV (le plus récent) par étudiant
    cvs_uniques = {}
    for c in candidatures:
        if c.etudiant_id not in cvs_uniques:
            cvs_uniques[c.etudiant_id] = c

    cvs = list(cvs_uniques.values())

    return render(request, 'liste_cv.html', {'cvs': cvs})