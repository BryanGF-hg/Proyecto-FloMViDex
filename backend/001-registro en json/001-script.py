import json
import re
from difflib import SequenceMatcher

def normalize_title(title: str) -> str:
    """
    Normaliza el título para poder compararlo:
    - pasa a minúsculas
    - elimina texto entre paréntesis (opcional)
    - quita caracteres raros, se queda con letras y números
    - recorta espacios extra
    """
    if not isinstance(title, str):
        return ""
    
    t = title.lower()
    # Opcional: eliminar lo que está entre paréntesis, tipo "1414 (extended ver.)" -> "1414 "
    t = re.sub(r'\(.*?\)', '', t)
    # Dejar solo letras, números y espacios
    t = re.sub(r'[^a-z0-9áéíóúüñ]+', ' ', t)
    # Quitar espacios al principio y final, y espacios dobles
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def load_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_small_index(small_data: dict):
    """
    Crea un índice por 'dir':
    {
        "mc1": [
            {"norm_title": "...", "artist": "...", "title": "..."},
            ...
        ],
        "mc2": [...]
    }
    """
    index = {}

    for dir_name, tracks in small_data.items():
        index[dir_name] = []
        for track in tracks:
            small_title = track.get("title", "")
            artist = track.get("artist", "")
            norm = normalize_title(small_title)
            index[dir_name].append({
                "norm_title": norm,
                "artist": artist,
                "title": small_title
            })
    return index


def find_best_match(norm_master_title: str, candidates: list, min_score: float = 0.6):
    """
    Busca el mejor título candidato usando similitud de SequenceMatcher.
    Devuelve el diccionario del mejor match o None si no llega al min_score.
    """
    best = None
    best_score = 0.0

    for c in candidates:
        score = SequenceMatcher(None, norm_master_title, c["norm_title"]).ratio()
        if score > best_score:
            best_score = score
            best = c

    if best is not None and best_score >= min_score:
        return best, best_score
    return None, 0.0


def enrich_master_with_artists(master_path: str, small_path: str, output_path: str):
    # 1. Cargar JSONs
    master_data = load_json(master_path)
    small_data = load_json(small_path)

    # 2. Crear índice del json pequeño
    small_index = build_small_index(small_data)

    # 3. Recorrer master y asignar artist cuando haya match
    for track in master_data:
        dir_name = track.get("dir")
        title = track.get("title", "")

        # Si no hay dir o no existe en el json pequeño, saltamos
        if not dir_name or dir_name not in small_index:
            continue

        # Normalizar título del master
        norm_master = normalize_title(title)

        # Buscar mejor candidato en el mismo 'dir'
        candidates = small_index[dir_name]
        best_match, score = find_best_match(norm_master, candidates, min_score=0.6)

        if best_match:
            # Solo sobreescribimos si artist está vacío o no existe
            if not track.get("artist"):
                track["artist"] = best_match["artist"]
            # Si quieres, puedes guardar también info del matching:
            # track["matched_title_small"] = best_match["title"]
            # track["match_score"] = score

    # 4. Guardar nuevo master enriquecido
    save_json(master_data, output_path)


if __name__ == "__main__":
    # Cambia los nombres de los archivos si los tuyos son distintos
    enrich_master_with_artists(
        master_path="master-mc1.json",
        small_path="artista-mc1.json",
        output_path="resultado1.json"
    )
