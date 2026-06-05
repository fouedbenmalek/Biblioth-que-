from django.contrib import admin
from .models import Livre, Categorie, Emprunt

admin.site.register(Livre)
admin.site.register(Categorie)
admin.site.register(Emprunt)