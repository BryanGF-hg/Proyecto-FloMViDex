  // ============================================
  // 9. DELETE MÚLTIPLE (eliminar seleccionados)
  // ============================================
  if (deleteSelectedBtn) {
    deleteSelectedBtn.addEventListener('click', async () => {
      const checked = document.querySelectorAll('.row-select:checked');
      if (!checked.length) {
        alert('Selecciona al menos un track para eliminar');
        return;
      }
      if (!confirm(`¿Eliminar ${checked.length} track(s)?`)) return;
      
      const ids = Array.from(checked).map(cb => parseInt(cb.dataset.id, 10));
      let successCount = 0; let failCount = 0; let failedIds = [];
      
      deleteSelectedBtn.disabled = true;
      const originalText = deleteSelectedBtn.textContent;
      deleteSelectedBtn.textContent = `Eliminando 0/${ids.length}...`;     
      
      const idsToDelete = [...ids];
      for (let i = 0; i < idsToDelete.length; i++) {
        const id = idsToDelete[i];
        deleteSelectedBtn.textContent = `Eliminando ${i+1}/${idsToDelete.length}...`;
        
        try {
          const res = await fetch(
            `${API_BASE}/api/tracks/${currentDirectory}/${id}`,
            { method: 'DELETE' }
          );
          
          if (res.ok) {
            successCount++;
            tracksByDirectory[currentDirectory] = 
              tracksByDirectory[currentDirectory].filter(t => t.id !== id);
          } else {
            failCount++;  failedIds.push(id);
            const err = await res.json().catch(() => ({}));
            console.warn('Error al borrar', id, err.detail || res.status);
          }
        } catch (e) {
          failCount++;  failedIds.push(id);
          console.error('Error de red al borrar', id, e);
        }
        await new Promise(r => setTimeout(r, 50));
      }
      
      deleteSelectedBtn.disabled = false;
      deleteSelectedBtn.textContent = originalText;
      
      if (failCount === 0) {
        alert(`𖦏 ${successCount} tracks eliminados correctamente`);
      } else {
        alert(`☢️ Eliminados: ${successCount} | Fallos: ${failCount}\nIDs con error: ${failedIds.join(', ')}`);
      }

      loadTracks();
      await fetchTracks(currentDirectory);
    });
  }
