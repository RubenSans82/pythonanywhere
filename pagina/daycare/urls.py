# pagina/daycare/urls.py

from django.urls import path
from . import views

app_name = 'daycare'

urlpatterns = [
    # ... otras URLs de daycare ...

    # URL para la página de inicio (lista de mascotas del usuario logueado)
    path('', views.lista_mis_mascotas, name='home'),

    # URL para agregar una nueva mascota
    path('agregar-mascota/', views.agregar_mascota, name='agregar_mascota'),

    # URL para ver el detalle de una mascota específica, usando su ID (pk)
    path('<int:pk>/', views.detalle_mascota, name='detalle_mascota'), 
    
        # URL para editar una mascota específica
    path('editar/<int:pk>/', views.editar_mascota, name='editar_mascota'),
    
        # URL para eliminar una mascota específica
    path('eliminar/<int:pk>/', views.eliminar_mascota, name='eliminar_mascota'),
    
       # URL para la página de registro de Dueño/Usuario
    path('registro/', views.registro_owner, name='registro_owner'),
    
        # URL para el perfil/panel del Dueño
    path('perfil/', views.perfil_owner, name='perfil_owner'),
    
        # URL para solicitar una nueva reserva
    path('solicitar-reserva/', views.solicitar_reserva, name='solicitar_reserva'),

    # ... otras URLs futuras ...
]