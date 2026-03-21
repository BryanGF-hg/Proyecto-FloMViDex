  // ============================================
  // 3. FUNCIONES DE UTILIDAD BÁSICA
  // ============================================
  // Funcion de actualizacion de Directorios
  function updateDirectoryLabel() {
    const allTracks = tracksByDirectory[currentDirectory] || [];          
    const totalTracks = allTracks.length; 
    dirLabel.innerHTML = '<h3>Directorio actual:</h3> '+currentDirectory + ' Tracks: ' + totalTracks;
  }
  
  const playInHeader = track => {
    headerPlayer.src = `${API_BASE}/media/${currentDirectory}/${encodeURIComponent(track.file)}`;
    headerPlayer.play().catch(() => {});
    if (playerInfo) {
      playerInfo.textContent =
        (track.title || 'Sin título') + ' – ' +
        (track.artist || '') + ' (' + track.file + ')';
    }
  };
  
  // Funcion de contador total  
  async function fetchGlobalStats() {
      try {
          const res = await fetch(`${API_BASE}/api/stats`);
          const data = await res.json();
          const counterEl = document.getElementById('global-counter');
          if (counterEl) {
              counterEl.innerHTML = `Total en BD: <strong>${data.total_global}</strong> canciones`;
          }
      } catch (e) {
          console.error("Error al obtener stats:", e);
      }
  }  
