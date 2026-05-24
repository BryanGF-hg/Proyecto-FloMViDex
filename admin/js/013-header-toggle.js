  // ============================================
  // 16. TOGGLE DEL HEADER (ocultar/mostrar)
  // ============================================
  (function setupHeaderToggle() {
    const headerToggle = document.getElementById('header-toggle');
    
    if (!headerToggle) return;
    
    const body = document.body;
    
    // Función para actualizar el botón según el estado
    function updateToggleUI(isHidden) {
      if (isHidden) {
        headerToggle.textContent = '⬇️';
        headerToggle.title = 'Mostrar panel superior';
      } else {
        headerToggle.textContent = '⬆️';
        headerToggle.title = 'Ocultar panel superior';
      }
    }
    
    // Recuperar estado guardado
    const savedState = localStorage.getItem('flomvidex_header_hidden');
    
    if (savedState === 'true') {
      body.classList.add('header-hidden');
      updateToggleUI(true);
    } else {
      updateToggleUI(false);
    }
    
    // Evento click
    headerToggle.addEventListener('click', () => {
      const isCurrentlyHidden = body.classList.contains('header-hidden');
      
      if (isCurrentlyHidden) {
        body.classList.remove('header-hidden');
        updateToggleUI(false);
        localStorage.setItem('flomvidex_header_hidden', 'false');
      } else {
        body.classList.add('header-hidden');
        updateToggleUI(true);
        localStorage.setItem('flomvidex_header_hidden', 'true');
      }
    });
  })();
