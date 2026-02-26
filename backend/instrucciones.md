# dentro de la carpeta back-end:
pip install fastapi uvicorn
uvicorn app:app --reload

# Accedemos a las siguientes direcciones para probar las peticiones GET:
http://localhost:8000/api/tracks?dir=mc1 → JSON para los tracks
http://localhost:8000/media/mc1/archivo.mp3 → audo de los tracks

# Despues los otros endpoints serian:
GET  /api/tracks?dir=mc1          -> lista de tracks
POST /api/tracks                  -> crear track nuevo (metadata + fichero)
PUT  /api/tracks/{dir}/{id}       -> editar
DELETE /api/tracks/{dir}/{id}     -> borrar
