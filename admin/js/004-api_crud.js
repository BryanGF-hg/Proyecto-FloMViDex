// ============================================
  // 4. FUNCIONES DE API (CRUD)
  // ============================================
  
  // 4.1 GET /api/tracks
  async function fetchTracks(dir) {
    try {
      const res = await fetch(`${API_BASE}/api/tracks?dir=${encodeURIComponent(dir)}`);
      if (!res.ok) throw new Error('Error al cargar tracks');
      const data = await res.json();
      tracksByDirectory[dir] = data;
      loadTracks();
    } catch (e) {
      console.error('Error en fetchTracks:', e);
      tracksByDirectory[dir] = [];
      loadTracks();
    }
  }
  
  // 4.2 PUT /api/tracks (editar metadata)
  const editTrack = async id => {
    const arr = tracksByDirectory[currentDirectory];
    const track = arr.find(t => t.id === id);
    if (!track) return;

    const newTitle = prompt('Nuevo título:', track.title || '');
    if (newTitle === null) return;
    const newArtist = prompt('Nuevo artista:', track.artist || '');
    if (newArtist === null) return;
    const newTagsStr = prompt(
      'Nuevos tags (separados por comas):',
      Array.isArray(track.tags) ? track.tags.join(', ') : (track.tags || '')
    );
    if (newTagsStr === null) return;

    const newTags = newTagsStr.split(',').map(t => t.trim()).filter(Boolean);

    const payload = {
      title: newTitle.trim() || track.title,
      artist: newArtist.trim(),
      tags: newTags
    };

    try {
      const res = await fetch(
        `${API_BASE}/api/tracks/${currentDirectory}/${id}`,
        {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }
      );
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        alert('Error al editar: ' + (err.detail || res.status));
        return;
      }
      const updatedTrack = await res.json();
      const idx = arr.findIndex(t => t.id === id);
      if (idx > -1) {
        arr[idx] = updatedTrack;
      }
      loadTracks();
    } catch (e) {
      console.error('Error en editTrack:', e);
      alert('Error de red al editar track');
    }
  };
  
  // 4.3 DELETE /api/tracks (individual)
  const deleteTrack = async id => {
    if (!confirm(`¿Eliminar el track con ID ${id} en ${currentDirectory}?`)) return;

    try {
      const res = await fetch(
        `${API_BASE}/api/tracks/${currentDirectory}/${id}`,
        { method: 'DELETE' }
      );
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        alert('Error al eliminar: ' + (err.detail || res.status));
        return;
      }
      tracksByDirectory[currentDirectory] =
        (tracksByDirectory[currentDirectory] || []).filter(t => t.id !== id);
      loadTracks();
    } catch (e) {
      console.error('Error en deleteTrack:', e);
      alert('Error de red al eliminar track');
    }
  };
