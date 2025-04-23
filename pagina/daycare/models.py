from django.db import models
from django.contrib.auth.models import User
# Importamos DateField, TimeField, DateTimeField si no están ya importados por otros modelos
from django.db.models import DateField, TimeField, DateTimeField, TextField, CharField, ForeignKey
from django.utils import timezone # Importar timezone

# Modelo para representar al dueño de la mascota
# Extiende el modelo de Usuario incorporado de Django con información adicional
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Relación uno-a-uno con el Usuario de Django
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    # Puedes añadir más campos de contacto si es necesario

    def __str__(self):
        return f"Perfil de {self.user.username}"

# Modelo para representar una mascota
class Pet(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets') # Relación muchos-a-uno con Dueño
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    foto = models.ImageField(upload_to='pets_photos/', blank=True, null=True)
    notas_medicas = models.TextField(blank=True, null=True) # Alergias, medicaciones, etc.
    comportamiento_notas = models.TextField(blank=True, null=True, verbose_name='Notas sobre la Mascota') # Cómo se lleva con otros perros, etc.

    def __str__(self):
        return self.nombre

# Definir opciones para el estado de la reserva
STATUS_CHOICES = [
    ('Pending', 'Pendiente'),
    ('Confirmed', 'Confirmada'),
    ('Cancelled', 'Cancelada'),
    ('Completed', 'Completada'),
]


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Nombre del Servicio') # Nombre único del servicio
    description = models.TextField(blank=True, null=True, verbose_name='Descripción') # Descripción detallada
    # Opcional: Precio (usamos DecimalField para dinero)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='Precio')
    # Opcional: Duración (si aplica y es estándar, puedes usar un CharField o un campo de Duración si tu DB lo soporta bien)
    duration_description = models.CharField(max_length=100, blank=True, null=True, verbose_name='Duración (ej: Medio día, 1 hora)')

    is_active = models.BooleanField(default=True, verbose_name='Activo') # Para poder desactivar servicios temporalmente

    def __str__(self):
        return self.name # La representación legible es el nombre del servicio

    class Meta:
        verbose_name = 'Servicio' # Nombre singular en el Admin/Django
        verbose_name_plural = 'Servicios' # Nombre plural en el Admin/Django
        ordering = ['name'] # Ordenar servicios alfabéticamente por nombre


## Modelo para representar una Reserva
class Booking(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings', verbose_name='Servicio')
    date = models.DateField()
    time = models.TimeField()
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    # Campo para las notas que el Dueño dejó al hacer la reserva
    notes = models.TextField(blank=True, null=True, verbose_name='Notas del Dueño al Reservar')
    created_at = models.DateTimeField(auto_now_add=True)

    # --- Nuevo campo para Notas Internas del Staff ---
    staff_notes = models.TextField(blank=True, null=True, verbose_name='Notas Internas del Staff') # <--- Añade este campo
    # --- Fin Nuevo campo ---


    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"Reserva {self.pk} para {self.pet.nombre} - {self.service.name} el {self.date} ({self.status})"