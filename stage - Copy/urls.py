from django.urls import path

from signalement.views import signaler_vue
from stage.views import mon_header, annonce_liste, parametres, liste_notifications, \
    marquer_notifications_comme_lues, liste_annonces_fetch, details_annonce, creer_ou_modifier_annonce, \
    dashboard, supprimer_annonce, modifier_annonce, liste_cv

urlpatterns = [

    path('header/', mon_header, name='header'),

    path('details_annonce/<int:id>/', details_annonce, name='details_annonce'),
    path('dashboard/', dashboard, name='dashboard' ),
    path('annonce/', creer_ou_modifier_annonce, name='creer_annonce'),
    path('annonce_liste/', annonce_liste, name='annonce_liste'),
    path('modifier_annonce/<int:pk>', modifier_annonce, name='modifier_annonce'),
    path('supprimer/<int:id>/', supprimer_annonce, name='supprimer_annonce'),
    path('liste_cv/', liste_cv, name='liste_cv'),

    # avec js pour le fetch
    path('api/annonces/', liste_annonces_fetch),

    # a coder

    path('parametres/', parametres, name='parametres'),
    # pour ajax

    path('notifications/', liste_notifications, name='liste_notifications'),
    path('changer-etat-notif/', marquer_notifications_comme_lues, name='changer_etat_notif'),

    # pour signaler
    path('signaler/', signaler_vue, name='signaler')
]
