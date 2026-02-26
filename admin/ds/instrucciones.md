// Cambiar estas funciones:
async function loadTracks() {
  const response = await fetch(`/api/tracks/${currentDirectory}`);
  const data = await response.json();
  // render...
}

async function uploadFiles() {
  const formData = new FormData();
  // ... append files
  await fetch('/api/upload', { method: 'POST', body: formData });
}

async function deleteTrack(id) {
  await fetch(`/api/tracks/${id}`, { method: 'DELETE' });
}
