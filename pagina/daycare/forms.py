# pagina/daycare/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet, Owner, Booking # Asegúrate de importar Booking

# Nuestro formulario PetForm (ya lo teníamos)
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nombre', 'raza', 'fecha_nacimiento', 'notas_medicas', 'comportamiento_notas', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'notas_medicas': forms.Textarea(attrs={'rows': 4}),
            'comportamiento_notas': forms.Textarea(attrs={'rows': 4}),
        }

# Nuevo formulario para el registro de usuario (Dueño)
class OwnerRegistrationForm(UserCreationForm): # Hereda de UserCreationForm
    # Añadimos campos que vienen del modelo User (aunque UserCreationForm ya los incluye por defecto)
    # Los listamos aquí si queremos personalizarlos o añadir validaciones específicas
    # email = forms.EmailField(required=True) # Si quieres que el email sea obligatorio

    # Añadimos campos que vienen de nuestro modelo Owner
    telefono = forms.CharField(max_length=15, required=False, help_text='Opcional')
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, help_text='Opcional')

    class Meta(UserCreationForm.Meta): # Hereda la clase Meta de UserCreationForm
        # UserCreationForm.Meta.fields por defecto son ('username', 'password', 'password2')
        # Aquí añadimos email, first_name, last_name del modelo User
        model = User # Este formulario sigue estando basado en el modelo User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        # Asegúrate de que los campos añadidos aquí también existan en el modelo User

    # Sobrescribimos el método save() para crear también el perfil Owner
    def save(self, commit=True):
        # Llama al método save() de la clase padre (UserCreationForm)
        # Esto crea y guarda el objeto User
        user = super().save(commit=True)

        # Crea el perfil Owner y lo vincula al usuario recién creado
        owner_profile = Owner(user=user,
                              telefono=self.cleaned_data.get('telefono', ''), # Usamos .get para valores opcionales
                              direccion=self.cleaned_data.get('direccion', ''))
        owner_profile.save() # Guarda el perfil Owner en la base de datos

        return user # Devuelve el objeto User creado (como hace el UserCreationForm original)
    
    # Nuevo formulario para crear una Reserva
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # Incluimos los campos que el usuario va a rellenar
        fields = ['pet', 'date', 'time', 'notes']
        # El campo 'status' y 'created_at' se manejan en la vista o modelo

        # Opcional: Añadir widgets para una mejor entrada de fecha/hora
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Input de fecha HTML5
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}), # Input de hora HTML5
            'notes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}), # Área de texto para notas
            'pet': forms.Select(attrs={'class': 'form-select'}), # Select estilizado por Bootstrap
        }

    # Sobrescribimos el método __init__ para filtrar las opciones del campo 'pet'
    def __init__(self, *args, **kwargs):
        # El usuario logueado se pasa como un argumento 'user' al crear la instancia del formulario en la vista
        user = kwargs.pop('user', None) # Obtenemos el argumento 'user' y lo removemos de kwargs
        super().__init__(*args, **kwargs) # Llamamos al __init__ de la clase padre

        # Filtramos las opciones del campo 'pet'
        if user and user.is_authenticated:
            try:
                # Obtenemos el perfil Owner del usuario logueado
                owner_profile = user.owner
                # Filtramos el queryset del campo 'pet' para incluir solo las mascotas de este owner
                self.fields['pet'].queryset = Pet.objects.filter(owner=owner_profile).order_by('nombre')
            except Owner.DoesNotExist:
                 # Si por alguna razón el usuario logueado no tiene perfil Owner,
                 # dejamos el queryset vacío para evitar errores.
                 self.fields['pet'].queryset = Pet.objects.none()
        else:
            # Si no hay usuario logueado o no está autenticado, dejamos el queryset vacío
            self.fields['pet'].queryset = Pet.objects.none()
            
            