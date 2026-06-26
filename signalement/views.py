from django.shortcuts import redirect
from django.contrib import messages
from .models import Signalement


def signaler_vue(request):
    if request.method == 'POST':
        raison = request.POST.get('raison')
        details = request.POST.get('commentaire')
        annonce_id = request.POST.get('annonce_id')

        Signalement.objects.create(
            user=request.user,
            annonce_id=annonce_id,
            raison=raison,
            commentaire=details
        )

        messages.success(request, "Votre signalement a bien été envoyé ✅")
        return redirect('details_annonce', id=annonce_id)
