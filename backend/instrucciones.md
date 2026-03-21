# dentro de la carpeta back-end:
pip install fastapi uvicorn PyMySQL python-multipart
## version vieja para el json
  uvicorn 001-json:app --reload
## version nueva para usar sql
  uvicorn 002-sql:app --reload

# Accedemos a las siguientes direcciones para probar las peticiones GET:
- Admin:  http://127.0.0.1:8000/admin/012-conexion%20con%20backend.html
- Frontend: http://127.0.0.1:8000/frontend/005-controlador.html
- API MC1: http://127.0.0.1:8000/api/tracks?dir=mc1\n
- API STATS: http://127.0.0.1:8000/api/stats

# formato de tracks.json:
{
  "mc1":[
  {
    "id": 1,
    "title": "Ozoi The Maid X Yakui The Maid - Frontier",
    "file": "Ozoi The Maid X Yakui The Maid - Frontier.mp3",
    "artist": "zuf",
    "tags": [],
    "dir": "mc1"
  },
  ...],
 "mc2":[...],
 "mc3":[...],
 "mc4":[...]
}
