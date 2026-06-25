from django.urls import path

from chatbot.views import chat, get_gemini_response

urlpatterns = [
    path('monChat/', get_gemini_response, name='get_gemini_response'),
    path('chat/', chat, name='chat'),

]