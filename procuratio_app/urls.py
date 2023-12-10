from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='index'),
    path('Padmin/',adminboard,name='Adminboard'),
    path('login/',loginU,name='loginA'),
    path("register/",registerC,name='registerA'),
    path("logout/",logoutU,name='logout'),
    path("produit_list/",productlist,name='productlist'),
    path("service_list/",servicelist,name='servicelist'),
    path("client_list/",clientlist,name='clientlist'),
    path("reservationlist/",reservationlist,name='reservationlist'),
    path("productshop/",produitlclient,name='produitsC'),
    path("serviceshop/",servicesclient,name='servicesC'),
    path("profile/",profil_user,name='profile'),
    path('profile/reset-password', resetPassword, name='resetPassword'),
    path("Rendez-vous/<str:service_id>",prendre_rendezvous,name="prendre_rendezvous"),
    path('reservations/', listreservations, name='user_reservations'),
    path('create_reservation/', create_reservation, name='create_reservation'),
    ####################################################################################

    path('ajouterproduit/', ajouterproduit, name='ajouterproduit'),
    path('modifierproduit/<str:produit_id>', modifierproduit, name='modifierproduit'),
    path('supprimerproduit/<str:produit_id>/', supprimerproduit, name='supprimerproduit'),

    path('ajouterservice/', ajouterservice, name='ajouterservice'),
    path('modifierservice/<str:service_id>', modifierservice, name='modifierservice'),
    path('supprimerservice/<str:service_id>/', supprimerservice, name='supprimerservice'),

    path('articles/<int:article_id>',articlepage,name='articles'),

    path('add-to-cart', add_to_cart, name='add-to-cart'),
    path('view_cart', view_cart, name='viewpanier'),
    path('delete-from-cart',delete_cart_item,name='delete-from-cart'),
    path('update-cart',update_cart_item,name='update-cart'),

    path('checkout', checkout, name='checkout'),

    path('fidelite-programme/',fidelityprog,name='fidelite'),
    path('fidelity-update', fidelity_update, name='fidelity-update'),

    path('historique-achat',historiqueA,name='historique'),

]