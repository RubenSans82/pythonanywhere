# pagina/daycare/urls.py

from django.urls import path
from . import views

app_name = 'daycare'

urlpatterns = [
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
        # URL para editar el perfil del Dueño logueado
    path('perfil/editar/', views.editar_perfil_owner, name='editar_perfil_owner'),
     # URL para la vista de la lista de reservas del dueño
    # Esta es la nueva URL para la página 'Reservas'
    path('reservas/', views.mis_reservas, name='mis_reservas'),
    # Asegúrate de que la URL para solicitar una NUEVA reserva sigue apuntando a su vista/plantilla
    # Si ya tenías algo como esto, déjalo como está:
    path('solicitar-reserva/', views.solicitar_reserva, name='solicitar_reserva'),
        # URL para ver el detalle de una reserva específica
    path('reserva/<int:pk>/', views.detalle_reserva, name='detalle_reserva'),
        # URL para cancelar una reserva específica
    path('reserva/<int:pk>/cancelar/', views.cancelar_reserva, name='cancelar_reserva'),

#-------------------- Staff --------------------#

        # URL para el listado de reservas para Staff
    path('staff/bookings/', views.staff_booking_list, name='staff_booking_list'),
        # URL para ver y editar el detalle de una reserva específica para Staff
    path('staff/bookings/<int:pk>/', views.staff_booking_detail, name='staff_booking_detail'),

    # ... otras URLs futuras ...
]