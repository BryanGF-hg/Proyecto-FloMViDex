  // ============================================
  // 12. EXPORTAR JSON
  // ============================================
  if (exportJsonBtn) {
    exportJsonBtn.addEventListener('click', () => {
      const data = tracksByDirectory[currentDirectory] || [];
      console.log('JSON exportado para', currentDirectory, JSON.stringify(data,null,2));
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
  extensionFilter.addEventListener('change', () => {
    if (extensionFilter.value === "global") {
        // Si elige global, llamamos a la API con dir=all
        currentDirectory = "all"; 
        fetchTracks("all");
        dirLabel.querySelector('h3').textContent = "Resultados Globales:";
    } else {
        // Lógica normal de filtrado por extensión si no es global
        loadTracks(); 
    }
  
