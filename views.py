# Mon application Django, fichier views.py

import google.generativeai as genai
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import markdown

# ATTENTION : Remplacez 'VOTRE_CLE_API' par votre clé API réelle.
# C'est une méthode DÉCONSEILLÉE pour la production.
# API_KEY = "AIzaSyCcWXKeVdlSxgUeyUM2OoQfjcdAZ0g2FAY"
API_KEY = "AIzaSyB07KdlUfILd9x82QmsA0Aiy7BS5I6R9Zw"

# Configurez la clé API de Gemini
genai.configure(api_key=API_KEY)


@csrf_exempt
def get_gemini_response(request):
    """
    Vue Django pour interagir avec le modèle Gemini.
    Elle reçoit un message d'une requête POST et renvoie une réponse de l'IA.
    """
    if request.method == "POST":
        try:
            # Récupérer le message de l'utilisateur
            user_message = request.POST.get("message")

            if not user_message:
                return JsonResponse({"error": "Aucun message fourni."}, status=400)

            # Choisir le modèle que vous souhaitez utiliser
            model = genai.GenerativeModel('gemini-2.0-flash')

            # Envoyer le message au modèle et obtenir une réponse
            response = model.generate_content(user_message)

            # Récupérer la réponse en texte de Gemini
            gemini_response = response.text

            # Convertir la réponse du format Markdown en HTML
            formatted_html_response = markdown.markdown(gemini_response)

            return JsonResponse({"response": formatted_html_response})



        except Exception as e:
            # Gérer les erreurs de l'API (ex: clé invalide, limite d'utilisation dépassée)
            return JsonResponse({"error": str(e)}, status=500)

    # Répondre avec une erreur si la méthode n'est pas POST
    return JsonResponse({"error": "Méthode non autorisée."}, status=405)

def chat(request):
    return render(request, "chatbot.html")