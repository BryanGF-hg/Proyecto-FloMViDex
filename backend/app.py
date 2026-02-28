from fastapi import ( FastAPI,HTTPException,Query,UploadFile,File,Form)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
import json
import shutil
app = FastAPI(title="FloMViDex Backend")
# =========================== RUTAS BASE SEGÚN TU ESTRUCTURA
# app.py deberia estar en FloMViDex/backend/app.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEDIA_ROOT   = PROJECT_ROOT / "media" / "mp3" / "real mp3"
ADMIN_DIR    = PROJECT_ROOT / "admin"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
DATA_DIR     = PROJECT_ROOT / "backend" / "data"
DATA_FILE    = DATA_DIR / "tracks.json"

DIR_PATHS = {
    "mc1": "maidcore 1.0",
    "mc2": "maidcore 2.0",
    "mc3": "maidcore 3.0",
    "mc4": "maidcore 4.0",
}
# CORS
origins = [
    "http://localhost:8000","http://127.0.0.1:8000",
    "http://localhost:5500","http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================== MODELOS, es decir, como se basa los datos
class Track(BaseModel):
    id: int       
    title: str           # opcional
    file: str            # nombre del archivo en disco
    artist: str = ""     # opcional
    tags: List[str] = [] # opcional
    dir: str             # "mc1", "mc2", ...
class TrackUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    tags: Optional[List[str]] = None
tracks_by_directory: Dict[str, List[Track]] = {k: [] for k in DIR_PATHS.keys()}

# =========================== UTILIDADES: JSON PERSISTENTE
def save_tracks_to_json() -> None:
    """Guardar tracks_by_directory -> DATA_FILE (JSON)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    raw = {
        dir_key: [t.dict() for t in arr]
        for dir_key, arr in tracks_by_directory.items()
    }
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(raw, f, ensure_ascii=False, indent=2)
    print(f"[INFO] Tracks guardados en {DATA_FILE}")

def load_tracks_from_json() -> bool:
    """Cargar tracks desde JSON si existe. Devuelve True si se cargó, False si no."""
    if not DATA_FILE.exists():
        print(f"[INFO] No existe {DATA_FILE}, se usará escaneo de carpetas.")
        return False

    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            raw = json.load(f)
        for dir_key, arr in raw.items():
            tracks_by_directory[dir_key] = [Track(**t) for t in arr]
        print(f"[INFO]-Datos: Tracks cargados desde {DATA_FILE}")
        return True
    except Exception as e:
        print(f"[ERROR] Al leer {DATA_FILE}: {e}")
        return False

# =========================== UTILIDADES: ESCANEAR CARPETAS
def scan_media_folders() -> None:
    """Escanear maidcore X.0 y rellenar tracks_by_directory."""
    for dir_key, folder_name in DIR_PATHS.items():
        folder_path = MEDIA_ROOT / folder_name
        if not folder_path.exists():
            print(f"[WARN] Carpeta no encontrada: {folder_path}")
            continue

        tracks: List[Track] = []
        next_id = 1
        for f in sorted(folder_path.iterdir()):
            if f.is_file() and f.suffix.lower() in {".mp3", ".opus", ".ogg", ".wav"}:
                tracks.append(
                    Track(
                        id=next_id,
                        title=f.stem,
                        file=f.name,
                        dir=dir_key,
                        artist="",
                        tags=[],
                    )
                )
                next_id += 1
        tracks_by_directory[dir_key] = tracks
        print(f"[INFO] {dir_key}: {len(tracks)} tracks indexados")

    # Guardamos ese escaneo en JSON como estado inicial
    save_tracks_to_json()

def get_next_free_id(dir_key: str) -> int:
    arr = tracks_by_directory.get(dir_key, [])
    used = {t.id for t in arr}
    i = 1
    while i in used:
        i += 1
    return i

# STARTUP, al iniciar montame estáticos y usa las API para el CRUD en el backend
@app.on_event("startup")
def on_startup():
    # 1) Intentar cargar desde JSON
    loaded = load_tracks_from_json()
    # 2) Si no hay JSON, escanear carpetas y generar JSON
    if not loaded:
        scan_media_folders()

# =========================== ESTÁTICOS: AUDIO
# /media/mc1/archivo.mp3 -> media/mp3/real mp3/maidcore 1.0/archivo.mp3
for dir_key, folder_name in DIR_PATHS.items():
    mount_path = f"/media/{dir_key}"
    dir_path = MEDIA_ROOT / folder_name
    app.mount(mount_path, StaticFiles(directory=dir_path), name=f"media-{dir_key}")
    print(f"[INFO] Static mount: {mount_path} -> {dir_path}")
# =========================== ESTÁTICOS: BACKEND ADMIN
# /admin/... -> FloMViDex/admin/*
if ADMIN_DIR.exists():
    app.mount("/admin", StaticFiles(directory=ADMIN_DIR), name="admin")
    print(f"[INFO] Static mount: /admin -> {ADMIN_DIR}")
else: print("[WARN] ADMIN_DIR no existe:", ADMIN_DIR)
# =========================== ESTÁTICOS: FRONTEND USUARIO
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend") #cambiar /"nombre_estatico" para que sea corresponda a la carpeta real como /frontend
    print(f"[INFO] Static mount: /frontend -> {FRONTEND_DIR}")    
else: print("[WARN] FRONTEND_DIR no existe:", FRONTEND_DIR)

print("\n[INFO]-Admin:    http://127.0.0.1:8000/admin/archivo")
print("[INFO]-Frontend: http://127.0.0.1:8000/frontend/archivo")
print("[INFO]-API MCX:  http://127.0.0.1:8000/api/tracks?dir=mcX\n")





# ===========================
# API: GET /api/tracks
# ===========================
@app.get("/api/tracks", response_model=List[Track])
def get_tracks(dir: str = Query(..., description="mc1, mc2, mc3, mc4")):
    if dir not in tracks_by_directory:
        raise HTTPException(status_code=400, detail="Directorio inválido")
    return tracks_by_directory[dir]

# ===========================
# API: POST /api/tracks (crear + subir archivo)
# ===========================
@app.post("/api/tracks", response_model=Track)
async def create_track(
    dir: str = Form(...),
    title: str = Form(""),
    artist: str = Form(""),
    tags: str = Form(""),          
    file: UploadFile = File(...),
):
    if dir not in DIR_PATHS:
        raise HTTPException(status_code=400, detail="Directorio inválido")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Archivo requerido")

    # Carpeta física de destino
    folder_name = DIR_PATHS[dir]
    dest_dir = MEDIA_ROOT / folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Normalizar nombre
    original_name = Path(file.filename).name
    dest_path = dest_dir / original_name
    # variables para los condicionales siguientes que comprueban los archivos en tracks.json
    existing_tracks = tracks_by_directory.get(dir, [])
    existing_files = {t.file for t in existing_tracks}      
    if dest_path.exists() and original_name in existing_files:  # 1.- El archivo YA EXISTE y YA ESTÁ REGISTRADO
        raise HTTPException( status_code=400, detail=f"El archivo '{original_name}' ya existe en el directorio {dir}" )     # 2.- Si el archivo existe en disco pero NO en tracks.json (inconsistencia)
    if dest_path.exists() and original_name not in existing_files: # Renombrar el archivo existente como backup
        backup_name = f"{dest_path.stem}_backup{dest_path.suffix}"
        backup_path = dest_dir / backup_name
        dest_path.rename(backup_path)
        print(f"[WARN] Archivo huérfano renombrado a {backup_name}") 

    # Guardar archivo físico
    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parsear tags
    tags_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []

    # Calcular ID libre
    new_id = get_next_free_id(dir)

    track = Track(
        id=new_id,
        title=title or dest_path.stem,
        file=dest_path.name,
        artist=artist,
        tags=tags_list,
        dir=dir,
    )

    tracks_by_directory[dir].append(track)
    save_tracks_to_json()

    return track

# ===========================
# API: PUT /api/tracks/{dir}/{id} (editar metadata)
# ===========================
@app.put("/api/tracks/{dir}/{track_id}", response_model=Track)
def update_track(dir: str, track_id: int, payload: TrackUpdate):
    if dir not in tracks_by_directory:
        raise HTTPException(status_code=404, detail="Directorio no encontrado")

    arr = tracks_by_directory[dir]

    for idx, track in enumerate(arr):
        if track.id == track_id:
            data = track.dict()

            if payload.title is not None:
                data["title"] = payload.title
            if payload.artist is not None:
                data["artist"] = payload.artist
            if payload.tags is not None:
                data["tags"] = payload.tags

            updated = Track(**data)
            arr[idx] = updated
            save_tracks_to_json()
            return updated

    raise HTTPException(status_code=404, detail="Track no encontrado")

# ===========================
# API: DELETE /api/tracks/{dir}/{id} (eliminar metadata)
# ===========================
@app.delete("/api/tracks/{dir}/{track_id}")
def delete_track(dir: str, track_id: int):
    if dir not in tracks_by_directory:
        raise HTTPException(status_code=404, detail="Directorio no encontrado")

    arr = tracks_by_directory[dir]

    for idx, track in enumerate(arr):
        if track.id == track_id:
            # Borrar archivo físico
            folder_name = DIR_PATHS.get(dir)
            if folder_name:
                file_path = MEDIA_ROOT / folder_name / track.file
                try:
                    if file_path.exists():
                        file_path.unlink()
                        print(f"[INFO] Archivo borrado: {file_path}")
                    else:
                        print(f"[WARN] Archivo no encontrado en disco: {file_path}")
                except Exception as e:
                    print(f"[ERROR] Al borrar archivo {file_path}: {e}")
                    raise HTTPException(
                        status_code=500,
                        detail=f"Error al borrar archivo físico: {e}"
                    )

            # Borrar metadata
            arr.pop(idx)
            save_tracks_to_json()
            return {"ok": True, "deleted_id": track_id, "dir": dir}

    raise HTTPException(status_code=404, detail="Track no encontrado")
