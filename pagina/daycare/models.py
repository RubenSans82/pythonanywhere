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
    comportamiento_notas = models.TextField(blank=True, null=True) # Cómo se lleva con otros perros, etc.

    def __str__(self):
        return self.nombre

# Definir opciones para el estado de la reserva
STATUS_CHOICES = [
    ('Pending', 'Pendiente'),
    ('Confirmed', 'Confirmada'),
    ('Cancelled', 'Cancelada'),
    ('Completed', 'Completada'),
]

# Nuevo Modelo para representar una Reserva
class Booking(models.Model):
    # Relación con la mascota: una reserva es para una mascota específica
    # Si la mascota se elimina, también se elimina la reserva (CASCADE)
    pet = ForeignKey(Pet, on_delete=models.CASCADE, related_name='bookings')

    # Podrías añadir una relación directa al Owner, pero ya está implícita a través de pet.owner
    # owner = ForeignKey(Owner, on_delete=models.CASCADE, related_name='bookings')

    # Fecha y hora de la reserva
    date = DateField()
    # Usaremos TimeField para una hora específica, o podrías usar CharField para 'Mañana'/'Tarde'
    time = TimeField()

    # Estado de la reserva (ej: Pendiente, Confirmada)
    status = CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Notas adicionales para la reserva (opcional)
    notes = TextField(blank=True, null=True)

    # Fecha y hora en que se creó esta reserva
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        # Opcional: Ordenar las reservas por fecha y hora por defecto
        ordering = ['date', 'time']

    def __str__(self):
        # Representación legible del objeto reserva
        return f"Reserva para {self.pet.nombre} el {self.date} a las {self.time} - {self.status}"