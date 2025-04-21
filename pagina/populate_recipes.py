# populate_recipes.py

# Configura el entorno de Django para poder usar los modelos
import os
import django
from django.utils import timezone

# Configura el settings de tu proyecto (reemplaza 'mysite.settings' si tu proyecto se llama diferente)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Ahora puedes importar tus modelos
from app1.models import Receta

# Lista de datos de recetas para añadir
recetas_data = [
    {
        'nombre': 'Crispy Pata',
        'tiempo_preparacion': '30 minutos + marinado',
        'tiempo_coccion': '3-4 horas (hervir) + 45-60 minutos (freír)',
        'ingredientes': '''
1 pata de cerdo entera (trasera)
Agua, sal, granos de pimienta, hojas de laurel
Ajo, cebolla
Aceite para freír (suficiente para sumergir)
Salsa de mojo (vinagre, salsa de soja, ajo, cebolla, chiles) para servir
''',
        'instrucciones': '''
1. Hierve la pata de cerdo en agua con sal, granos de pimienta, laurel, ajo y cebolla hasta que esté muy tierna (3-4 horas).
2. Retira la pata, sécala completamente (es crucial para que quede crujiente) y refrigera por unas horas o toda la noche.
3. Calienta abundante aceite en una olla grande a fuego medio-alto.
4. Fríe la pata de cerdo, con cuidado, rotándola, hasta que la piel esté muy crujiente y dorada. Esto puede tomar 45-60 minutos.
5. Escurre sobre papel de cocina, trocea y sirve inmediatamente con salsa de mojo.
'''
    },
    {
        'nombre': 'Kare-Kare',
        'tiempo_preparacion': '20 minutos',
        'tiempo_coccion': '2-3 horas',
        'ingredientes': '''
Rabos de toro o carrilleras de ternera
Pasta de cacahuete (sin azúcar)
Achote (para color, opcional)
Cebolla, ajos
Berengena, judías largas, bok choy (pak choi)
Pasta de camarones (bagoong alamang), salteada
Caldo de ternera o agua
Aceite vegetal
Sal
''',
        'instrucciones': '''
1. Hierve el rabo/carne en agua con sal hasta que esté muy tierno (2-3 horas), retirando la espuma. Reserva el caldo.
2. En otra olla, saltea ajo y cebolla. Añade la pasta de cacahuete disuelta en un poco de caldo caliente y achote (si usas). Cocina hasta espesar.
3. Añade la carne tierna y cocina a fuego lento unos minutos.
4. Cuece las verduras por separado brevemente en agua o blanquéalas.
5. Sirve el guiso de carne con las verduras cocidas aparte. Acompaña con bagoong alamang salteado.
'''
    },
    {
        'nombre': 'La Paz Batchoy',
        'tiempo_preparacion': '15 minutos',
        'tiempo_coccion': '30-40 minutos',
        'ingredientes': '''
Fideos Miki frescos
Cerdo (picado y órganos como hígado, bofe - opcional)
Camarones (opcional)
Caldo de cerdo (idealmente hecho con huesos)
Cebolla, ajos, jengibre
Chicharrón (piel de cerdo crujiente), picado
Cebolleta picada
Huevo cocido
Aceite de camarones (opcional)
Patis (salsa de pescado) al gusto
''',
        'instrucciones': '''
1. En una olla, saltea ajo, cebolla y jengibre.
2. Añade el cerdo/órganos/camarones y cocina hasta que cambien de color.
3. Vierte el caldo de cerdo, lleva a ebullición y cocina a fuego lento 15-20 min.
4. Añade los fideos Miki y cocina unos minutos hasta que estén listos. Sazona con patis.
5. Sirve en boles, cubierto con chicharrón picado, cebolleta, ajo frito (si tienes) y medio huevo cocido. Añade aceite de camarones si usas.
'''
    },
    {
        'nombre': 'Pork Menudo',
        'tiempo_preparacion': '20 minutos',
        'tiempo_coccion': '45-60 minutos',
        'ingredientes': '''
500g de carne de cerdo en cubos pequeños
200g de hígado de cerdo en cubos pequeños (opcional)
Tomates en cubos
Cebolla, ajos
Patatas y zanahorias en cubos pequeños
Garbanzos (opcional)
Salchichas de cerdo en rodajas (como Hotdog filipino, opcional)
Salsa de tomate
Salsa de soja
Caldo de pollo o agua
Guisantes (chícharos)
Aceite vegetal
Sal y pimienta
''',
        'instrucciones': '''
1. Saltea ajo, cebolla y tomate. Añade el cerdo y cocina hasta dorar.
2. Incorpora el hígado (si usas) y cocina brevemente.
3. Añade patatas, zanahorias, garbanzos (si usas), salsa de tomate, salsa de soja y caldo. Lleva a ebullición.
4. Reduce el fuego, tapa y cocina a fuego lento hasta que la carne y las verduras estén tiernas (unos 30-40 min).
5. Añade las salchichas (si usas) y los guisantes; cocina unos minutos más.
6. Sazona con sal y pimienta al gusto. Sirve caliente.
'''
    },
    {
        'nombre': 'Mechado de Ternera',
        'tiempo_preparacion': '20 minutos + marinado',
        'tiempo_coccion': '1.5 - 2 horas',
        'ingredientes': '''
500g de ternera para guisar, en trozos grandes
Tocino o grasa de cerdo
Salsa de soja, jugo de limón/calamansi
Ajos picados, cebolla picada
Tomates picados o salsa de tomate
Caldo de ternera o agua
Patatas y zanahorias en trozos grandes
Pimientos rojos y verdes en tiras
Laurel
Aceite vegetal
Sal y pimienta
''',
        'instrucciones': '''
1. Marina la ternera en salsa de soja y jugo de limón por al menos 30 minutos.
2. Saltea ajo y cebolla. Añade la ternera marinada y dora.
3. Añade tomates/salsa de tomate y laurel. Cocina unos minutos.
4. Vierte caldo/agua suficiente para cubrir. Lleva a ebullición, luego baja el fuego, tapa y cocina a fuego lento hasta que la ternera esté tierna (1-1.5 horas).
5. Añade patatas y zanahorias, cocina hasta que estén tiernas.
6. Incorpora los pimientos. Cocina unos minutos más.
7. Sazona con sal y pimienta. Sirve caliente.
'''
    },
    {
        'nombre': 'Kaldereta de Ternera',
        'tiempo_preparacion': '20 minutos',
        'tiempo_coccion': '1.5 - 2 horas',
        'ingredientes': '''
500g de ternera para guisar, en cubos
Salsa de tomate
Hígado de ternera (opcional), picado o paté de hígado
Ajos picados, cebolla picada
Pimientos rojos y verdes en tiras
Aceitunas verdes
Guisantes (chícharos)
Patatas y zanahorias en cubos
Queso rallado (tipo cheddar o Eden) (opcional)
Caldo de ternera o agua
Aceite vegetal
Sal, pimienta, hojuelas de chile (opcional)
''',
        'instrucciones': '''
1. Saltea ajo y cebolla. Añade la ternera y dora.
2. Añade salsa de tomate, pasta de hígado (si usas), caldo/agua, laurel (opcional) y hojuelas de chile (si usas). Hierve, baja fuego, tapa y cocina hasta que la ternera esté tierna (1-1.5 horas).
3. Añade patatas y zanahorias, cocina hasta que estén tiernas.
4. Incorpora pimientos, aceitunas y guisantes. Cocina unos minutos más.
5. Sazona al gusto. Si usas queso, añádelo al final y revuelve hasta derretir.
'''
    },
    {
        'nombre': 'Pork Sisig',
        'tiempo_preparacion': '20 minutos + hervir/asar',
        'tiempo_coccion': '10-15 minutos (saltear)',
        'ingredientes': '''
Careta de cerdo, orejas, barriga (o una mezcla)
Cebolla roja picada
Jengibre picado
Chiles labuyo picados (al gusto)
Jugo de calamansi o limón
Salsa de soja
Mayonesa o huevo crudo (opcional)
Mantequilla o aceite
''',
        'instrucciones': '''
1. Hierve la careta/carne hasta tierna, luego ásala o fríela hasta que esté crujiente. Pícala finamente.
2. En una sartén caliente (idealmente de hierro), derrite mantequilla o aceite.
3. Saltea la cebolla y el jengibre.
4. Añade la carne picada crujiente. Saltea por unos minutos.
5. Sazona con salsa de soja y jugo de calamansi/limón. Añade chiles.
6. Si usas, añade mayonesa o rompe un huevo crudo encima y mezcla rápidamente en el calor.
7. Sirve sizzling (chispeante) si es posible.
'''
    },
    {
        'nombre': 'Gising-Gising',
        'tiempo_preparacion': '10 minutos',
        'tiempo_coccion': '15-20 minutos',
        'ingredientes': '''
Judías verdes o judías largas (sitaw), picadas
Carne de cerdo picada (opcional)
Camarones pequeños (opcional)
Leche de coco
Pasta de camarones (bagoong alamang)
Ajos picados, cebolla picada
Chiles labuyo picados (al gusto)
''',
        'instrucciones': '''
1. Saltea ajo y cebolla. Añade carne/camarones si usas y cocina.
2. Añade el bagoong alamang y cocina por 1-2 minutos.
3. Vierte la leche de coco y lleva a ebullición suave.
4. Añade las judías verdes y los chiles.
5. Cocina a fuego lento hasta que las judías estén tiernas y la salsa se haya espesado un poco.
6. Sazona al gusto y sirve caliente.
'''
    },
    {
        'nombre': 'Turon (Plátano Lumpia)',
        'tiempo_preparacion': '15 minutos',
        'tiempo_coccion': '5-7 minutos (por tanda)',
        'ingredientes': '''
Plátanos Saba maduros, cortados a lo largo en 2-4 trozos
Yaca (langka) en tiras (opcional)
Azúcar moreno
Hojas de lumpia (medianas o grandes)
Aceite para freír
''',
        'instrucciones': '''
1. Espolvorea cada trozo de plátano con azúcar moreno.
2. Coloca un trozo de plátano (y yaca si usas) en un extremo de una hoja de lumpia.
3. Dobla los lados, luego enrolla firmemente. Humedece el borde para sellar. Opcional: enrolla en azúcar extra.
4. Calienta suficiente aceite para freír en una sartén.
5. Fríe los rollitos de Turon hasta que estén dorados y crujientes por fuera. Si usaste azúcar por fuera, caramelizará.
6. Escurre y sirve caliente.
'''
    },
    {
        'nombre': 'Palabok / Pancit Malabon',
        'tiempo_preparacion': '20 minutos',
        'tiempo_coccion': '30-40 minutos (salsa)',
        'ingredientes': '''
Fideos de arroz gruesos (para Palabok/Malabon)
Camarones, cocidos y pelados (reserva algunas cabezas/cáscaras para la salsa)
Cerdo hervido y desmenuzado
Calamares (opcional)
Tofu frito o buñuelos de pescado, en cubos
Huevos cocidos, en rodajas
Chicharrón (piel de cerdo crujiente), picado
Cebolleta picada
Ajo frito picado
Salsa de pescado (patis)
Para la Salsa:
Harina de arroz o maicena
Caldo (de camarones/cerdo)
Gambas molidas (secas o frescas cabezas/cáscaras)
Achote en polvo (para color)
Ajo picado, cebolla picada
Salsa de pescado (patis)
''',
        'instrucciones': '''
1. Prepara los fideos según el paquete.
2. Para la salsa: Sofríe ajo y cebolla. Añade gambas molidas/cabezas y cocina. Añade achote. Vierte caldo y lleva a ebullición. Espesa con harina de arroz/maicena disuelta en agua. Sazona con patis. Cocina hasta espesar.
3. Para servir: Coloca fideos en un plato. Vierte la salsa caliente encima.
4. Cubre con aderezos: camarones, cerdo desmenuzado, calamares (si usas), tofu frito, huevo cocido, chicharrón, cebolleta y ajo frito. Sirve inmediatamente.
'''
    },
]

# Bucle para crear y guardar los objetos Receta
print("Iniciando la población de recetas...")
for data in recetas_data:
    try:
        # Intenta obtener la receta por nombre, si no existe, la crea con los datos
        receta, created = Receta.objects.get_or_create(
            nombre=data.get('nombre'), # Usa el nombre como clave para ver si ya existe
            defaults={ # Si la receta no existe, usa estos valores para crearla
                'tiempo_preparacion': data.get('tiempo_preparacion', ''), # Usa .get() con valor por defecto ''
                'tiempo_coccion': data.get('tiempo_coccion', ''),
                'ingredientes': data.get('ingredientes', ''),
                'instrucciones': data.get('instrucciones', '')
            }
        )
        if created:
            print(f"Receta '{receta.nombre}' añadida con éxito.")
        else:
            print(f"Receta '{receta.nombre}' ya existe. Saltando.") # Mensaje si ya existe

    except Exception as e:
        # Captura cualquier otro error que pueda ocurrir al crear/guardar
        print(f"Error al añadir o obtener la receta '{data.get('nombre', 'Desconocida')}': {e}")

print("Población de recetas finalizada.")