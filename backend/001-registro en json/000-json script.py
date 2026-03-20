import json
import requests

PLAYLIST_URLS = [
    "https://soundcloud.com/maidcore/sets/maidcore",
    "https://soundcloud.com/maidcore/sets/maidcore-2-0",
    "https://soundcloud.com/maidcore/sets/maidcore-3-0",
    "https://soundcloud.com/maidcore/sets/maidcore-4-0"
]

CLIENT_ID = "TU_CLIENT_ID_AQUI"


def resolve_soundcloud_url(url, client_id):
    api_url = "https://api-v2.soundcloud.com/resolve"
    params = {"url": url, "client_id": client_id}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": "https://soundcloud.com/",
        "Origin": "https://soundcloud.com"
    }
    resp = requests.get(api_url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()


def limpiar_descripcion(desc):
    if not desc:
        return ""
    return " ".join(desc.split())


def generar_catalogo():
    catalog = {
        "meta": {
            "source": "soundcloud",
            "description": "Catálogo generado desde playlists Maidcore"
        },
        "playlists": [],
        "tracks": {},
        "artists": {}
    }

    track_counter = 0

    for idx, url in enumerate(PLAYLIST_URLS):
        data = resolve_soundcloud_url(url, CLIENT_ID)

        playlist_id = f"maidcore-{idx+1}"
        playlist_title = data.get("title", f"Maidcore {idx+1}.0")
        playlist_tracks = data.get("tracks", [])

        track_ids = []

        for t in playlist_tracks:
            track_counter += 1
            tid = f"t{track_counter}"

            artist_name = t.get("user", {}).get("username", "Unknown artist")
            title = t.get("title", "Untitled")
            description = limpiar_descripcion(t.get("description"))

            # Guardar track
            catalog["tracks"][tid] = {
                "id": tid,
                "title": title,
                "artist": artist_name,
                "description": description,
                "playlist_ids": [playlist_id]
            }
            track_ids.append(tid)

            # Agregar al artista
            if artist_name not in catalog["artists"]:
                catalog["artists"][artist_name] = {
                    "name": artist_name,
                    "track_ids": [],
                    "playlist_ids": [],
                    "stats": {
                        "total_tracks": 0,
                        "distinct_playlists": 0,
                        "avg_description_length": 0
                    },
                    "tags": []  # futuro: puedes rellenar con IA
                }

            art = catalog["artists"][artist_name]
            art["track_ids"].append(tid)
            if playlist_id not in art["playlist_ids"]:
                art["playlist_ids"].append(playlist_id)

        # Guardar playlist
        catalog["playlists"].append({
            "id": playlist_id,
            "title": playlist_title,
            "url": url,
            "track_ids": track_ids
        })

    # Calcular estadísticas por artista
    for artist_name, art in catalog["artists"].items():
        track_ids = art["track_ids"]
        desc_lengths = []
        for tid in track_ids:
            desc = catalog["tracks"][tid]["description"]
            desc_lengths.append(len(desc))

        total_tracks = len(track_ids)
        distinct_playlists = len(art["playlist_ids"])
        avg_desc_len = sum(desc_lengths) / total_tracks if total_tracks > 0 else 0

        art["stats"]["total_tracks"] = total_tracks
        art["stats"]["distinct_playlists"] = distinct_playlists
        art["stats"]["avg_description_length"] = round(avg_desc_len, 2)

    return catalog


def guardar_catalogo_json(ruta="music_catalog.json"):
    catalog = generar_catalogo()
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"[+] Catálogo guardado en {ruta}")


if __name__ == "__main__":
    guardar_catalogo_json()
