  // ============================================
  // 6. EVENT LISTENERS DE PESTAÑAS (DIRECTORIOS)
  // ============================================
  let nextIdByDirectory = {mc1:1, mc2:1, mc3:1, mc4:1};  
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentDirectory = tab.dataset.dir;
      if (!tracksByDirectory[currentDirectory]) {
        tracksByDirectory[currentDirectory] = [];
        nextIdByDirectory[currentDirectory] = 1;
      }
      updateDirectoryLabel();
      fetchTracks(currentDirectory);
    });
  });

  // ============================================
  // 7. VARIABLES PARA PREVIEW (CREATE)
  // ============================================
  const filePreviews = new Map();  
