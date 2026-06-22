from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from authentification.models import CustomUser, Recruteur, Etudiant  # adapte ce chemin si besoin

def connexion(request):

    if request.method == 'POST':

        print("Entré dans POST")
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser.objects.filter(email=email).first()



        if user is None:
            messages.error(request, "Aucun utilisateur avec cet email.")
            return render(request, 'connexion.html')

        if not check_password(password, user.password):
            messages.error(request, "Mot de passe incorrect.")
            return render(request, 'connexion.html')

        login(request, user)
        return redirect('accueil')  # modifie selon ta vue d’accueil

    return render(request, 'connexion.html')


def sucess(request):

    utilisateur = request.user
    return render(request, 'success.html', {'utilisateur' : utilisateur})


def custom_logout_view(request):
    request.session.flush()
    logout(request)
    return redirect('accueil')

@login_required(login_url='/auth/connexion/')
def profil(request):
    user = request.user

    if user.type_utilisateur == 'etudiant':
        etudiant = get_object_or_404(Etudiant, user=user)

        if request.method == 'POST':
            etudiant.nom = request.POST.get('nom')
            etudiant.prenom = request.POST.get('prenom')
            etudiant.age = request.POST.get('age')
            etudiant.sexe = request.POST.get('sexe')
            etudiant.telephone = request.POST.get('telephone')
            etudiant.adresse = request.POST.get('adresse')
            etudiant.niveau_etude = request.POST.get('niveau_etude')
            etudiant.specialiter = request.POST.get('specialiter')
            etudiant.save()
            return redirect('profil')

        return render(request, 'profil.html', {'user_data': etudiant})

    elif user.type_utilisateur == 'recruteur':
        recruteur = get_object_or_404(Recruteur, user=user)

        if request.method == 'POST':
            recruteur.name_entreprise = request.POST.get('name_entreprise')
            recruteur.adresse_entreprise = request.POST.get('adresse_entreprise')
            recruteur.site_internet = request.POST.get('site_internet')
            recruteur.contact = request.POST.get('contact')
            recruteur.forme_legale = request.POST.get('forme_legale')
            recruteur.langue = request.POST.get('langue')
            recruteur.secteur = request.POST.get('secteur')
            if 'logo' in request.FILES:
                recruteur.logo = request.FILES['logo']
            recruteur.save()
            return redirect('profil')

        return render(request, 'profil.html', {'user_data': recruteur})

    return redirect('accueil')

User = get_user_model()

@csrf_exempt  # Seulement si cette vue est utilisée en dehors du système de formulaire CSRF
@require_POST
def check_email_exists(request):
    response = {'success': False}

    email = request.POST.get('email')

    if email:
        email_exists = User.objects.filter(email=email).exists()
        response['success'] = True
        response['val'] = email_exists
    else:
        response['error'] = "Données manquantes dans la requête POST."

    return JsonResponse(response)


# transaction cest pour commit tout une fois
@require_POST
@transaction.atomic
def register_user(request):
    response = {'success': False}

    email = request.POST.get('email', '').strip()
    role = request.POST.get('role', '').strip()
    password = request.POST.get('password', '').strip()

    if email and role and password:
        try:
            with transaction.atomic():
                # Stockage temporaire dans la session
                request.session['email'] = email
                request.session['role'] = role

                # Création de l'utilisateur
                user = User.objects.create(
                    email=email,
                    password=make_password(password),  # Hachage du mot de passe
                    type_utilisateur=role  # ou 'role' si ton champ s'appelle comme ça
                )

                login(request, user)
                request.session.save()

            response['success'] = True

        except Exception as e:
            response['error'] = f'Erreur lors de la création de l’utilisateur : {str(e)}'
    else:
        response['error'] = 'Champs manquants dans la requête POST.'

    return JsonResponse(response)

def register_step_2(request):
    return render(request, 'register_step2.html')

@require_POST
@login_required
def save2(request):
    response = {'success': False}
    user = request.user

    # On suppose que le champ user.type_utilisateur existe déjà
    role = getattr(user, 'type_utilisateur', None)

    if not role:
        return JsonResponse({'success': False, 'error': 'Type utilisateur non défini.'})

    try:
        if role == 'etudiant':
            Etudiant.objects.create(
                user=user,
                nom=request.POST.get('nom'),
                prenom=request.POST.get('prenom'),
                age=request.POST.get('age'),
                sexe=request.POST.get('sexe'),
                telephone=request.POST.get('telephone'),
                adresse=request.POST.get('adresse'),
                niveau_etude=request.POST.get('niveau_etude'),
                specialiter=request.POST.get('specialite')
            )
            response['success'] = True

        elif role == 'recruteur':
            recruteur = Recruteur(
                user=user,
                nom_entreprise=request.POST.get('name_entreprise'),
                adresse_entreprise=request.POST.get('adresse_entreprise'),
                site_internet=request.POST.get('website'),
                forme_legale=request.POST.get('forme_legale'),
                langue=request.POST.get('langue'),
                secteur=request.POST.get('secteur'),
                contact=request.POST.get('telephone')
            )

            # Gestion du fichier logo
            # if 'logo' in request.FILES:
            #     logo = request.FILES['logo']
            #     if logo.size > 5 * 1024 * 1024:
            #         return JsonResponse({'success': False, 'error': 'Le logo dépasse 5 Mo.'})
            #     path = default_storage.save(f'logos/{logo.name}', ContentFile(logo.read()))
            #     recruteur.logo = path

            recruteur.save()
            response['success'] = True

        else:
            response['error'] = 'Rôle inconnu.'

    except Exception as e:
        response['error'] = str(e)

    return JsonResponse(response)



def info_utilisateur():
    return None


def inscription(request):
    return render(request, 'inscription.html')


def acceuil(request):
    return render(request,'acceuil.html')