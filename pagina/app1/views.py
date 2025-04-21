from django.shortcuts import render, get_object_or_404
from .models import Receta # Importamos nuestro modelo Receta

# Vista para mostrar la lista de todas las recetas
def lista_recetas(request):
    # Recupera todas las recetas de la base de datos
    recetas = Receta.objects.all().order_by('nombre') # Ordenamos por nombre

    # Renderiza la plantilla 'app1/lista_recetas.html' y le pasa las recetas
    return render(request, 'app1/lista_recetas.html', {'recetas': recetas})

# Vista para mostrar los detalles de una receta específica
def detalle_receta(request, pk): # pk es el identificador primario de la receta
    # Recupera la receta con el pk dado, o muestra un 404 si no existe
    receta = get_object_or_404(Receta, pk=pk)

    # Renderiza la plantilla 'app1/detalle_receta.html' y le pasa la receta
    return render(request, 'app1/detalle_receta.html', {'receta': receta})