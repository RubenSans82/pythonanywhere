# pagina/daycare/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pet, Owner, Booking, STATUS_CHOICES # Asegúrate de importar Booking

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
    
    
# Nuevo formulario para editar el perfil del Dueño (teléfono y dirección)
class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model = Owner # Este formulario se basa en el modelo Owner
        # Incluimos solo los campos que el usuario puede editar en su perfil
        fields = ['telefono', 'direccion']
        # No incluimos el campo 'user' ya que esa relación no debe cambiarse aquí

        # Widgets opcionales para estilo Bootstrap
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}), # Input de texto simple
            'direccion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}), # Área de texto
        }

# --- Nuevo formulario combinado para editar User y Owner profile juntos ---
class UserOwnerProfileForm(forms.Form):
    # Campos del modelo User que queremos editar
    # Asegúrate de usar los mismos nombres de campo que en el modelo User
    first_name = forms.CharField(max_length=150, required=False, label='Nombre') # Nombre de pila
    last_name = forms.CharField(max_length=150, required=False, label='Apellido') # Apellido
    # El email en el modelo User suele ser único. Lo marcamos como requerido.
    email = forms.EmailField(required=True, label='Correo Electrónico')

    # Campos del modelo Owner que queremos editar
    telefono = forms.CharField(max_length=15, required=False, label='Teléfono')
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label='Dirección')


    # Método __init__ para pre-llenar el formulario con instancias existentes de User y Owner
    def __init__(self, *args, **kwargs):
        # Este formulario espera recibir las instancias 'user' y 'owner_profile' al ser creado
        user_instance = kwargs.pop('user', None)
        owner_profile_instance = kwargs.pop('owner_profile', None)

        super().__init__(*args, **kwargs)

        # Si recibimos instancias, inicializamos los campos del formulario con sus datos actuales
        if user_instance:
            self.fields['first_name'].initial = user_instance.first_name
            self.fields['last_name'].initial = user_instance.last_name
            self.fields['email'].initial = user_instance.email

        if owner_profile_instance:
             self.fields['telefono'].initial = owner_profile_instance.telefono
             self.fields['direccion'].initial = owner_profile_instance.direccion

        # Guardamos las instancias como atributos internos del formulario para usarlas en el método save()
        self._user = user_instance
        self._owner_profile = owner_profile_instance


    # Método save() personalizado para guardar los datos en AMBAS instancias (User y OwnerProfile)
    def save(self, commit=True):
        # Asegurarse de que tenemos las instancias de User y OwnerProfile para actualizar
        if not self._user or not self._owner_profile:
            raise ValueError("Para guardar UserOwnerProfileForm, las instancias 'user' y 'owner_profile' deben pasarse al constructor.")

        # Actualizar los campos del objeto User con los datos limpios del formulario
        self._user.first_name = self.cleaned_data['first_name']
        self._user.last_name = self.cleaned_data['last_name']
        self._user.email = self.cleaned_data['email'] # Django validará el formato y unicidad si es requerido

        # Actualizar los campos del objeto OwnerProfile con los datos limpios del formulario
        self._owner_profile.telefono = self.cleaned_data['telefono']
        self._owner_profile.direccion = self.cleaned_data['direccion']

        # Guardar los objetos en la base de datos
        if commit:
            self._user.save() # Guarda los cambios en el objeto User
            self._owner_profile.save() # Guarda los cambios en el objeto OwnerProfile

        # Opcional: devolver las instancias actualizadas
        return (self._user, self._owner_profile)

    # Puedes añadir validaciones adicionales aquí si es necesario (ej: def clean_email(self):)

    
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
            
    # Definir el formulario de cambio de estado (en línea)
class ChangeBookingStatusForm(forms.Form):
    new_status = forms.ChoiceField(
        choices=STATUS_CHOICES,  # Usa las opciones de estado del modelo Booking
        label='Nuevo Estado',
        widget=forms.Select(attrs={'class': 'form-control'})  # Clase de Bootstrap para el estilo
    )