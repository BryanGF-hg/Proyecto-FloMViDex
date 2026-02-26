from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict
from pathlib import Path

app = FastAPI(title="FloMViDex Backend")

# ===========================
# RUTAS BASE SEGÚN TU ESTRUCTURA
# ===========================
# app.py está en FloMViDex/backend/app.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADMIN_DIR    = PROJECT_ROOT / "admin"
MEDIA_ROOT   = PROJECT_ROOT / "media" / "mp3" / "real mp3"

DIR_PATHS = {
    "mc1": "maidcore 1.0",
    "mc2": "maidcore 2.0",
    "mc3": "maidcore 3.0",
    "mc4": "maidcore 4.0",
}

# ===========================
# CORS (por si sirves frontend en OTRO puerto)
# ===========================
origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# MODELO DE TRACK
# ===========================
class Track(BaseModel):
    id: int
    title: str
    file: str
    artist: str = ""
    tags: List[str] = []
    dir: str

tracks_by_directory: Dict[str, List[Track]] = {k: [] for k in DIR_PATHS.keys()}


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


@app.on_event("startup")
def on_startup():
    scan_media_folders()

# ===========================
# ESTÁTICOS: AUDIO
# ===========================
# /media/mc1/archivo.mp3 -> media/mp3/real mp3/maidcore 1.0/archivo.mp3
for dir_key, folder_name in DIR_PATHS.items():
    mount_path = f"/media/{dir_key}"
    dir_path = MEDIA_ROOT / folder_name
    app.mount(mount_path, StaticFiles(directory=dir_path), name=f"media-{dir_key}")
    print(f"[INFO] Static mount: {mount_path} -> {dir_path}")

# ===========================
# ESTÁTICOS: FRONTEND ADMIN
# ===========================
# /admin/... -> FloMViDex/admin/*
if ADMIN_DIR.exists():
    app.mount("/admin", StaticFiles(directory=ADMIN_DIR), name="admin")
    print(f"[INFO] Static mount: /admin -> {ADMIN_DIR}")
else:
    print("[WARN] ADMIN_DIR no existe:", ADMIN_DIR)

print("\nPara acceder al admin: http://127.0.0.1:8000/admin/012-conexion%20con%20backend.html")
print("Para acceder a la lista de los audio: http://127.0.0.1:8000/api/tracks?dir=mc1\n")

# ===========================
# API: LISTAR TRACKS
# ===========================
@app.get("/api/tracks", response_model=List[Track])
def get_tracks(dir: str = Query(..., description="mc1, mc2, mc3, mc4")):
    if dir not in tracks_by_directory:
        raise HTTPException(status_code=400, detail="Directorio inválido")
    return tracks_by_directory[dir]
