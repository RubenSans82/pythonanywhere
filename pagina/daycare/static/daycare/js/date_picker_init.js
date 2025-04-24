// pagina/daycare/static/daycare/js/date_picker_init.js

// Asegura que el DOM esté completamente cargado antes de ejecutar el código principal.
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM completamente cargado. Inicializando scripts.");

    // --- Obtener referencia al input de archivo foto y elementos relacionados ---
    const photoInput = document.getElementById('id_foto'); // El input de archivo real (siempre debería existir en esta página)
    const photoPreview = document.getElementById('photo-preview'); // La imagen para la vista previa (AHORA dentro de la zona de soltar en tu HTML)
    const existingPhotoSection = document.getElementById('existing-photo-section'); // El div que muestra la foto actual (FUERA de la zona de soltar)
    const dropZone = document.getElementById('drop-zone'); // El div que actúa como zona de arrastrar y soltar
    // Obtener TODOS los elementos de texto de instrucción dentro de la zona de soltar
    const dropZoneTextElements = dropZone ? dropZone.querySelectorAll('.drop-zone-text') : []; // Selecciona todos los elementos con clase .drop-zone-text dentro de #drop-zone


    console.log("Input foto (#id_foto) encontrado:", photoInput);
    console.log("Preview img (#photo-preview) encontrado:", photoPreview); // Este debería encontrarse si tu plantilla está correcta
    console.log("Sección foto actual (#existing-photo-section) encontrada:", existingPhotoSection);
    console.log("Área de arrastrar y soltar (#drop-zone) encontrada:", dropZone);
    console.log("Elementos de texto de instrucción (.drop-zone-text) encontrados:", dropZoneTextElements);


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
    // Por ejemplo, el campo de fecha de nacimiento en la página de edición de mascota (su ID es probablemente 'id_fecha_nacimiento').
    // Solo haz esto si realmente tienes un campo 'fecha_nacimiento' en tu PetForm y quieres que sea un datepicker.
    const dateInputPetBirth = document.getElementById('id_fecha_nacimiento'); // ID probable para fecha de nacimiento
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
    // Este listener se dispara cuando se selecciona un archivo en el input de archivo (por click o drag/drop)
    // Ahora maneja la visibilidad de la vista previa y el texto DENTRO de la zona de soltar
    // photoInput, photoPreview, dropZone, dropZoneTextElements ya están declarados y verificados arriba
    if (photoInput && photoPreview && dropZone && dropZoneTextElements.length > 0) { // Aseguramos que todos los elementos necesarios existan
         console.log("Elementos para vista previa encontrados. Añadiendo listener 'change' al input foto.");
        photoInput.addEventListener('change', function(event) {
            console.log("'change' event disparado en input foto.");
            const file = event.target.files[0]; // Obtener el primer archivo seleccionado

            if (file && file.type.startsWith('image/')) { // Verificar si se seleccionó un archivo y si es una imagen
                 console.log("Archivo de imagen seleccionado:", file.name);
                const reader = new FileReader(); // Objeto para leer el contenido del archivo

                reader.onload = function(e) { // Función que se ejecuta cuando la lectura termina
                     console.log("FileReader cargado. Mostrando vista previa y ocultando texto...");
                    photoPreview.src = e.target.result; // Establecer la fuente de la vista previa
                    photoPreview.style.display = 'block'; // Mostrar la imagen de vista previa

                    // --- Controlar la visibilidad DENTRO de la zona de soltar ---
                    // Ocultar todos los párrafos de texto de instrucción
                    dropZoneTextElements.forEach(el => el.style.display = 'none');

                    // Opcional: Ocultar la sección de la foto actual (que está fuera del drop zone)
                    // Esto da la sensación de que la nueva foto "reemplaza" la antigua visualmente de inmediato.
                    if (existingPhotoSection) { // La sección de foto actual solo existe si la mascota tiene foto
                        existingPhotoSection.style.display = 'none';
                         console.log("Ocultando sección foto actual (#existing-photo-section).");
                    }
                };
                reader.readAsDataURL(file); // Leer el archivo como una URL de datos (base64)

            } else { // Si no se selecciona archivo o no es imagen (ej: se canceló el selector de archivo)
                console.log("Ningún archivo seleccionado o no es imagen.");
                photoPreview.src = '#'; // Limpiar la fuente de la vista previa
                photoPreview.style.display = 'none'; // Ocultar la vista previa

                // --- Controlar la visibilidad DENTRO de la zona de soltar ---
                 // Mostrar los párrafos de texto de instrucción de nuevo
                 dropZoneTextElements.forEach(el => el.style.display = 'block');

                // Si se cancela la selección de archivo, volver a mostrar la foto actual si existía
                 if (existingPhotoSection) {
                      existingPhotoSection.style.display = 'block';
                      console.log("Mostrando sección foto actual (#existing-photo-section) de nuevo.");
                  }
            }
        });
    } else {
         // Este warning es esperado en páginas donde no hay campo de foto o los elementos necesarios no están presentes
         console.warn("Elementos para vista previa de foto (input#id_foto, img#photo-preview, div#drop-zone, o .drop-zone-text) no encontrados. La funcionalidad de vista previa no estará activa. (Puede ser esperado)");
    }
    // --- Fin JavaScript para Vista Previa de Subida de Foto ---


    // --- JavaScript para Botón Personalizado de Eliminar Foto ---
    console.log("Intentando configurar botón de eliminar foto personalizado...");
    // photoInput, existingPhotoSection, dropZone, dropZoneTextElements ya están declarados y verificados arriba
    const deleteButton = document.getElementById('delete-photo-button');
    // Casilla 'Limpiar' GENERADA por Django (ID correcto ya confirmado)
    const clearCheckbox = document.getElementById('foto-clear_id'); // <-- ID CORREGIDO


    console.log("Botón eliminar encontrado:", deleteButton);
    console.log("Casilla 'Limpiar' encontrada (ID 'foto-clear_id'):", clearCheckbox);


    // La lógica de eliminar solo aplica si hay una foto existente.
    // El botón 'delete-photo-button' y el div 'existing-photo-section'
    // solo se renderizan en la plantilla si mascota.foto existe (gracias a tu {% if mascota.foto %}).
    // Aseguramos que los TRES elementos necesarios para la eliminación visual existan
    if (deleteButton && clearCheckbox && existingPhotoSection && dropZoneTextElements.length > 0) { // Aseguramos que todos los elementos necesarios existan
        console.log("Elementos para botón eliminar foto personalizado encontrados. Añadiendo listener de click a #delete-photo-button.");

        deleteButton.addEventListener('click', function() {
            console.log("Botón 'Eliminar Foto' clickeado.");

            // Opcional: Mostrar un cuadro de diálogo de confirmación
            const confirmDelete = confirm("¿Estás seguro de que quieres eliminar la foto de la mascota?");
            console.log("Confirmación eliminar:", confirmDelete);

            if (confirmDelete) {
                console.log("Confirmado. Marcando casilla 'Limpiar' oculta y ajustando visibilidad...");
                // ¡La clave! Marcar la casilla 'Limpiar' oculta programáticamente.
                clearCheckbox.checked = true;

                // --- Ajustar visibilidad ---
                // Ocultar la sección de la foto actual (que contiene la img y el botón eliminar)
                existingPhotoSection.style.display = 'none'; // Ocultar el div
                // Ya verificamos que existingPhotoSection existe en el if principal, por lo que deleteButton también se ocultará.

                // Cuando se elimina la foto (visualmente), debemos mostrar el texto de instrucción en la zona de soltar
                 dropZoneTextElements.forEach(el => el.style.display = 'block'); // Mostrar texto de instrucción

                 // Y asegurar que la vista previa está oculta (en caso de que se haya seleccionado algo previamente y luego se decidiera eliminar la foto antigua)
                 if (photoPreview) {
                      photoPreview.src = '#'; // Limpiar la fuente
                      photoPreview.style.display = 'none'; // Ocultar la vista previa
                      console.log("Ocultando vista previa en zona de soltar.");
                 }


                console.log("Foto marcada para eliminar visualmente. Recuerda guardar el formulario.");
            } else {
                 console.log("Eliminación cancelada por el usuario.");
            }
        });
    } else {
        console.warn("Elementos para botón de eliminar foto personalizado no encontrados (botón#delete-photo-button, casilla#foto-clear_id, div#existing-photo-section, o .drop-zone-text). La funcionalidad de eliminar visualmente no estará activa. (Puede ser esperado si la mascota no tiene foto)");
    }


    // --- JavaScript para Arrastrar y Soltar (Drag and Drop) ---
    console.log("Intentando configurar área de arrastrar y soltar foto...");

    // dropZone, photoInput, dropZoneTextElements ya están declarados y verificados arriba

    // Verificar si encontramos la zona de soltar Y el input de archivo
    if (dropZone && photoInput) {
        console.log("Área de arrastrar y soltar (#drop-zone) y input foto (#id_foto) encontrados. Añadiendo listeners de arrastre y suelta.");

        // Prevenir el comportamiento por defecto del navegador
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        // Un-highlight drop zone when item leaves it or is dropped
        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        // Manejar los archivos soltados
        dropZone.addEventListener('drop', handleDrop, false);

        // Hacer que al hacer click en la zona de soltar, se abra el selector de archivo nativo (funciona porque el input está dentro y es invisible)
        // NO necesitamos añadir un listener de click AQUI, ya que el input dentro maneja el click nativamente.
        // La lógica de click en dropZoneTextElements podría ser útil si esos elementos impidieran el click nativo en el input, pero pointer-events: none; debería evitarlo.
        // Si la lógica de click nativo no funciona bien, podríamos considerar AÑADIR este listener de click en la zona de soltar de nuevo.
        // Por ahora, confiamos en el click nativo.


        // --- Funciones de Ayuda ---

        function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }
        function highlight(e) { dropZone.classList.add('dragover'); }
        function unhighlight(e) { dropZone.classList.remove('dragover'); }

        function handleDrop(e) {
             console.log("Archivo(s) soltado(s).");
            const dt = e.dataTransfer;
            const files = dt.files;

            console.log("Archivos soltados:", files);

             if (files.length > 0 && photoInput) {
                 photoInput.files = files;
                 console.log("Archivos asignados al input foto.");

                 // Disparar el evento 'change' manualmente en el input de archivo.
                 // El listener 'change' de la vista previa manejará la visibilidad del texto/imagen dentro de la zona.
                 const event = new Event('change', { bubbles: true });
                 photoInput.dispatchEvent(event);
                 console.log("'change' event disparado en input foto.");

             } else {
                 console.warn("No se soltaron archivos o el input foto no está disponible.");
                 // Si user suelta algo que no es archivo, o cancela arrastre, el change event podría no dispararse o la lista de archivos estar vacía.
                 // El 'else' block en el listener 'change' manejará restaurar el texto y ocultar preview si es necesario.
             }
        }
        // --- Fin Funciones de Ayuda ---

    } else {
        console.warn("Área de arrastrar y soltar (#drop-zone) o input foto (#id_foto) no encontrados. La funcionalidad de arrastrar y soltar no estará activa. (Puede ser esperado)");
    }
    // --- Fin JavaScript para Arrastrar y Soltar ---

}); // --- Fin del listener DOMContentLoaded ---

// --- Cualquier otra función o código que DEBA estar fuera del listener DOMContentLoaded iría aquí ---