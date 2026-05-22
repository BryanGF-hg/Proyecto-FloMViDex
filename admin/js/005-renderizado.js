 // ============================================
  // 5. RENDERIZADO DE TABLA (loadTracks)
  // ============================================
  const loadTracks = () => {
    const term = searchInput.value.trim().toLowerCase();
    const mode = extensionFilter.value;
    
    tableBody.innerHTML = '';
    
    let sourceList = [];
    
    // Si el usuario elige búsqueda global o estamos en modo global
    if (mode === 'global' || currentDirectory === 'global') {
      sourceList = [];
      ['mc1', 'mc2', 'mc3', 'mc4'].forEach(dir => {
        const tracks = tracksByDirectory[dir] || [];
        sourceList.push(...tracks);
      });
    } else {
      sourceList = tracksByDirectory[currentDirectory] || [];
    }
    
    // Ordenar por ID
    sourceList.sort((a, b) => a.id - b.id);
    
    const filtered = sourceList.filter(track => {
      const title = (track.title || '').toLowerCase();
      const file = (track.file || '').toLowerCase();
      const artist = (track.artist || '').toLowerCase();
      const tagsText = Array.isArray(track.tags) 
        ? track.tags.join(' ').toLowerCase() 
        : (track.tags || '').toLowerCase();
      
      const textMatch = !term || 
        title.includes(term) || 
        file.includes(term) || 
        artist.includes(term) || 
        tagsText.includes(term);
      
      let extMatch = true;
      if (mode === 'mp3') {
        extMatch = file.endsWith('.mp3');
      } else if (mode === 'opus') {
        extMatch = file.endsWith('.opus');
      }
      
      return textMatch && extMatch;
    });
    
    if (selectAllCheckbox) selectAllCheckbox.checked = false;
    
    if (!filtered.length) {
      const row = document.createElement('tr');
      const cell = document.createElement('td');
      cell.colSpan = 7;
      cell.textContent = t('no_tracks');
      cell.className = 'no-data';
      row.appendChild(cell);
      tableBody.appendChild(row);
      updateDirectoryLabel();
      return;
    }
    
    filtered.forEach(track => {
      const row = document.createElement('tr');
      
      // Selección
      const selectCell = document.createElement('td');
      selectCell.className = 'select-col';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.className = 'row-select';
      cb.dataset.id = track.id;
      selectCell.appendChild(cb);
      
      // ID
      const idCell = document.createElement('td');
      idCell.textContent = track.id;
      
      // Título
      const titleCell = document.createElement('td');
      titleCell.textContent = track.title;
      titleCell.addEventListener('dblclick', () => {
        const input = document.createElement('input');
        input.type = 'text';
        input.value = track.title;
        input.className = 'title-edit-input';
        titleCell.textContent = '';
        titleCell.appendChild(input);
        input.focus();
        const save = async () => {
          const val = input.value.trim();
          if (val && val !== track.title) {
            track.title = val;
            await editTrack(track.id);
          } else {
            loadTracks();
          }
        };
        input.addEventListener('blur', save);
        input.addEventListener('keydown', e => {
          if (e.key === 'Enter') input.blur();
          if (e.key === 'Escape') loadTracks();
        });
      });
      
      // Artista
      const artistCell = document.createElement('td');
      artistCell.textContent = track.artist || '-';
      
      // Tags
      const tagsCell = document.createElement('td');
      tagsCell.textContent = Array.isArray(track.tags) 
        ? track.tags.join(', ') 
        : (track.tags || '-');
      
      // Archivo
      const fileCell = document.createElement('td');
      fileCell.textContent = track.file;
      
      // Acciones
      const actionsCell = document.createElement('td');
      actionsCell.className = 'actions';
      const playBtn = document.createElement('button');
      playBtn.textContent = t('play_btn');
      playBtn.addEventListener('click', () => playInHeader(track));
      const editBtn = document.createElement('button');
      editBtn.textContent = t('edit_btn');
      editBtn.addEventListener('click', () => editTrack(track.id));
      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = t('delete_btn');
      deleteBtn.addEventListener('click', () => deleteTrack(track.id));
      
      actionsCell.appendChild(playBtn);
      actionsCell.appendChild(editBtn);
      actionsCell.appendChild(deleteBtn);
      
      row.appendChild(selectCell);
      row.appendChild(idCell);
      row.appendChild(titleCell);
      row.appendChild(artistCell);
      row.appendChild(tagsCell);
      row.appendChild(fileCell);
      row.appendChild(actionsCell);
      
      tableBody.appendChild(row);
    });
    
    updateDirectoryLabel();
  };
