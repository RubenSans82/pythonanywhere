# pagina/daycare/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Owner, Pet, Booking # Asegúrate de importar Booking
from .forms import PetForm, OwnerRegistrationForm, BookingForm, ChangeBookingStatusForm, OwnerProfileForm, UserOwnerProfileForm # Importar el nuevo formulario
from django.http import HttpResponseForbidden
# Importar timezone y Q si necesitas filtrar por fecha o estado combinado en la vista
# from django.utils import timezone
# from django.db.models import Q
from django import forms  # Importar el módulo forms de Django

# Nueva vista para agregar una mascota
@login_required # Este decorador asegura que solo usuarios autenticados puedan acceder a esta vista
def agregar_mascota(request):
    # Intentamos obtener el perfil de Owner asociado al usuario logueado
    # Si el usuario logueado no tiene un perfil Owner, esto podría fallar.
    # Asumimos por ahora que todo usuario logueado que llegue aquí tiene un perfil Owner.
    # Una implementación más robusta manejaría este caso (ej: redirigir a crear perfil).
    try:
        owner_profile = request.user.owner # Accedemos al Owner a través de la relación OneToOne
    except Owner.DoesNotExist:
         # Si el usuario no tiene perfil Owner (esto no debería pasar si creaste Owners en admin),
         # podrías redirigirlo o mostrar un error. Por ahora, mostraremos un mensaje simple.
         # Considera redirigir a una página de error o a la creación de perfil Owner si implementas eso.
         return render(request, 'daycare/error_no_owner_profile.html', {'mensaje': 'Tu cuenta de usuario no tiene un perfil de Dueño asociado.'})


    if request.method == 'POST':
        # Si la petición es POST, significa que se envió el formulario
        # Instanciamos el formulario con los datos de la petición (request.POST)
        # y los archivos subidos (request.FILES), ¡fundamental para las fotos!
        form = PetForm(request.POST, request.FILES)

        # Verificamos si el formulario es válido (si los datos cumplen las validaciones del modelo/formulario)
        if form.is_valid():
            # No guardamos el objeto Pet directamente todavía (commit=False)
            # porque necesitamos asignarle el dueño antes de guardar
            mascota = form.save(commit=False)

            # Asignamos el dueño de la mascota al perfil del usuario logueado
            mascota.owner = owner_profile

            # Ahora sí, guardamos la mascota (esto incluye guardar el archivo de la foto)
            mascota.save()

            # Opcional: Guardar relaciones ManyToMany si el modelo Pet las tuviera y estuvieran en el formulario
            # form.save_m2m()

            # Redirigimos a una página de éxito o al perfil del usuario/lista de sus mascotas
            # Todavía no tenemos la URL para esto, usaremos una URL placeholder por ahora.
            # Deberías cambiar 'nombre_url_perfil_usuario' por el nombre de una URL real de tu proyecto.
            # Por ahora, redirigimos a la raíz o a /admin/ para verificar que se creó.
            # return redirect('nombre_url_perfil_usuario') # <- Idealmente, una URL del usuario

            # Opción temporal: redirigir a la página de administración para ver la mascota creada
            # return redirect('/admin/') # <- Temporal para verificar

            # Opción temporal: redirigir a la raíz
            return redirect('/') # <- Opción simple por ahora

    else:
        # Si la petición es GET (es decir, el usuario simplemente visitó la página)
        # Creamos un formulario vacío para mostrarlo
        form = PetForm()

    # Renderizamos la plantilla 'daycare/agregar_mascota.html'
    # y le pasamos el formulario para que se muestre en el HTML
    return render(request, 'daycare/agregar_mascota.html', {'form': form})

# Nueva vista para la página de inicio
def home_page(request):
    # Simplemente renderiza una plantilla llamada 'daycare/home.html'
    return render(request, 'daycare/home.html')

# Nueva vista para mostrar la lista de mascotas del usuario logueado
@login_required
def lista_mis_mascotas(request):
    try: # <--- INICIO BLOQUE TRY
        # Intentamos obtener el perfil de Owner asociado al usuario logueado
        owner_profile = request.user.owner
        # Si el try fue exitoso, continuamos con la lógica original
        # Recuperamos las mascotas asociadas a este Owner
        mis_mascotas = owner_profile.pets.all().order_by('nombre')

        # Renderizamos la plantilla
        return render(request, 'daycare/lista_mis_mascotas.html', {'mis_mascotas': mis_mascotas})

    except Owner.DoesNotExist: # <--- INICIO BLOQUE EXCEPT
         # Si el usuario logueado no tiene perfil Owner
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         # Redirigir a una página segura, como el login.
         return redirect('login') # <--- Redirige al login
    # <--- FIN BLOQUE EXCEPT

# Nueva vista para mostrar los detalles de una mascota específica
@login_required # Solo usuarios logueados pueden ver detalles de mascotas (asumimos que son sus propias mascotas o de guardería)
def detalle_mascota(request, pk): # Esta vista espera recibir el ID (pk) de la mascota
    # Intenta obtener la mascota con el ID (pk) dado
    # get_object_or_404 mostrará un error 404 si no encuentra la mascota
    mascota = get_object_or_404(Pet, pk=pk)

    # Opcional: Verificar que el usuario logueado es el dueño de esta mascota
    # Esto es importante si quieres que los usuarios solo vean los detalles de sus propias mascotas
    # if mascota.owner.user != request.user:
    #     # Si no es el dueño, podrías redirigir o mostrar un error 403 (Prohibido)
    #     from django.http import HttpResponseForbidden
    #     return HttpResponseForbidden("No tienes permiso para ver los detalles de esta mascota.")
        # O redirigir a la lista de sus propias mascotas:
        # return redirect('daycare:home') # O la URL de lista_mis_mascotas

    # Renderiza la plantilla 'daycare/detalle_mascota.html' y le pasa el objeto mascota
    return render(request, 'daycare/detalle_mascota.html', {'mascota': mascota})

# Nueva vista para editar una mascota existente
@login_required
def editar_mascota(request, pk): # Espera el ID (pk) de la mascota a editar
    # Intenta obtener la mascota por su ID, si no existe, muestra un 404
    mascota = get_object_or_404(Pet, pk=pk)

    # *** Implementar la verificación de dueño ***
    # Es importante que solo el dueño de la mascota pueda editarla
    if mascota.owner.user != request.user:
        # Si el usuario logueado NO es el dueño de esta mascota
        messages.error(request, 'No tienes permiso para editar esta mascota.') # Añade un mensaje de error
        return redirect('daycare:home') # Redirige a la lista de sus mascotas

    if request.method == 'POST':
        # Si la petición es POST, procesamos los datos del formulario
        # Instanciamos el formulario CON los datos de la petición (POST, FILES)
        # Y lo más importante, le pasamos la instancia de la mascota que queremos editar (instance=mascota)
        form = PetForm(request.POST, request.FILES, instance=mascota)

        if form.is_valid():
            # Si el formulario es válido, simplemente llamamos a form.save()
            # Como pasamos la instancia 'mascota', Django actualizará ESE objeto en lugar de crear uno nuevo
            form.save()

            # Opcional: Mostrar un mensaje de éxito
            messages.success(request, f'Los datos de {mascota.nombre} se han actualizado correctamente.')

            # Redirigimos a la página de detalles de la mascota o a la lista de mascotas
            # return redirect('daycare:detalle_mascota', pk=mascota.pk) # Redirigir a detalles
            return redirect('daycare:home') # Redirigir a la lista de mascotas

    else:
        # Si la petición es GET, mostramos el formulario pre-llenado
        # Instanciamos el formulario pasándole la instancia de la mascota
        form = PetForm(instance=mascota)

    # Renderizamos la plantilla de edición, pasando el formulario y la mascota
    return render(request, 'daycare/editar_mascota.html', {'form': form, 'mascota': mascota})

# Nueva vista para confirmar y eliminar una mascota
@login_required
def eliminar_mascota(request, pk): # Espera el ID (pk) de la mascota a eliminar
    # Intenta obtener la mascota por su ID
    mascota = get_object_or_404(Pet, pk=pk)

    # *** Implementar la verificación de dueño ***
    # Es importante que solo el dueño de la mascota pueda eliminarla
    if mascota.owner.user != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta mascota.')
        return redirect('daycare:home') # Redirige a la lista de sus mascotas

    if request.method == 'POST':
        # Si la petición es POST (el usuario confirmó en el formulario de la plantilla)
        nombre_mascota = mascota.nombre # Guardamos el nombre antes de eliminar
        mascota.delete() # Elimina el objeto de la base de datos

        messages.success(request, f'{nombre_mascota} ha sido eliminada correctamente.')

        # Redirige a la lista de mascotas del usuario
        return redirect('daycare:home')

    # Si la petición es GET, simplemente mostramos la página de confirmación
    return render(request, 'daycare/eliminar_mascota.html', {'mascota': mascota})

# Nueva vista para el registro de un nuevo Dueño (Usuario + Perfil Owner)
def registro_owner(request):
    if request.method == 'POST':
        # Si la petición es POST, procesamos el formulario enviado
        form = OwnerRegistrationForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, llamamos a form.save()
            # Nuestro método save() personalizado en el formulario crea el User Y el Owner
            user = form.save()

            # Opcional: Autologin del usuario después del registro (requiere importar login)
            # from django.contrib.auth import login
            # login(request, user)
            # messages.success(request, f"¡Registro exitoso! Bienvenido, {user.username}.")
            # return redirect('daycare:home') # Redirigir a la página principal o dashboard

            # Mostrar mensaje de éxito y redirigir a la página de login
            messages.success(request, f"¡Registro exitoso para el usuario '{user.username}'! Por favor, inicia sesión.")
            # 'login' es el nombre de URL de la vista de login de Django auth
            return redirect('login') # Redirigir a la página de login

    else:
        # Si la petición es GET, mostramos un formulario vacío
        form = OwnerRegistrationForm()

    # Renderizamos la plantilla de registro, pasándole el formulario
    return render(request, 'daycare/registro_owner.html', {'form': form})

# Nueva vista para el perfil/panel del Dueño
@login_required
def perfil_owner(request):
    # Esta vista asume que el usuario logueado tiene un perfil Owner.
    # Si no lo tiene, request.user.owner lanzará RelatedObjectDoesNotExist.
    # Añadiremos manejo de este error para evitar el crash.
    try: # <--- INICIO BLOQUE TRY
        user = request.user
        owner_profile = user.owner # Accedemos al perfil Owner asociado al usuario
        # Obtenemos las mascotas asociadas a este Owner
        mis_mascotas = owner_profile.pets.all().order_by('nombre')

        # Renderizamos la plantilla del perfil
        return render(request, 'daycare/perfil_owner.html', {
            'user': user,
            'owner_profile': owner_profile,
            'mis_mascotas': mis_mascotas
        })

    except Owner.DoesNotExist: # <--- INICIO BLOQUE EXCEPT
         # Si el usuario logueado no tiene perfil Owner
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         # Redirigir a una página segura, como el login.
         return redirect('login') # <--- Redirige al login
    # <--- FIN BLOQUE EXCEPT

# Vista para EDITAR el perfil del Dueño logueado (ahora incluye campos de User y Owner)
@login_required # Solo usuarios logueados pueden editar su perfil
def editar_perfil_owner(request):
    try:
        # Intentamos obtener el perfil de Owner asociado al usuario logueado
        # Necesitamos owner_profile para pasarlo al formulario y para el manejo de error
        owner_profile = request.user.owner
        # También necesitamos el objeto User directamente para pasarlo al formulario
        user_instance = request.user
    except Owner.DoesNotExist:
         # Si el usuario logueado no tiene perfil Owner (esto no debería pasar si se registraron via frontend o se les creó en admin),
         # redirigimos a una página segura.
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         return redirect('login') # Redirige al login o a la página principal


    # Si el try fue exitoso, tenemos user_instance y owner_profile
    if request.method == 'POST':
        # Si la petición es POST, procesamos los datos del formulario enviado
        # --- MODIFICAR INSTANCIACIÓN DEL FORMULARIO ---
        # Instanciamos el nuevo formulario UserOwnerProfileForm
        # Le pasamos los datos de la petición (request.POST)
        # Y las instancias de user_instance y owner_profile para que las actualice
        form = UserOwnerProfileForm(request.POST, user=user_instance, owner_profile=owner_profile) # Pasar user y owner_profile
        # --- Fin MODIFICAR INSTANCIACIÓN ---

        if form.is_valid():
            # Si el formulario es válido, llamamos a su método save() personalizado
            # Este método que definimos en el formulario guardará los cambios en AMBAS instancias (User y OwnerProfile)
            user_instance, owner_profile = form.save() # Nuestro save() devuelve las instancias actualizadas (opcional usar el retorno aquí)

            # Opcional: Mostrar un mensaje de éxito
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')

            # Redirigimos de vuelta a la página de perfil
            return redirect('daycare:perfil_owner')

    else: # GET request
        # Si la petición es GET (el usuario visitó la página de edición)
        # Mostramos el formulario pre-llenado con los datos actuales
        # --- MODIFICAR INSTANCIACIÓN DEL FORMULARIO ---
        # Instanciamos el nuevo formulario UserOwnerProfileForm
        # Le pasamos las instancias de user_instance y owner_profile para pre-llenar los campos con los datos actuales
        form = UserOwnerProfileForm(user=user_instance, owner_profile=owner_profile) # Pasar user y owner_profile
        # --- Fin MODIFICAR INSTANCIACIÓN ---


    # Renderizamos la plantilla de edición, pasando el formulario y las instancias
    # Pasamos user y owner_profile para que la plantilla pueda acceder a ellos si es necesario
    return render(request, 'daycare/editar_perfil_owner.html', {'form': form, 'owner_profile': owner_profile, 'user': user_instance}) # Pasamos user y owner_profile


# Nueva vista para que un Dueño pueda solicitar una Reserva
@login_required # Solo usuarios logueados pueden solicitar reservas
def solicitar_reserva(request):
    # Al instanciar el formulario, le pasamos el usuario logueado para que filtre las mascotas
    # En el método POST, pasamos request.POST para los datos del formulario
    # En el método GET (else), no pasamos datos, solo el usuario
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user) # Pasar user aquí también es crucial

        if form.is_valid():
            # form.save() creará el objeto Booking.
            # Como el campo 'pet' ya está validado por el formulario (y filtrado por el dueño),
            # y el estado por defecto es 'Pending', no necesitamos commit=False aquí.
            booking = form.save()

            # Opcional: Mostrar un mensaje de éxito
            messages.success(request, f'Solicitud de reserva para {booking.pet.nombre} el {booking.date} a las {booking.time} enviada. Está Pendiente de confirmación.')

            # Redirigir a la página de perfil del usuario o a una página de confirmación de reserva
            # Usaremos la página de perfil por ahora, ya que muestra las mascotas y podríamos añadir reservas futuras allí.
            return redirect('daycare:perfil_owner') # Redirigir a la página de perfil

    else: # GET request
        # Creamos un formulario vacío para mostrar
        form = BookingForm(user=request.user) # Pasar el usuario es esencial en GET para filtrar el select de mascotas

    # Renderizamos la plantilla para solicitar la reserva
    return render(request, 'daycare/solicitar_reserva.html', {'form': form})

# Vista para el perfil/panel del Dueño (Añadimos reservas)
@login_required
def perfil_owner(request):
    try:
        user = request.user
        owner_profile = user.owner # Accedemos al perfil Owner asociado al usuario

        # Obtenemos las mascotas asociadas a este Owner
        mis_mascotas = owner_profile.pets.all().order_by('nombre')

        # --- Nuevo: Obtenemos las reservas asociadas a las mascotas de este Owner ---
        # Podemos filtrar las reservas donde la mascota pertenezca a este owner_profile
        # Booking está relacionado con Pet, y Pet con Owner.
        # Podemos usar la sintaxis de doble guion bajo '__' para "cruzar" relaciones en el filtro.
        mis_reservas = Booking.objects.filter(pet__owner=owner_profile).order_by('date', 'time') # Ordenar por fecha y hora

        # Puedes añadir filtrado adicional aquí si quieres, ej: .exclude(status='Completed') para no mostrar completadas


        # Renderizamos la plantilla del perfil, pasando el usuario, el perfil Owner, sus mascotas Y sus reservas
        return render(request, 'daycare/perfil_owner.html', {
            'user': user,
            'owner_profile': owner_profile,
            'mis_mascotas': mis_mascotas,
            'mis_reservas': mis_reservas, # <--- Pasar la lista de reservas a la plantilla
        })

    except Owner.DoesNotExist:
         messages.error(request, 'Tu cuenta de usuario no tiene un perfil de Dueño asociado. Por favor, usa una cuenta con perfil de dueño o contacta al administrador.')
         return redirect('login') # Redirige al login
    
    # Nueva vista para mostrar los detalles de una reserva específica
@login_required # Solo usuarios logueados pueden ver detalles de reserva
def detalle_reserva(request, pk): # Espera el ID (pk) de la reserva
    # Intenta obtener la reserva por su ID, si no existe, muestra un 404
    reserva = get_object_or_404(Booking, pk=pk)

    # *** Implementar la verificación de dueño ***
    # Es importante que solo el dueño de la mascota asociada a la reserva pueda verla
    # Accedemos al usuario del dueño a través de la relación reserva -> mascota -> dueño -> usuario
    if reserva.pet.owner.user != request.user:
        # Si el usuario logueado NO es el dueño de la mascota de esta reserva
        messages.error(request, 'No tienes permiso para ver los detalles de esta reserva.') # Mensaje de error
        # Redirigir a una página segura, como la lista de sus reservas (perfil), o mostrar un 403
        # return redirect('daycare:perfil_owner')
        return HttpResponseForbidden("No tienes permiso para ver los detalles de esta reserva.") # Muestra un error 403


    # Si el usuario es el dueño, renderizamos la plantilla de detalles de reserva
    return render(request, 'daycare/detalle_reserva.html', {'reserva': reserva})

# Nueva vista para CANCELAR una reserva (desde el lado del Dueño)
@login_required # Solo usuarios logueados pueden cancelar reservas
def cancelar_reserva(request, pk): # Espera el ID (pk) de la reserva a cancelar
    # Intenta obtener la reserva por su ID, si no existe, muestra un 404
    reserva = get_object_or_404(Booking, pk=pk)

    # *** Implementar la verificación de dueño ***
    # Es importante que solo el dueño pueda cancelar su propia reserva
    if reserva.pet.owner.user != request.user:
        messages.error(request, 'No tienes permiso para cancelar esta reserva.')
        # Redirigir a una página segura, como la lista de sus reservas (perfil)
        return redirect('daycare:perfil_owner') # Redirige al perfil del dueño

    # *** Implementar la verificación de estado ***
    # Solo se pueden cancelar reservas que están Pendientes
    if reserva.status != 'Pending':
        messages.error(request, f'La reserva para {reserva.pet.nombre} no se puede cancelar porque su estado actual es "{reserva.get_status_display}". Solo se pueden cancelar reservas Pendientes.')
        # Redirigir de vuelta a los detalles de la reserva
        return redirect('daycare:detalle_reserva', pk=reserva.pk)


    # Si es el dueño y el estado es Pendiente, procesamos la acción
    if request.method == 'POST':
        # Si la petición es POST (el usuario confirmó la cancelación en la plantilla de confirmación)
        reserva.status = 'Cancelled' # Cambiamos el estado a Cancelada
        reserva.save() # Guardamos el cambio en la base de datos
        
        fecha_formateada = reserva.date.strftime('%d %b %Y')
        messages.success(request, f'La reserva para {reserva.pet.nombre} el {fecha_formateada} ha sido cancelada correctamente.')

        # Redirigimos a la lista de reservas del usuario (página de perfil)
        return redirect('daycare:perfil_owner')

    # Si la petición es GET, mostramos la página de confirmación
    return render(request, 'daycare/confirmar_cancelacion_reserva.html', {'reserva': reserva})


#---------------------------- Lado del Staff ----------------------------#


# Nueva vista para el listado de Reservas para el Personal (Staff)
# Esta vista solo es accesible para usuarios logueados Y que sean staff
@login_required # Requiere que el usuario esté logueado
def staff_booking_list(request):
    # *** Implementar la verificación de Staff ***
    # Si el usuario logueado NO es staff, le negamos el acceso
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('daycare:perfil_owner') # Redirige a una página segura para usuarios normales (ej: su perfil)

    # Obtener todas las reservas para que el staff las vea
    # Puedes filtrar aquí si prefieres (ej: solo pendientes, solo futuras, etc.)
    # Para empezar, mostramos todas, ordenadas por fecha y hora
    all_bookings = Booking.objects.all().order_by('date', 'time')

    # Renderizar la plantilla del staff, pasando la lista de reservas
    return render(request, 'daycare/staff_booking_list.html', {'all_bookings': all_bookings})

# Nueva vista para el listado de Reservas para el Personal (Staff)
# Esta vista solo es accesible para usuarios logueados Y que sean staff
@login_required # Requiere que el usuario esté logueado
def staff_booking_list(request):
    # *** Implementar la verificación de Staff ***
    # Si el usuario logueado NO es staff, le negamos el acceso
    if not request.user.is_staff:
        messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('daycare:perfil_owner') # Redirige a una página segura para usuarios normales (ej: su perfil)

    # Lógica para cambiar el estado de la reserva (si el formulario fue enviado)
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')  # Obtiene el ID de la reserva del formulario
        new_status = request.POST.get('new_status')  # Obtiene el nuevo estado seleccionado
        if booking_id and new_status:
            reserva = get_object_or_404(Booking, pk=booking_id)  # Obtiene la reserva o devuelve 404
            reserva.status = new_status  # Actualiza el estado
            reserva.save()  # Guarda los cambios
            messages.success(request, f'El estado de la reserva {reserva.pk} ha sido cambiado a {reserva.get_status_display()}.')  # Mensaje de éxito

    # Obtener todas las reservas para que el staff las vea
    # Puedes filtrar aquí si prefieres (ej: solo pendientes, solo futuras, etc.)
    # Para empezar, mostramos todas, ordenadas por fecha y hora
    all_bookings = Booking.objects.all().order_by('date', 'time')



    # Crear una instancia del formulario para cada reserva
    form = ChangeBookingStatusForm()

    # Renderizar la plantilla del staff, pasando la lista de reservas Y el formulario
    return render(request, 'daycare/staff_booking_list.html', {'all_bookings': all_bookings, 'form': form})