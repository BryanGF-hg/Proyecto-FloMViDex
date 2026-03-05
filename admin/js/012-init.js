  // ============================================
  // 15. INICIALIZACIÓN
  // ============================================
  (async () => {
    await loadTranslations();
    applyTranslations();
    updateDirectoryLabel();
    fetchTracks(currentDirectory);
  })();
