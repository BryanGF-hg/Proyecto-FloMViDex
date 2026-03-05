 // ============================================
  // 8. CREATE - SUBIR TRACKS (con contador)
  // ============================================
  createForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = createForm.querySelector('button[type="submit"]');
    if (submitBtn.disabled) return;
    
    const fd = new FormData(createForm);
    const files = fd.getAll('file');
    const originalText = submitBtn.textContent;
    let successCount = 0; let failCount = 0;    
    submitBtn.disabled = true;  
    
    // Mostrar previews inmediatos
    files.forEach((file, i) => {
      const previewUrl = URL.createObjectURL(file);
      const previewId = `preview_${Date.now()}_${i}`;
      filePreviews.set(previewId, previewUrl);
    });
    
    // Subida real al servidor
    for (let i= 0; i < files.length; i++) {
      const file = files[i];
      submitBtn.textContent = `Subiendo ${i+1}/${files.length}...`;  
      const formData = new FormData();
      formData.append('dir', currentDirectory);
      formData.append('file', file);
      formData.append('title', fd.get('title') || '');
      formData.append('artist', fd.get('artist') || '');
      formData.append('tags', fd.get('tags') || '');
      
      try {
        const res = await fetch(`${API_BASE}/api/tracks`, {
          method: 'POST',
          body: formData
        });
        
        if (res.ok) { successCount++;
        } else { failCount++; }
      } catch(e) { 
        failCount++; 
        console.error('Error subiendo:', e);
        console.warn(`Error $[res.status] en archivo ${file.name}`);
      }
    }    
    
    // Limpiar previews
    filePreviews.forEach((url, id) => {
      URL.revokeObjectURL(url);
      filePreviews.delete(id);
    });
    
    createForm.reset();

    // Mostrar resultado
    if (failCount === 0) { 
      submitBtn.textContent = `𖦏 ${successCount} subidos`;
      setTimeout(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }, 5000);  
    } else { 
      submitBtn.textContent = `☢️  Subidos: ${successCount}, Fallos: ${failCount}`;
      setTimeout(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      }, 10000);  
    }  
    
    await fetchTracks(currentDirectory);
  });
