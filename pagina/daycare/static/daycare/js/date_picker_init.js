// pagina/daycare/static/daycare/js/date_picker_init.js

// Asegura que el DOM esté completamente cargado antes de ejecutar el código principal.
// Esto previene errores al intentar acceder a elementos HTML que aún no existen.
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente cargado. Inicializando scripts.");

    // --- JavaScript para inicializar Flatpickr ---
    // Este código se ejecutará SOLAMENTE si el elemento con el ID correspondiente existe en la página actual.

    // Intentar inicializar Flatpickr en el campo de fecha de RESERVA si existe (su ID es típicamente 'id_date')
    const dateInputBooking = document.getElementById('id_date');
    if (dateInputBooking) { // Si encontramos el elemento con ID 'id_date'
        console.log("Elemento para fecha de reserva (#id_date) encontrado. Inicializando Flatpickr.");
        flatpickr(dateInputBooking, {
            enableTime: false, // Desactivar selector de hora si no se usa
            dateFormat: "Y-m-d", // Asegurar el formato esperado por Django DateField
            minDate: "today", // Opcional: Evitar seleccionar fechas pasadas
            locale: "es" // Opcional: Usar localización en español si has cargado el archivo l10n/es.js
        });
    } else {
        // Este mensaje es esperado en páginas donde NO hay un campo con ID 'id_date' (como la edición de mascota)
        console.log("Elemento para fecha de reserva (#id_date) NO encontrado. Flatpickr no inicializado en este campo (Esperado en esta página).");
    }

    // Opcional: Inicializar Flatpickr en otro campo de fecha si existe en la página actual
    // Por ejemplo, el campo de fecha de nacimiento en la página de edición de mascota (su ID es probablemente 'id_fecha_nacimiento')
    const dateInputPetBirth = document.getElementById('id_fecha_nacimiento');
    if (dateInputPetBirth) { // Si encontramos el elemento con ID 'id_fecha_nacimiento'
        console.log("Elemento para fecha de nacimiento (#id_fecha_nacimiento) encontrado. Inicializando Flatpickr.");
         flatpickr(dateInputPetBirth, {
             enableTime: false,
             dateFormat: "Y-m-d",
             // Opcional: Puedes añadir maxDate: "today" aquí si es una fecha de nacimiento para evitar fechas futuras
             // maxDate: "today",
             locale: "es" // Opcional: Usar localización en español
         });
    } else {
         // Este mensaje es esperado si la mascota no tiene campo de fecha de nacimiento, o su ID es diferente
         console.log("Elemento para fecha de nacimiento (#id_fecha_nacimiento) NO encontrado (Puede ser esperado).");
    }
    // --- Fin JavaScript Flatpickr ---


    // --- JavaScript para Vista Previa de Subida de Foto ---
    console.log("Intentando configurar vista previa de foto...");
    const photoInput = document.getElementById('id_foto'); // ID estándar del input de archivo 'foto'
    const photoPreview = document.getElementById('photo-preview'); // ID del elemento <img> de vista previa
    // Declarar existingPhotoSection una vez al principio de esta sección relevante
    const existingPhotoSection = document.getElementById('existing-photo-section'); // ID del div que envuelve la foto actual

    console.log("Input foto (#id_foto) encontrado:", photoInput);
    console.log("Preview img (#photo-preview) encontrado:", photoPreview);
    console.log("Sección foto actual (#existing-photo-section) encontrada:", existingPhotoSection);


    // Proceder con la lógica de vista previa SOLO si encontramos el input de archivo y el placeholder de vista previa
    if (photoInput && photoPreview) {
        console.log("Elementos para vista previa encontrados. Añadiendo listener 'change' al input foto.");
        photoInput.addEventListener('change', function(event) {
            console.log("'change' event disparado en input foto.");
            const file = event.target.files[0]; // Obtener el primer archivo seleccionado

            // Verificar si se seleccionó un archivo y si es una imagen
            if (file && file.type.startsWith('image/')) {
                 console.log("Archivo de imagen seleccionado:", file.name);
                const reader = new FileReader(); // Objeto para leer el contenido del archivo

                reader.onload = function(e) { // Función que se ejecuta cuando la lectura termina
                     console.log("FileReader cargado. Mostrando vista previa.");
                    photoPreview.src = e.target.result; // Establecer la fuente de la vista previa
                    photoPreview.style.display = 'block'; // Mostrar la vista previa

                    // Ocultar la sección de la foto actual cuando se muestra una nueva vista previa
                    if (existingPhotoSection) { // La sección de foto actual solo existe si la mascota tiene foto
                        existingPhotoSection.style.display = 'none';
                         console.log("Ocultando sección foto actual.");
                    }
                };
                reader.readAsDataURL(file); // Leer el archivo como una URL de datos (base64)

            } else { // Si no se selecciona archivo o no es imagen
                console.log("Ningún archivo seleccionado o no es imagen.");
                photoPreview.src = '#'; // Limpiar la fuente de la vista previa
                photoPreview.style.display = 'none'; // Ocultar la vista previa

                // Si se cancela la selección de archivo, volver a mostrar la foto actual si existía
                 if (existingPhotoSection) {
                      existingPhotoSection.style.display = 'block';
                      console.log("Mostrando sección foto actual de nuevo.");
                  }
            }
        });
    } else {
         // Este warning es esperado en páginas donde no hay campo de foto o el placeholder de vista previa #photo-preview
         console.warn("Elementos para vista previa de foto (input#id_foto o img#photo-preview) no encontrados. La funcionalidad de vista previa no estará activa. (Puede ser esperado)");
    }
    // --- Fin JavaScript para Vista Previa de Subida de Foto ---


    // --- JavaScript para Botón Personalizado de Eliminar Foto ---
    console.log("Intentando configurar botón de eliminar foto personalizado...");
    const deleteButton = document.getElementById('delete-photo-button');
    // CORRECCIÓN: Usar el ID correcto para la casilla 'Limpiar' que nos proporcionaste
    const clearCheckbox = document.getElementById('foto-clear_id'); // <-- ¡ID CORREGIDO AQUÍ!
    // Reutilizamos la variable existingPhotoSection declarada arriba


    // La lógica de eliminar solo aplica si hay una foto existente.
    // El botón 'delete-photo-button' y el div 'existing-photo-section'
    // solo se renderizan en la plantilla si mascota.foto existe (gracias a tu {% if mascota.foto %}).
    // La casilla 'clearCheckbox' (#foto-clear_id) solo se renderiza si mascota.foto existe Y form.foto no se renderiza manualmente.
    // Por lo tanto, si encontramos deleteButton y clearCheckbox, deberíamos encontrar también existingPhotoSection.
    // Aseguramos que los TRES elementos necesarios para la eliminación visual existan antes de configurar el listener
    if (deleteButton && clearCheckbox && existingPhotoSection) {
        console.log("Elementos para botón eliminar foto personalizado encontrados. Añadiendo listener de click a #delete-photo-button.");

        deleteButton.addEventListener('click', function() {
            console.log("Botón 'Eliminar Foto' clickeado.");

            // Opcional: Mostrar un cuadro de diálogo de confirmación
            const confirmDelete = confirm("¿Estás seguro de que quieres eliminar la foto de la mascota?");
            console.log("Confirmación eliminar:", confirmDelete);

            if (confirmDelete) {
                console.log("Confirmado. Marcando casilla 'Limpiar' oculta y ocultando elementos visualmente.");
                // ¡La clave! Marcar la casilla 'Limpiar' oculta programáticamente.
                // Cuando el formulario se envíe, Django verá que esta casilla está marcada
                // y entenderá que se debe eliminar la foto asociada.
                clearCheckbox.checked = true;

                // Dar Feedback Visual al Usuario en la interfaz
                // Ocultar la sección de la foto actual (que contiene la img y el botón eliminar)
                // Ya verificamos que existingPhotoSection existe en el if principal
                existingPhotoSection.style.display = 'none'; // Ocultar el div que contiene la foto y el botón

                // Opcional: Mostrar un mensaje visual en la página (ej: "Foto marcada para eliminar. Guarda los cambios.")
                // Puedes tener un elemento <p id="delete-message" style="display:none;">...</p> en la plantilla
                // y hacerlo visible aquí si lo necesitas:
                // const deleteMessageElement = document.getElementById('delete-message');
                // if (deleteMessageElement) {
                //     deleteMessageElement.textContent = "La foto será eliminada al guardar."; // O el mensaje que quieras
                //     deleteMessageElement.style.display = 'block';
                // }

                console.log("Foto marcada para eliminar visualmente. Recuerda guardar el formulario.");
            } else {
                 console.log("Eliminación cancelada por el usuario.");
            }
        });
    } else {
        // Este warning es esperado si la mascota no tiene foto (deleteButton no se renderiza)
        // o si el div #existing-photo-section no fue añadido correctamente a la plantilla.
        // Si la mascota SÍ tiene foto pero ves este warning, revisa los IDs y la estructura HTML en tu plantilla.
        console.warn("Elementos para botón de eliminar foto personalizado no encontrados (botón#delete-photo-button, casilla#foto-clear_id, o div#existing-photo-section). La funcionalidad de eliminar visualmente no estará activa. (Puede ser esperado si la mascota no tiene foto)");
    }

    // --- Fin JavaScript para Botón Personalizado de Eliminar Foto ---

}); // --- Fin del listener DOMContentLoaded ---

// --- Cualquier otra función o código que DEBA estar fuera del listener DOMContentLoaded iría aquí ---
// (Normalmente, la mayoría del código que interactúa con el DOM debe estar dentro del listener)