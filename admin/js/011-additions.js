  // ============================================
  // 12. EXPORTAR JSON
  // ============================================
  if (exportJsonBtn) {
    exportJsonBtn.addEventListener('click', () => {
      const data = tracksByDirectory[currentDirectory] || [];
      console.log('JSON exportado para', currentDirectory, JSON.stringify(data, null, 2));
      alert('JSON del directorio exportado a la consola (F12).');
    });
  }

  // ============================================
  // 13. CHECKBOX "SELECCIONAR TODO"
  // ============================================
  if (selectAllCheckbox) {
    selectAllCheckbox.addEventListener('change', () => {
      document.querySelectorAll('.row-select').forEach(cb => cb.checked = selectAllCheckbox.checked);
    });
  }

  // ============================================
  // 14. FILTROS DE BÚSQUEDA
  // ============================================
  searchInput.addEventListener('input', loadTracks);
  
  // Función auxiliar para cargar TODOS los tracks de todos los directorios
  async function fetchAllTracks() {
    try {
      const promises = ['mc1', 'mc2', 'mc3', 'mc4'].map(dir => 
        fetch(`${API_BASE}/api/tracks?dir=${encodeURIComponent(dir)}`)
          .then(res => res.json())
          .then(data => ({ dir, tracks: data }))
          .catch(err => ({ dir, tracks: [], error: err }))
      );
      
      const results = await Promise.all(promises);
      
      results.forEach(result => {
        tracksByDirectory[result.dir] = result.tracks;
      });
      
      loadTracks();
    } catch (e) {
      console.error('Error en fetchAllTracks:', e);
    }
  }
  
  extensionFilter.addEventListener('change', async () => {
    const selectedValue = extensionFilter.value;
    
    if (selectedValue === 'global') {
      // Modo búsqueda global: cargar todos los directorios
      currentDirectory = 'global';
      await fetchAllTracks();
      
      // Actualizar el label del directorio
      const h3 = dirLabel.querySelector('h3');
      if (h3) h3.textContent = t('current_dir') || 'Directorio actual:';
      dirLabel.innerHTML = `<h3>${t('current_dir') || 'Directorio actual:'}</h3> 🌍 Búsqueda Global`;
    } else if (selectedValue === 'mp3' || selectedValue === 'opus') {
      // Filtro por extensión en el directorio actual
      if (currentDirectory === 'global') {
        // Si venimos de búsqueda global, cargar el último directorio activo
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) {
          currentDirectory = activeTab.dataset.dir;
          await fetchTracks(currentDirectory);
        }
      }
      loadTracks();
    } else {
      // Modo normal (all)
      if (currentDirectory === 'global') {
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) {
          currentDirectory = activeTab.dataset.dir;
          await fetchTracks(currentDirectory);
        }
      }
      loadTracks();
    }
  });  // ← CIERRE DEL addEventListener
