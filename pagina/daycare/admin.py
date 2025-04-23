# pagina/daycare/admin.py

from django.contrib import admin
from .models import Owner, Pet, Booking, Service # Asegúrate de importar Booking

# Register your models here.

admin.site.register(Owner)
admin.site.register(Pet)
admin.site.register(Booking) # <--- Registra el modelo Booking
admin.site.register(Service)