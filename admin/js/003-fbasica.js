  // ============================================
  // 3. FUNCIONES DE UTILIDAD BÁSICA
  // ============================================
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
