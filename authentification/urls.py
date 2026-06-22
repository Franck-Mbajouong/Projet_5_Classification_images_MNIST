from django.urls import path

from authentification.views import connexion, custom_logout_view, profil, info_utilisateur, sucess, inscription, \
    check_email_exists, register_user, register_step_2, save2,acceuil

urlpatterns = [
    path('connexion/', connexion, name='connexion'),
    path('inscription/', inscription, name='inscription'),
    path('logout/', custom_logout_view, name='logout'),
    path('sucess/', sucess, name='sucess'),

    path('profil/', profil, name='profil'),

    # pour ajax
    path('check-email/', check_email_exists, name='check_email_exists'),
    path('register/', register_user, name='register_user'),
    path('register/step2/', register_step_2, name='register_step_2'),
    path('save2/', save2, name='save2'),

    path('utilisateur-info/', info_utilisateur, name='info_utilisateur'),
    # path('supprimer/<str:table>/<int:item_id>/', views.supprimer_objet, name='supprimer_objet'),
]

