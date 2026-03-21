from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
import time
import json
import shutil
import pymysql
import os

app = FastAPI(title="FloMViDex Backend - SQL Edition")
# =========================== RUTAS BASE SEGÚN LA ESTRUCTURA
# 002-sql.py deberia estar en FloMViDex/backend/002-sql.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEDIA_ROOT   = PROJECT_ROOT / "media" / "mp3" / "real mp3"
ADMIN_DIR    = PROJECT_ROOT / "admin"
FRONTEND_DIR = PROJECT_ROOT / "frontend"
LOG_DIR      = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

DIR_PATHS = {
    "mc1": "maidcore 1.0",
    "mc2": "maidcore 2.0",
    "mc3": "maidcore 3.0",
    "mc4": "maidcore 4.0",
}

# =========================== CONFIGURACIÓN SQL
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='dj_maidcore',
        password='dj_maidcore',
        database='flomvidex',
        cursorclass=pymysql.cursors.DictCursor
    )

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],allow_credentials=True,
    allow_methods=["*"],allow_headers=["*"],
)

# =========================== MODELOS, es decir, como se basa los datos
class Track(BaseModel):
    id: int       
    title: str
    file: str
    artist: str = ""
    tags: List[str] = []
    dir: str

class TrackUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    tags: Optional[List[str]] = None

# =========================== ESTÁTICOS: AUDIO
# /media/mc1/archivo.mp3 -> media/mp3/real mp3/maidcore 1.0/archivo.mp3
for dir_key, folder_name in DIR_PATHS.items():
    app.mount(f"/media/{dir_key}", StaticFiles(directory=MEDIA_ROOT / folder_name), name=f"media-{dir_key}")

if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    print(f"[INFO] Static mount: /frontend -> {FRONTEND_DIR}")        
if ADMIN_DIR.exists():
    app.mount("/admin", StaticFiles(directory=ADMIN_DIR), name="admin")
    print(f"[INFO] Static mount: /admin -> {ADMIN_DIR}")    
    
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~PUERTOS~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("[INFO]-Admin:    http://127.0.0.1:8000/admin/archivo")
print("[INFO]-Frontend: http://127.0.0.1:8000/frontend/archivo")
print("[INFO]-API MCX:  http://127.0.0.1:8000/api/tracks?dir=mcX")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# ===========================
# API: GET /api/tracks
# ===========================
@app.get("/api/tracks", response_model=List[Track])
def get_tracks(dir: str = Query(..., description="mc1, mc2, mc3, mc4")):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
          if dir == "all":
            #BUSQUEDA GLOBAL
            cursor.execute("SELECT * FROM tracks")
          else:
            # BUSQUEDA FILTRADA            
            cursor.execute("SELECT * FROM tracks WHERE dir = %s", (dir,))
            rows = cursor.fetchall()
            # Convertir tags de string (DB) a lista (JSON)
            for row in rows:
                row['tags'] = row['tags'].split(',') if row['tags'] else []
            return rows
    finally:
        conn.close()

# ===========================
# API: POST /api/tracks
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

    dest_dir = MEDIA_ROOT / DIR_PATHS[dir]
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / file.filename

    # Guardar archivo físico
    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    final_title = title or dest_path.stem
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO tracks (title, file, artist, tags, dir) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (final_title, file.filename, artist, tags, dir))
            new_id = cursor.lastrowid
            
            # Registrar log en SQL
            cursor.execute("INSERT INTO logs (action) VALUES (%s)", (f"Subida: {file.filename}",))
        conn.commit()
        
        return Track(id=new_id, title=final_title, file=file.filename, artist=artist, tags=tags.split(',') if tags else [], dir=dir)
    finally:
        conn.close()

# ===========================
# API: PUT /api/tracks/{dir}/{id}
# ===========================
@app.put("/api/tracks/{dir}/{track_id}", response_model=Track)
def update_track(dir: str, track_id: int, payload: TrackUpdate):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Construir query dinámica según lo que venga en el payload
            updates = []
            values = []
            if payload.title is not None:
                updates.append("title = %s")
                values.append(payload.title)
            if payload.artist is not None:
                updates.append("artist = %s")
                values.append(payload.artist)
            if payload.tags is not None:
                updates.append("tags = %s")
                values.append(",".join(payload.tags))
            
            if not updates:
                raise HTTPException(status_code=400, detail="Nada que actualizar")
            
            values.extend([track_id, dir])
            sql = f"UPDATE tracks SET {', '.join(updates)} WHERE id = %s AND dir = %s"
            cursor.execute(sql, tuple(values))
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Track no encontrado")
        
        conn.commit()
        return get_track_by_id(track_id) # Función auxiliar
    finally:
        conn.close()

# ===========================
# API: DELETE /api/tracks/{dir}/{id}
# ===========================
@app.delete("/api/tracks/{dir}/{track_id}")
def delete_track(dir: str, track_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1. Buscar nombre de archivo para borrarlo del disco
            cursor.execute("SELECT file FROM tracks WHERE id = %s AND dir = %s", (track_id, dir))
            track = cursor.fetchone()
            if not track:
                raise HTTPException(status_code=404, detail="Track no encontrado")
            
            file_path = MEDIA_ROOT / DIR_PATHS[dir] / track['file']
            if file_path.exists():
                file_path.unlink()

            # 2. Borrar de SQL
            cursor.execute("DELETE FROM tracks WHERE id = %s", (track_id,))
            cursor.execute("INSERT INTO logs (action) VALUES (%s)", (f"Eliminado: ID {track_id}",))
        conn.commit()
        return {"ok": True, "deleted_id": track_id}
    finally:
        conn.close()

def get_track_by_id(track_id: int):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tracks WHERE id = %s", (track_id,))
        t = cursor.fetchone()
        t['tags'] = t['tags'].split(',') if t['tags'] else []
        return t

# ===========================
# API: COUNT /api/stats/{dir}/{id}
# ===========================
@app.get("/api/stats")
def get_stats():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Esta consulta agrupa por directorio y cuenta cuántos hay en cada uno
            sql = "SELECT dir, COUNT(*) as total FROM tracks GROUP BY dir"
            cursor.execute(sql)
            stats_list = cursor.fetchall()
            
            # También sacamos el gran total
            cursor.execute("SELECT COUNT(*) as gran_total FROM tracks")
            total_general = cursor.fetchone()['gran_total']
            
            return {
                "por_directorio": stats_list,
                "total_global": total_general
            }
    finally:
        conn.close()        
