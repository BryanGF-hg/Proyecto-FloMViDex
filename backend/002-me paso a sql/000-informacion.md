# 002-me paso a sql:
## Por que nos pasamos de JSON a SQL:
Es importante notar que antes teniamos un solo archivo JSON estático que supone la base entera del proyecto, cambiar a una base de datos relacional (SQL) nos da mucha más estabilidad, seguridad y velocidad ademas de control avanzado de datos en un futuro.

## Razones:
1.- Consultas Ultra Rápidas: Cuando en tu Frontend haces clic en la pestaña Maidcore 3.0, el servidor de Python ya no tiene que leer un archivo de texto gigante, procesarlo y buscar. Simplemente le dice a SQL:
SELECT * FROM tracks WHERE dir = 'mc3';
SQL encuentra esos registros en milisegundos.

2.- ID Único Global: Ahora cada canción en toda tu colección tiene un "id" único. Ya no hay confusión de si el "ID 1" es de la carpeta 1 o de la 2. El ID 911 siempre será esa canción específica de mc3.

3.- Búsqueda Global: Con el JSON, buscar una canción de un artista en todas las carpetas a la vez era difícil. Ahora es una sola línea:

SELECT * FROM tracks WHERE artist LIKE '%zuf%'; (Esto buscará en los 1515 registros al instante).
