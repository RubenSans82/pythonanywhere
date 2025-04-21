from django.db import models

# Create your models here.

class Receta(models.Model):
    nombre = models.CharField(max_length=200)
    tiempo_preparacion = models.CharField(max_length=50, blank=True) # Ej: "30 minutos"
    tiempo_coccion = models.CharField(max_length=50, blank=True) # Ej: "1 hora"
    ingredientes = models.TextField() # Usamos TextField para un bloque de texto largo
    instrucciones = models.TextField() # Usamos TextField para las instrucciones detalladas
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Se añade automáticamente al crear
    # Puedes añadir más campos después, como categoria, imagen, etc.

    def __str__(self):
        return self.nombre # Esto ayuda a identificar las recetas fácilmente en el admin