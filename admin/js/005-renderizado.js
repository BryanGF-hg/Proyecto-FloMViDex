 // ============================================
  // 5. RENDERIZADO DE TABLA (loadTracks)
  // ============================================
  const loadTracks = () => {
    const currentList = tracksByDirectory[currentDirectory] || [];
    currentList.sort((a, b) => a.id - b.id);
    tableBody.innerHTML = '';

    const term = searchInput.value.trim().toLowerCase();
    const ext = extensionFilter.value;

    const filtered = currentList.filter(t => {
      const title = (t.title || '').toLowerCase();
      const file = (t.file || '').toLowerCase();
      const artist = (t.artist || '').toLowerCase();
      const tagsText = Array.isArray(t.tags) ? t.tags.join(' ').toLowerCase() : (t.tags || '').toLowerCase();

      const textMatch =
        !term ||
        title.includes(term) ||
        file.includes(term) ||
        artist.includes(term) ||
        tagsText.includes(term);

      const extMatch = ext === 'all' ? true : file.split('.').pop() === ext;

      return textMatch && extMatch;
    });

    if (selectAllCheckbox) selectAllCheckbox.checked = false;

    if (!filtered.length) {
      const row = document.createElement('tr');
      const cell = document.createElement('td');
      cell.colSpan = 7;
      cell.textContent = 'No hay tracks en este directorio con el filtro actual.';
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
            await editTrackTitleOnly(track.id, val);
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
      tagsCell.textContent = Array.isArray(track.tags) ? track.tags.join(', ') : (track.tags || '-');

      // Archivo
      const fileCell = document.createElement('td');
      fileCell.textContent = track.file;

      // Acciones
      const actionsCell = document.createElement('td');
      actionsCell.className = 'actions';
      const playBtn = document.createElement('button');
      playBtn.textContent = 'Reproducir';
      playBtn.addEventListener('click', () => playInHeader(track));
      const editBtn = document.createElement('button');
      editBtn.textContent = 'Editar';
      editBtn.addEventListener('click', () => editTrack(track.id));
      const deleteBtn = document.createElement('button');
      deleteBtn.textContent = 'Eliminar';
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
