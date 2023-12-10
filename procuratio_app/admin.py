from django.contrib import admin
from .models import *

admin.site.register(Utilisateur)
admin.site.register(Client)
admin.site.register(Produit)
admin.site.register(Service)
admin.site.register(Transaction)

"""
admin.site.register(HistoriqueA)
admin.site.register(RendezVous)
admin.site.register(CampagnePub)
"""