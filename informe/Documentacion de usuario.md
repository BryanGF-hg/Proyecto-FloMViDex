# FRONTEND-MaidCore Player (Interfaz de Escucha)
El reproductor está diseñado con una estética nostálgica de Windows XP.
## Navegación: 
Use los botones superiores (Maidcore 1.0, 2.0, etc.) para cambiar de "disco" o directorio.

# Reproducción:
Haz doble clic en una canción de la lista para empezar.
Usa los controles ⏮, ▶/⏸, ⏭ para gestionar el flujo.

## Barra de Título:
 Muestra la versión del programa y el total de canciones disponibles en la base de datos.
## Taskbar (Barra de Tareas):
 Puedes minimizar la ventana, registrar tu acceso o consultar el reloj del sistema (a futuro, seleccionar una canción aleatoria dentro del directorio como ver albumes).



# BACKEND-Admin Dashboard (Panel de Control)
Permite la gestión de la biblioteca musical.

# Búsqueda Global:
 En el filtro de extensiones, podemos seleccionar "BÚSQUEDA GLOBAL". Esto permite buscar cualquier canción en toda la base de datos sin importar en qué carpeta esté.

#Subida de Canciones: 
Selecciona el directorio de destino.
También arrastra tus archivos de audio al formulario.
Puedes añadir Título, Artista y Tags de forma masiva o individual.

# Mantenimiento:
## Eliminar: 
Selecciona varias canciones y pulsa "Eliminar seleccionados" para limpiar la biblioteca.
##Exportar:
 Genera un respaldo en formato JSON del directorio actual en la CONSOLA.

# Guía de Mantenimiento (Linux)
Si el sistema se siente lento:

Reiniciar procesos: pkill gunicorn y volver a lanzar con 4 workers.

Limpiar logs: Revisar el archivo de registro de acceso si la base de datos crece demasiado.

Permisos: Asegúrate de que la carpeta /media/ tenga permisos de escritura (chmod 775) para que la API pueda guardar las subidas de nuevos usuarios.
