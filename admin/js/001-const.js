  // ============================================
  // 1. CONFIGURACIÓN Y CONSTANTES GLOBALES
  // ============================================
  const API_BASE = '';
  const DIR_PATHS = {
    mc1: 'maidcore 1.0',
    mc2: 'maidcore 2.0',
    mc3: 'maidcore 3.0',
    mc4: 'maidcore 4.0'
  };
  const emptyTracks = () => ({ mc1: [], mc2: [], mc3: [], mc4: [] });
  let tracksByDirectory = emptyTracks();
  let currentDirectory = 'mc1';
