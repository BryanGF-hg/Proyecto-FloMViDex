import json

result = []

for idx, line in enumerate(tracks_text.splitlines(), start=1):
    line = line.strip()
    if not line:
        continue
    # Prefer ' - ' delimiter; fallback to ' – '
    artist = None
    title = None
    if ' - ' in line:
        artist, title = line.split(' - ', 1)
    elif ' – ' in line:
        artist, title = line.split(' – ', 1)
    else:
        artist = ''
        title = line
    result.append({"id": idx, "artist": artist, "title": title})

print(json.dumps({"mc1": result}, ensure_ascii=False, indent=2))
