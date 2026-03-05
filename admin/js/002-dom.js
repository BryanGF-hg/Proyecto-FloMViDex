  // ============================================
  // 2. ELEMENTOS DEL DOM
  // ============================================
  const tabs = document.querySelectorAll('.tab');
  const tableBody = document.querySelector('#tracks-table tbody');
  const dirLabel = document.getElementById('current-directory-label');
  const createForm = document.getElementById('create-form');
  const searchInput = document.getElementById('search-input');
  const extensionFilter = document.getElementById('extension-filter');
  const headerPlayer = document.getElementById('header-player');
  const playerInfo = document.getElementById('player-info');
  const deleteSelectedBtn = document.getElementById('delete-selected-btn');
  const exportJsonBtn = document.getElementById('export-json-btn');
  const selectAllCheckbox = document.getElementById('select-all');
