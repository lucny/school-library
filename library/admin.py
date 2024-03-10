from django.contrib import admin
from .models import Autor, Zanr, Vydavatelstvi, Kniha

admin.site.register(Autor)
admin.site.register(Zanr)
admin.site.register(Vydavatelstvi)
admin.site.register(Kniha)