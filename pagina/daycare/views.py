# pagina/daycare/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Asegúrate de que Booking, STATUS_CHOICES Y Service están importados
from .models import Owner, Pet, Booking, STATUS_CHOICES, Service, OwnerProfile 
# Asegúrate de que tus formularios necesarios están importados
from .forms import PetForm, OwnerRegistrationForm, BookingForm, ChangeBookingStatusForm, UserOwnerProfileForm, StaffNotesForm
from django.http import HttpResponseForbidden
from datetime import date
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.urls import reverse_lazy


# --- NUEVA VISTA: Landing Page ---
# Esta vista no tiene el decorador @login_required
def landing_page(request):
    # Obtenemos la lista de servicios activos para mostrarlos en la landing page.
    # Usamos .filter(is_active=True) para solo mostrar los que marcaste como activos en el admin.
    services = Service.objects.filter(is_active=True).order_by('name')

    # Preparamos el contexto con los datos que la plantilla necesita
    context = {
        'services': services, # Pasamos el queryset de servicios activos
        # Puedes añadir otras variables aquí, como un título, etc.
        # 'landing_title': "Tu Amigo Fiel: Cuidado Canino con Amor"
    }

    # Renderizamos la plantilla 'landing_page.html'.
    # Asegúrate de crear este archivo en tu carpeta de templates.
    return render(request, 'daycare/landing_page.html', context)

# Nueva vista para agregar una mascota - MISMO CÓDIGO
@login_required # Este decorador asegura que solo usuarios autenticados puedan acceder a esta vista
def agregar_mascota(request):
    # ... try-except para Owner.DoesNotExist ...
    try:
        owner_profile = request.user.owner
    except Owner.DoesNotExist:
         return render(request, 'daycare/error_no_owner_profile.html', {'mensaje': 'Tu cuenta de usuario no tiene un perfil de Dueño asociado.'})

    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.owner = owner_profile
            mascota.save()
            messages.success(request, f'{mascota.nombre} ha sido agregada a tu perfil.') # Mensaje más útil
            return redirect('daycare:home') # Redirigir a la lista de mascotas

    else:
        form = PetForm()

    return render(request, 'daycare/agregar_mascota.html', {'form': form})

# Nueva vista para la página de inicio (redirige a lista_mis_mascotas) - NO USADA CON LA URL ''
# def home_page(request):
#     return render(request, 'daycare/home.html')

# Nueva vista para mostrar la lista de mascotas del usuario logueado - MISMO CÓDIGO
@login_required
def lista_mis_mascotas(request):
    try:
        owner_profile = request.user.owner
        mis_mascotas = owner_profile.pets.all().order_by('nombre')
        return render(request, 'daycare/lista_mis_mascotas.html', {'mis_mascotas': mis_mascotas})
    except Owner.DoesNotExist:
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         return redirect('login')

# Nueva vista para mostrar los detalles de una mascota específica - MISMO CÓDIGO
@login_required
def detalle_mascota(request, pk):
    mascota = get_object_or_404(Pet, pk=pk)

    # Verificar que el usuario logueado es el dueño de esta mascota
    if mascota.owner.user != request.user:
        messages.error(request, 'No tienes permiso para ver los detalles de esta mascota.')
        return redirect('daycare:home') # Redirige a la lista de sus mascotas

    return render(request, 'daycare/detalle_mascota.html', {'mascota': mascota})

# Vista para editar una mascota existente - MODIFICADA para manejo de fotos
@login_required
def editar_mascota(request, pk): # Espera el ID (pk) de la mascota a editar
    # Intenta obtener la mascota por su ID, si no existe, muestra un 404
    mascota = get_object_or_404(Pet, pk=pk)

    # *** Implementar la verificación de dueño ***
    # Es importante que solo el dueño de la mascota pueda editarla
    if mascota.owner.user != request.user:
        messages.error(request, 'No tienes permiso para editar esta mascota.') # Añade un mensaje de error
        return redirect('daycare:home') # Redirige a la lista de sus mascotas

    if request.method == 'POST':
        # Si la petición es POST, procesamos los datos del formulario
        # Instanciamos el formulario CON los datos de la petición (POST, FILES)
        # Y le pasamos la instancia de la mascota que queremos editar (instance=mascota)
        form = PetForm(request.POST, request.FILES, instance=mascota)

        if form.is_valid():
            # --- Lógica para manejar la eliminación de foto ---
            # El widget ClearableFileInput añade un campo oculto de nombre 'campo_name-clear'
            # Si ese campo está en request.POST y su valor es 'on' (o simplemente está presente),
            # Y si el campo original (foto) no tiene un nuevo archivo adjunto en request.FILES,
            # Django entiende que se marcó la casilla "Borrar".
            # form.cleaned_data['foto'] será False en este caso.

            # Verificamos si el campo 'foto' en los datos limpios del formulario es False.
            # Esto ocurre cuando se marcó la casilla "Borrar" y NO se subió una nueva foto.
            if form.cleaned_data.get('foto') is False: # Usar .get() para manejar el caso si el campo no está en el form
                # Si hay una foto existente asociada a esta mascota
                if mascota.foto: # Verifica si el campo foto de la instancia tiene un archivo
                    # Opcional: Eliminar el archivo físico del sistema de archivos
                    # Usa el método delete() del campo FileField/ImageField. Esto también pone el campo a null.
                    try:
                        mascota.foto.delete(save=False) # save=False para no guardar inmediatamente, lo guardará el form.save()
                        messages.info(request, 'Foto anterior eliminada.')
                    except Exception as e:
                        messages.error(request, f'Error al eliminar la foto anterior: {e}')

            # --- Fin Lógica para manejar la eliminación de foto ---

            # form.save() actualizará el objeto mascota.
            # Si se subió una nueva foto (request.FILES contiene 'foto'), form.save() se encargará de borrar la antigua
            # y guardar la nueva.
            # Si se marcó "Borrar" y NO se subió nueva, form.save() establecerá el campo foto a null/vacío
             # (esto ya lo hizo mascota.foto.delete(save=False) si existía foto antes, pero form.save() lo finaliza)
            form.save()

            messages.success(request, f'Los datos de {mascota.nombre} se han actualizado correctamente.')

            # Redirigimos a la página de detalles de la mascota
            return redirect('daycare:detalle_mascota', pk=mascota.pk) # Redirigir a detalles

    else:
        # Si la petición es GET, mostramos el formulario pre-llenado
        form = PetForm(instance=mascota)

    # Renderizamos la plantilla de edición, pasando el formulario y la mascota
    # La plantilla usará 'mascota.foto' para mostrar la imagen actual.
    return render(request, 'daycare/editar_mascota.html', {'form': form, 'mascota': mascota})

# Nueva vista para confirmar y eliminar una mascota - MISMO CÓDIGO
@login_required
def eliminar_mascota(request, pk):
    mascota = get_object_or_404(Pet, pk=pk)

    # *** Implementar la verificación de dueño ***
    if mascota.owner.user != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta mascota.')
        return redirect('daycare:home')

    if request.method == 'POST':
        nombre_mascota = mascota.nombre
        mascota.delete()
        messages.success(request, f'{nombre_mascota} ha sido eliminada correctamente.')
        return redirect('daycare:home')

    return render(request, 'daycare/eliminar_mascota.html', {'mascota': mascota})

# Nueva vista para el registro de un nuevo Dueño (Usuario + Perfil Owner) - MISMO CÓDIGO
# No requiere login
def registro_owner(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"¡Registro exitoso para el usuario '{user.username}'! Por favor, inicia sesión.")
            return redirect('login') # Redirigir a la página de login

    else:
        form = OwnerRegistrationForm()

    return render(request, 'daycare/registro_owner.html', {'form': form})

# Nueva vista para el perfil/panel del Dueño - MISMO CÓDIGO (Obtiene Reservas)
@login_required
def perfil_owner(request):
    try:
        user = request.user
        owner_profile = user.owner

        mis_mascotas = owner_profile.pets.all().order_by('nombre')

        # --- Nuevo: Obtenemos las reservas asociadas a las mascotas de este Owner ---
        mis_reservas = Booking.objects.filter(pet__owner=owner_profile).order_by('date', 'time')

        return render(request, 'daycare/perfil_owner.html', {
            'user': user,
            'owner_profile': owner_profile,
            'mis_mascotas': mis_mascotas,
            'mis_reservas': mis_reservas,
        })
    except Owner.DoesNotExist:
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         return redirect('login')

# Vista para EDITAR el perfil del Dueño logueado - MISMO CÓDIGO (Usa UserOwnerProfileForm)
@login_required
def editar_perfil_owner(request):
    try:
        owner_profile = request.user.owner
        user_instance = request.user
    except Owner.DoesNotExist:
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         return redirect('login')

    if request.method == 'POST':
        form = UserOwnerProfileForm(request.POST, user=user_instance, owner_profile=owner_profile)
        if form.is_valid():
            user_instance, owner_profile = form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('daycare:perfil_owner')

    else:
        form = UserOwnerProfileForm(user=user_instance, owner_profile=owner_profile)

    return render(request, 'daycare/editar_perfil_owner.html', {'form': form, 'owner_profile': owner_profile, 'user': user_instance})

# --- MODIFICAR Vista para que un Dueño pueda solicitar una Reserva (USA EL FORMULARIO MODIFICADO) ---
@login_required # Solo usuarios logueados pueden solicitar reservas
def solicitar_reserva(request):
    # Al instanciar el formulario, le pasamos el usuario logueado para que filtre las mascotas
    # El formulario ahora también incluye el campo 'service' que Django maneja automáticamente.
    if request.method == 'POST':
        # Instanciamos el formulario CON los datos de la petición (request.POST)
        # y pasamos el usuario para filtrar las mascotas
        form = BookingForm(request.POST, user=request.user)

        if form.is_valid():
            # form.save() creará el objeto Booking.
            # Como el formulario ahora incluye 'pet' y 'service', Django validará y asignará
            # automáticamente estos campos al guardar el objeto Booking.
            booking = form.save()

            # Opcional: Mostrar un mensaje de éxito
            # El mensaje ahora puede incluir el nombre del servicio usando booking.service.name
            messages.success(request, f'Solicitud de reserva para {booking.pet.nombre} - {booking.service.name} el {booking.date} a las {booking.time} enviada. Está Pendiente de confirmación.')

            # Redirigir a la página de perfil del usuario o a una página de confirmación de reserva
            return redirect('daycare:perfil_owner') # Redirigir a la página de perfil

    else: # GET request
        # Creamos un formulario vacío para mostrar, pasando el usuario para filtrar las mascotas
        form = BookingForm(user=request.user)

    # Renderizamos la plantilla para solicitar la reserva
    # La plantilla ahora debe renderizar también el campo 'service' del formulario.
    return render(request, 'daycare/solicitar_reserva.html', {'form': form})
# --- FIN MODIFICAR solicitar_reserva ---


# Nueva vista para mostrar los detalles de una reserva específica (lado Dueño) - MISMO CÓDIGO (PENDIENTE ACTUALIZAR PLANTILLA)
@login_required
def detalle_reserva(request, pk):
    reserva = get_object_or_404(Booking, pk=pk)

    # *** Implementar la verificación de dueño ***
    if reserva.pet.owner.user != request.user:
        messages.error(request, 'No tienes permiso para ver los detalles de esta reserva.')
        return HttpResponseForbidden("No tienes permiso para ver los detalles de esta reserva.")

    # Renderiza la plantilla de detalles de reserva (necesita actualizar para mostrar el servicio)
    return render(request, 'daycare/detalle_reserva.html', {'reserva': reserva})

# Nueva vista para CANCELAR una reserva (desde el lado del Dueño) - MISMO CÓDIGO
@login_required
def cancelar_reserva(request, pk):
    # ... Obtener reserva y verificar dueño ...
    reserva = get_object_or_404(Booking, pk=pk)
    if reserva.pet.owner.user != request.user:
        messages.error(request, 'No tienes permiso para cancelar esta reserva.')
        return redirect('daycare:perfil_owner')

    # *** Implementar la verificación de estado (Solo Pendientes) ***
    if reserva.status != 'Pending':
        messages.error(request, f'La reserva para {reserva.pet.nombre} no se puede cancelar porque su estado actual es "{reserva.get_status_display}". Solo se pueden cancelar reservas Pendientes.')
        return redirect('daycare:detalle_reserva', pk=reserva.pk)


    # Si es el dueño y el estado es Pendiente, procesamos la acción
    if request.method == 'POST':
        reserva.status = 'Cancelled'
        reserva.save()
        fecha_formateada = reserva.date.strftime('%d %b %Y')
        # Mensaje de éxito - Opcional: añadir el servicio aquí también
        messages.success(request, f'La reserva para {reserva.pet.nombre} el {fecha_formateada} ha sido cancelada correctamente.')

        return redirect('daycare:perfil_owner')

    # Si la petición es GET, mostramos la página de confirmación
    return render(request, 'daycare/confirmar_cancelacion_reserva.html', {'reserva': reserva})


@login_required # Asegura que solo usuarios logueados puedan ver sus reservas
def mis_reservas(request):
    """
    Vista para mostrar la lista de reservas del dueño autenticado.
    """
    # --- Obtener las reservas del usuario autenticado ---
    # Necesitas filtrar las reservas para que solo pertenezcan al usuario logueado (request.user)
    # ESTO ASUME que tu modelo 'Booking' tiene un campo ForeignKey
    # llamado 'owner' (o similar) que apunta al modelo de usuario (settings.AUTH_USER_MODEL).
    # Si tu modelo de reserva se relaciona con el usuario de otra manera (ej: a través de OwnerProfile),
    # necesitarás ajustar la consulta.
    try:
        # Ejemplo de consulta: Filtra por el campo 'owner' en el modelo Booking
        # Ordena por fecha de inicio de la reserva (o fecha de creación) descendente
        mis_reservas_list = Booking.objects.filter(pet__owner__user=request.user).order_by('-date', '-time') # <-- Consulta corregida
        # Si no tienes fecha_inicio_reserva, puedes ordenar por created_at si lo tienes:
        # mis_reservas_list = Booking.objects.filter(owner=request.user).order_by('-created_at')


    except Exception as e:
        # Manejo de errores simple en caso de que la consulta falle
        print(f"Error al obtener reservas para el usuario {request.user.username}: {e}")
        mis_reservas_list = [] # Devuelve una lista vacía en caso de error


    # --- Preparar el contexto y renderizar la plantilla ---
    context = {
        'mis_reservas': mis_reservas_list, # Pasa la lista de reservas a la plantilla
        # No necesitas pasar 'owner_profile' aquí a menos que la plantilla 'mis_reservas.html' lo use
        # No necesitas pasar 'mis_mascotas' aquí
    }
    return render(request, 'daycare/mis_reservas.html', context)


#---------------------------- Lado del Staff ----------------------------#


# Vista para el listado de Reservas para el Personal (Staff) - CON FILTROS (incluido por Servicio) Y PAGINACIÓN
@login_required
def staff_booking_list(request):
    # *** Implementar la verificación de Staff ***
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('daycare:perfil_owner')

    # Lógica para cambiar el estado de la reserva (si el formulario POST fue enviado) - MISMA LÓGICA
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('new_status')
        if booking_id and new_status:
            reserva = get_object_or_404(Booking, pk=booking_id)
            valid_statuses = [choice[0] for choice in STATUS_CHOICES]
            if new_status in valid_statuses:
                 reserva.status = new_status
                 reserva.save()
                 messages.success(request, f'El estado de la reserva {reserva.pk} ({reserva.pet.nombre}) ha sido cambiado a {reserva.get_status_display()}.')
            else:
                 messages.error(request, f'Estado de reserva "{new_status}" no válido.')

        return redirect('daycare:staff_booking_list')


    # --- Lógica para obtener y aplicar FILTROS (en peticiones GET) ---
    all_bookings = Booking.objects.all() # Iniciar con todas las reservas
    status_filter = request.GET.get('status')
    start_date_filter_str = request.GET.get('start_date')
    # --- Nuevo: Obtener filtro de Servicio ---
    service_filter_id_str = request.GET.get('service') # Obtener el ID del servicio como string de la URL
    service_filter_id = None # Variable para almacenar el ID entero del servicio seleccionado, si es válido

    # --- 1. Filtrar por Estado ---
    if status_filter and status_filter != '':
        valid_statuses = [choice[0] for choice in STATUS_CHOICES]
        if status_filter in valid_statuses:
             all_bookings = all_bookings.filter(status=status_filter)
             # messages.info(request, f'Filtrando por estado: {dict(STATUS_CHOICES).get(status_filter)}')
        else:
             messages.error(request, f'Estado de reserva "{status_filter}" no válido para filtrar.')
             status_filter = '' # Limpiar el filtro inválido para que el selector no muestre una opción incorrecta


    # --- 2. Filtrar por Fecha de Inicio ---
    if start_date_filter_str:
        try:
            start_date_filter = date.fromisoformat(start_date_filter_str)
            all_bookings = all_bookings.filter(date__gte=start_date_filter)
            # messages.info(request, f'Filtrando a partir de la fecha: {start_date_filter_str}')
        except ValueError:
            messages.error(request, f'Formato de fecha de inicio inválido: "{start_date_filter_str}". Usa el formato AAAA-MM-DD.')
            start_date_filter_str = '' # Limpiar el filtro inválido para que el input no muestre el valor incorrecto

    # --- 3. Filtrar por Servicio ---
    if service_filter_id_str and service_filter_id_str != '': # Si se proporcionó un ID de servicio (y no está vacío)
        try:
            # Intentar convertir el string del ID a un entero
            service_filter_id = int(service_filter_id_str)
            # Verificar si existe un servicio con ese ID en la base de datos.
            # Esto es importante para evitar un error de base de datos si el ID no existe.
            # Si Service.objects.get(pk=...) no encuentra el objeto, lanzará ObjectDoesNotExist.
            # Alternativa: all_bookings = all_bookings.filter(service_id=service_filter_id) y manejar ObjectDoesNotExist de la consulta.
            # Verificar antes da un mensaje de error más claro si el ID es válido pero no existe.
            Service.objects.get(pk=service_filter_id) # Lanzará excepción si no existe

            # Si el ID es válido y el servicio existe, aplicar el filtro
            all_bookings = all_bookings.filter(service_id=service_filter_id) # service_id filtra por la clave foránea
            # Opcional: messages.info(request, f'Filtrando por servicio: {Service.objects.get(pk=service_filter_id).name}')

        except ValueError:
            # Si el string del ID no se puede convertir a un entero (ej: service=abc)
            messages.error(request, f'ID de servicio "{service_filter_id_str}" no válido (debe ser un número).')
            service_filter_id = None # Limpiar filtro inválido
        except ObjectDoesNotExist:
            # Si el ID entero no corresponde a ningún servicio existente (ej: service=9999)
            messages.error(request, f'No existe un servicio con ID "{service_filter_id_str}".')
            service_filter_id = None # Limpiar filtro inválido


    # --- Aplicar Ordenamiento Final ---
    all_bookings = all_bookings.order_by('date', 'time')


    # --- Lógica de PAGINACIÓN ---
    items_per_page = 10
    paginator = Paginator(all_bookings, items_per_page)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    # --- Preparar el contexto para la plantilla ---
    context = {
        'page_obj': page_obj, # Contiene los elementos de la página actual y la info de paginación
        # Pasamos los valores de los filtros aplicados para pre-llenar el formulario de filtro en la plantilla
        'status_filter': status_filter,
        'start_date_filter_str': start_date_filter_str,
        'service_filter_id': service_filter_id, # <-- Pasar el ID entero del filtro de servicio aplicado (o None)
        'status_choices': STATUS_CHOICES, # Las opciones de estado del modelo para el selector de filtro
        # --- Nuevo: Pasar todos los Servicios para el selector de filtro ---
        'services': Service.objects.all().order_by('name'), # <-- Pasar TODOS los objetos Service para popular el selector
        # --- Fin Nuevo ---

        'status_change_form': ChangeBookingStatusForm(), # Instancia vacía del form de cambio de estado (para cada fila)
    }


    return render(request, 'daycare/staff_booking_list.html', context)

# Vista para ver y editar detalles de Reserva para el Personal (Staff) - MISMO CÓDIGO (PENDIENTE ACTUALIZAR PLANTILLA)
@login_required # Solo usuarios logueados
def staff_booking_detail(request, pk): # Espera el ID (pk) de la reserva
    # *** Implementar la verificación de Staff ***
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('daycare:perfil_owner')

    # Obtener la reserva específica o devolver 404
    reserva = get_object_or_404(Booking, pk=pk)

    # Manejar el envío del formulario de notas internas (si es POST)
    if request.method == 'POST':
        form = StaffNotesForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notas internas actualizadas correctamente.')
            return redirect('daycare:staff_booking_detail', pk=reserva.pk)

    # Manejar petición GET (mostrar detalles y formulario pre-llenado)
    else:
        form = StaffNotesForm(instance=reserva)


    # Renderizar la plantilla de detalles de staff (necesita actualizar para mostrar el servicio y notas del dueño)
    context = {
        'reserva': reserva,
        'staff_notes_form': form,
    }
    return render(request, 'daycare/staff_booking_detail.html', context)

class CustomLoginView(LoginView):
    """
    Vista de login personalizada que redirige al staff a una URL diferente.
    """
    # template_name = 'registration/login.html' # Tu plantilla de login si tienes una


    def setup(self, request, *args, **kwargs):
         print("--- DEBUG: CustomLoginView setup ejecutado ---") # Añade esta línea
         super().setup(request, *args, **kwargs)

    # O también podrías añadirla en dispatch (el método que se ejecuta antes de setup)
    # def dispatch(self, request, *args, **kwargs):
    #     print("--- DEBUG: CustomLoginView dispatch ejecutado ---") # Añade esta línea
    #     return super().dispatch(request, *args, **kwargs)


    def get_redirect_url(self):
        """
        Sobrescribe este método para redirigir al staff a LOGIN_REDIRECT_URL_STAFF
        y a otros usuarios a la URL por defecto (LOGIN_REDIRECT_URL o 'next').
        """
        print("--- DEBUG: get_redirect_url ejecutado ---") # Añade esta línea

        url = super().get_redirect_url() # Obtiene URL por defecto

        print(f"--- DEBUG: Usuario autenticado: {self.request.user.is_authenticated} ---") # Añade esta línea
        if self.request.user.is_authenticated:
             print(f"--- DEBUG: Usuario es staff: {self.request.user.is_staff} ---") # Añade esta línea
             # Verifica si el usuario autenticado es staff
             if self.request.user.is_staff:
                 print("--- DEBUG: Usuario es staff. Intentando redirigir a staff URL. ---") # Añade esta línea
                 # Si es staff, sobrescribe la URL de redirección con la URL específica para staff
                 if hasattr(settings, 'LOGIN_REDIRECT_URL_STAFF'):
                      staff_url = settings.LOGIN_REDIRECT_URL_STAFF
                      print(f"--- DEBUG: Redirigiendo staff a (settings): {staff_url} ---") # Añade esta línea
                      url = staff_url
                 else:
                      # Fallback si no se definió LOGIN_REDIRECT_URL_STAFF (no debería pasar si lo añadiste)
                      fallback_url = reverse_lazy('daycare:staff_booking_list')
                      print(f"--- DEBUG: LOGIN_REDIRECT_URL_STAFF no definida. Redirigiendo staff a (fallback): {fallback_url} ---") # Añade esta línea
                      url = fallback_url
             else:
                  print(f"--- DEBUG: Usuario NO es staff. Redirigiendo a URL por defecto: {url} ---") # Añade esta línea
        else:
             print("--- DEBUG: Usuario NO está autenticado (inesperado después de login exitoso). ---") # Añade esta línea


        print(f"--- DEBUG: get_redirect_url finaliza. URL devuelta: {url} ---") # Añade esta línea
        return url