from django.urls import path
from . import views # Importamos las vistas de nuestra aplicación

# Namespace para la aplicación (opcional pero recomendado para proyectos grandes)
# app_name = 'app1'

urlpatterns = [
    # path() define una URL:
    # El primer argumento es la 'ruta' URL ('' significa la raíz de esta app)
    # El segundo argumento es la función de vista a llamar
    # El tercer argumento 'name' es un nombre para esta URL, útil para referenciarla en plantillas o código Python
    path('', views.lista_recetas, name='lista_recetas'),

    # Para los detalles de una receta, usamos una parte variable en la URL: <int:pk>
    # <int:pk> captura un número entero (el ID de la receta) y lo pasa como argumento 'pk' a la vista
    path('<int:pk>/', views.detalle_receta, name='detalle_receta'),
]