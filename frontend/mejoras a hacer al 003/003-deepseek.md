Vamos a integrar la funcionalidad de reproducción con Blob (similar a la del admin dashboard) en la página front-end con estilo Windows XP. También debemos ajustar la estructura de datos de las canciones para que puedan incluir archivos blob o rutas a archivos reales. El front-end actual tiene una lista fija de canciones. Lo modificaremos para que use datos similares a los del admin, pero con soporte para Blob. Además, debemos replicar la función playInHeader adaptada a este reproductor.

Pasos:

Crear una estructura de datos de canciones que incluya un campo file (nombre) y opcionalmente un blob. En el front-end actual no hay subida de archivos, así que probablemente usaremos archivos locales o rutas. Podemos simular con archivos de ejemplo y usar el mismo mecanismo de blob si se suben, pero en esta página no hay formulario de subida. Así que mantendremos la lista actual y añadiremos una ruta de audio real (por ejemplo, archivos en una carpeta). Para que funcione con blob, necesitaríamos tener los archivos realmente, pero podemos simular usando URLs de ejemplo (por ejemplo, de SoundHelix) o usar blob con datos de ejemplo.

Pero el usuario quiere implementar la función playInHeader que usa blob y ruta. En esta página no hay subida de archivos, así que probablemente quiera usar archivos predefinidos con rutas relativas. Podemos modificar el array songs para incluir una propiedad file que sea la ruta al archivo (por ejemplo, en una carpeta audio/). Luego en playSong usaremos esa ruta para reproducir con un elemento <audio> oculto o similar.

El front-actual no tiene un elemento <audio> en el HTML. En el admin dashboard se usa <audio id="header-player">. Aquí tenemos un display de texto, pero no un reproductor de audio real. Para que funcione, necesitamos añadir un elemento <audio> invisible o visible. Podemos añadirlo dentro del reproductor, pero manteniendo la estética.

Propuesta: Añadir un elemento <audio> oculto y controlarlo con JavaScript. Al hacer clic en Play, cargar la canción actual y reproducir. Actualizar el display con el tiempo.

También debemos mantener la compatibilidad con blob si hubiera archivos subidos, pero en esta página no hay subida. Podemos dejar la función playInHeader adaptada: si existe un blob para la canción (lo cual no será el caso), usar ese; si no, usar una ruta base.

Vamos a modificar el HTML para incluir un <audio> oculto justo después del display o en el body. Luego adaptar las funciones.

Además, en el admin dashboard hay un objeto fileBlobs que asocia clave con blob URL. En el front-end, podríamos tener un objeto similar si se implementara subida, pero no es necesario ahora. Podemos simular que las canciones tienen una propiedad file que es la ruta. Usaremos una ruta base como ../media/mp3/real mp3/... similar al admin. Pero como no tenemos esos archivos, podemos usar URLs públicas de ejemplo (por ejemplo, de archive.org o SoundHelix) para que suene algo. O usar tonos generados con Web Audio API.

Para simplificar, usaremos un array de canciones con URLs de ejemplo (MP3 de muestra). Por ejemplo, usar el mismo recurso de SoundHelix.

Implementación:

Añadir elemento <audio id="audio-player" style="display: none;"></audio>.

En playSong(), obtener la canción actual, determinar la fuente: si existe blob para esa canción, usar; si no, usar URL base + nombre de archivo (o una URL fija). Podemos definir una propiedad url en cada canción.

Actualizar el display con información.

También necesitamos manejar eventos de tiempo para actualizar el display con el tiempo transcurrido/duración. Podemos usar timeupdate y loadedmetadata.

Vamos a reescribir el script para integrar todo.

Además, el usuario quiere que sea "lo más simple posible", así que no necesitamos toda la complejidad del admin dashboard, solo la función de reproducción adaptada. Pero debemos mantener el estilo Windows XP.

Voy a generar el código completo con las modificaciones.

He integrado la funcionalidad de reproducción con Blob (similar a tu admin dashboard) en la página de estilo Windows XP. Ahora el reproductor usa un elemento <audio> oculto y puede reproducir tanto archivos locales como blobs. La lista de canciones ahora incluye rutas de ejemplo (usando archivos de SoundHelix para que funcionen directamente). Además, he añadido un Map para simular blobs (aunque en esta demo no se suben archivos, la estructura está preparada).

html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MaidCore Player</title>
    <link rel="icon" type="image/x-icon" href="https://raw.githubusercontent.com/BryanGF-hg/Proyecto-FloVViDex/refs/heads/main/Images/Logo/medevil%20100x100.png">    
    <style>
      * {margin: 0; padding: 0; box-sizing: border-box; font-family: "Tahoma","Arial",sans-serif; font-size: 11px;}
      body {background-image: url('https://raw.githubusercontent.com/BryanGF-hg/Proyecto-FloVViDex/refs/heads/main/Images/wallpaper/wallpaper-v0-ww00n61..._imresizer.png'); height: 100vh; overflow: hidden;}

      .window {width: 300px; height: 400px; background-color: #c0c0c0; border: 2px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); box-shadow: 4px 4px 10px rgba(0,0,0,0.5);}
      .window-title {padding-left: 5px;}
      .window-content {padding: 10px; height: calc(100% - 28px); overflow: auto;}
      .window-controls {display: flex;}
      .title-bar {background: linear-gradient(135deg,#000080,#F2F7F2); color: white; padding: 4px; height: 28px; display: flex; align-items: center; justify-content: space-between; font-weight: bold; font-size: 12px;}

      .control-btn {width: 20px; height: 20px; margin-left: 2px; background-color: #c0c0c0; border: 1px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 10px; cursor: pointer;}
      .control-btn:active {border-top-color: #808080; border-left-color: #808080; border-right-color: #fff; border-bottom-color: #fff;}

      .player {background-color: #c0c0c0; border: 2px inset; padding: 15px; margin-bottom: 15px; height: 120px;}
      .player-display {background-color: black; color: #00ff00; padding: 10px;font-family: "Courier New", monospace; font-size: 12px; overflow: hidden; border: 1px inset;}
      .player-controls {display: flex; justify-content: center; gap: 8px; margin-bottom: 15px;}
      .player-btn {width: 100px; height: 25px; background-color: #c0c0c0; border: 2px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080; cursor: pointer; font-size: 10px; font-weight: bold;}
      .player-btn:active {border-top-color: #808080; border-left-color: #808080; border-right-color: #fff; border-bottom-color: #fff;}

      .playlist {background-color: white; border: 2px inset; height: 215px; overflow-y: auto; margin-top: -5px; padding: 5px;}
      .playlist-item {padding: 3px 5px; cursor: pointer; border-bottom: 1px dotted #c0c0c0;}
      .playlist-item:hover {background-color: #000080; color: white;}
      .playlist-item.active {background-color: #000080; color: white; font-weight: bold;}

      .taskbar {position: fixed; bottom: 0; left: 0; width: 100%; height: 40px; background-color: #c0c0c0; border-top: 2px solid #fff; display: flex; align-items: center; padding: 0 5px;}
      .taskbar-items {display: flex; gap: 5px; flex-grow: 1;}
      .taskbar-item {background-color: #c0c0c0; border: 2px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080; padding: 5px 10px; min-width: 120px; cursor: pointer; font-size: 10px;}
      .taskbar-item.active {border-top-color: #808080; border-left-color: #808080; border-right-color: #fff; border-bottom-color: #fff;}

      .start-btn {width: 80px; height: 30px; background-color: #c0c0c0; border: 2px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080; display: flex; align-items: center; padding: 0 8px; font-weight: bold; font-size: 12px; cursor: pointer; margin-right: 10px;}
      .start-btn:active {border-top-color: #808080; border-left-color: #808080; border-right-color: #fff; border-bottom-color: #fff;}
      .start-icon {background-color: #008080; color: white; width: 16px; height: 16px; display: flex; align-items: center; justify-content: center; margin-right: 5px; font-weight: bold;}

      .clock {background-color: #c0c0c0; border: 2px inset; padding: 5px 10px; font-size: 11px; min-width: 100px; text-align: center; margin-left: 10px;}

      ::-webkit-scrollbar {width: 16px;}
      ::-webkit-scrollbar-track {background-color: #c0c0c0; border: 1px inset;}
      ::-webkit-scrollbar-thumb {background-color: #c0c0c0; border: 2px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080;}
      ::-webkit-scrollbar-button {background-color: #c0c0c0; border: 1px solid; border-top-color: #fff; border-left-color: #fff; border-right-color: #808080; border-bottom-color: #808080; height: 16px;}

      .bold {font-weight: bold;}
      .blue {color: #000080;}
    </style>
</head>
<body>
    <!-- Elemento de audio oculto -->
    <audio id="audio-player" style="display: none;"></audio>

    <!-- VENTANA PRINCIPAL -->
    <div class="window">
        <div class="title-bar">
            <div class="window-title">MaidCore Player v1.0</div>
            <div class="window-controls">
                <div class="control-btn">_</div>
                <div class="control-btn">□</div>
                <div class="control-btn">X</div>
            </div>
        </div>
        
        <div class="window-content">
            <!-- REPRODUCTOR -->
            <div class="player">
                <div class="player-display" id="display">
                    MaidCore Player - Ready<br>
                    -----------------------<br>
                    Now Playing: [Stopped]<br>
                    Time: 00:00 / 00:00
                </div>
                
                <div class="player-controls">
                    <button class="player-btn" onclick="playSong()">▶ Play</button>
                    <button class="player-btn" onclick="pauseSong()">⏸ Pause</button>
                    <button class="player-btn" onclick="stopSong()">⏹ Stop</button>
                    <button class="player-btn" onclick="prevSong()">⏮ Prev</button>                    
                    <button class="player-btn" onclick="nextSong()">⏭ Next</button>
                </div>
                
                <div class="playlist" id="playlist">
                    <div style="font-weight: bold; margin-bottom: 5px;">Playlist:</div>                
                    <!-- Los items se generarán dinámicamente desde JavaScript -->
                </div>
            </div>
        </div>
    </div>

    <!-- BARRA DE TAREAS (TASKBAR) -->
    <div class="taskbar">
        <div class="start-btn" onclick="toggleStartMenu()">
            <div class="start-icon">M</div>
            Start
        </div>
        
        <div class="taskbar-items">
            <div class="taskbar-item active" onclick="focusWindow()">MaidCore Player</div>
            <div class="taskbar-item" onclick="openExplorer()">🗀 Song of the Week</div>
            <div class="taskbar-item" onclick="openBrowser()"><> Paint</div>
        </div>
        
        <div class="clock" id="clock">14:25:37</div>
    </div>

    <script>
        // Elementos del DOM
        const audioPlayer = document.getElementById('audio-player');
        const display = document.getElementById('display');
        const playlistContainer = document.getElementById('playlist');

        // Variables del reproductor
        let currentSong = 0;
        let isPlaying = false;

        // Estructura de canciones con campo file (nombre de archivo) y opcionalmente blobKey
        // Usaremos URLs de ejemplo de SoundHelix para que suenen realmente
        const songs = [
            { 
                title: "Sakura Electronica - Cherry Blossom Dreams", 
                duration: "3:45",
                file: "SoundHelix-Song-1.mp3",
                url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
            },
            { 
                title: "Kawaii Circuit - Digital Heartbeat", 
                duration: "4:12",
                file: "SoundHelix-Song-2.mp3",
                url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
            },
            { 
                title: "Maid² - Binary Love", 
                duration: "3:28",
                file: "SoundHelix-Song-3.mp3",
                url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
            },
            { 
                title: "Tokyo Wave - Neon Streets", 
                duration: "5:01",
                file: "SoundHelix-Song-4.mp3",
                url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
            },
            { 
                title: "Valencia Otaku Ensemble - Mediterranean Maid", 
                duration: "4:33",
                file: "SoundHelix-Song-5.mp3",
                url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
            }
        ];

        // Mapa para almacenar Blob URLs (simulación, aquí no se usan pero la estructura está lista)
        const fileBlobs = new Map(); // clave: nombre de archivo, valor: blob URL

        // Función para obtener la URL de reproducción (similar a playInHeader del admin)
        function getTrackUrl(track) {
            // Si existe un blob para este track (por nombre de archivo), usarlo
            if (fileBlobs.has(track.file)) {
                return fileBlobs.get(track.file);
            }
            // Si no, usar la URL predefinida (o ruta local)
            return track.url; // también podrías usar una ruta base como `../media/mp3/real mp3/${folderName}/${track.file}`
        }

        // Reproducir la canción actual
        function playSong() {
            const track = songs[currentSong];
            const url = getTrackUrl(track);
            audioPlayer.src = url;
            audioPlayer.play()
                .then(() => {
                    isPlaying = true;
                    updateDisplay();
                })
                .catch(err => {
                    console.error('Error al reproducir:', err);
                    display.innerHTML = `MaidCore Player - Error<br>-----------------------<br>No se pudo reproducir el archivo.`;
                });
        }

        function pauseSong() {
            audioPlayer.pause();
            isPlaying = false;
            updateDisplay();
        }

        function stopSong() {
            audioPlayer.pause();
            audioPlayer.currentTime = 0;
            isPlaying = false;
            updateDisplay();
        }

        function nextSong() {
            currentSong = (currentSong + 1) % songs.length;
            if (isPlaying) {
                playSong(); // Reproduce automáticamente si ya estaba sonando
            } else {
                updateDisplay();
            }
            updatePlaylist();
        }

        function prevSong() {
            currentSong = (currentSong - 1 + songs.length) % songs.length;
            if (isPlaying) {
                playSong();
            } else {
                updateDisplay();
            }
            updatePlaylist();
        }

        function selectSong(index) {
            currentSong = index;
            if (isPlaying) {
                playSong();
            } else {
                updateDisplay();
            }
            updatePlaylist();
        }

        // Actualizar el display con información de la canción y el tiempo
        function updateDisplay() {
            const track = songs[currentSong];
            const status = isPlaying ? "Playing" : "Stopped";
            let currentTime = "00:00";
            let duration = track.duration;

            if (audioPlayer.duration && !isNaN(audioPlayer.duration)) {
                // Formatear tiempo
                const format = (seconds) => {
                    const mins = Math.floor(seconds / 60);
                    const secs = Math.floor(seconds % 60);
                    return `${mins}:${secs.toString().padStart(2, '0')}`;
                };
                currentTime = format(audioPlayer.currentTime);
                duration = format(audioPlayer.duration);
            }

            display.innerHTML = 
                `MaidCore Player - ${status}<br>-----------------------<br>Now Playing: ${track.title}<br>Time: ${currentTime} / ${duration}`;
        }

        // Actualizar la lista visual (marcar la canción activa)
        function updatePlaylist() {
            const items = document.querySelectorAll('.playlist-item');
            items.forEach((item, index) => {
                if (index === currentSong) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        }

        // Renderizar la lista de canciones en el DOM
        function renderPlaylist() {
            let html = '<div style="font-weight: bold; margin-bottom: 5px;">Playlist:</div>';
            songs.forEach((song, index) => {
                const activeClass = index === currentSong ? 'active' : '';
                html += `<div class="playlist-item ${activeClass}" onclick="selectSong(${index})">${String(index+1).padStart(2,'0')}. ${song.title}</div>`;
            });
            playlistContainer.innerHTML = html;
        }

        // Eventos del audio para actualizar el display
        audioPlayer.addEventListener('timeupdate', updateDisplay);
        audioPlayer.addEventListener('loadedmetadata', updateDisplay);
        audioPlayer.addEventListener('play', () => {
            isPlaying = true;
            updateDisplay();
        });
        audioPlayer.addEventListener('pause', () => {
            isPlaying = false;
            updateDisplay();
        });
        audioPlayer.addEventListener('ended', () => {
            isPlaying = false;
            updateDisplay();
            // Opcional: pasar a la siguiente canción automáticamente
            nextSong();
        });

        // Funciones de la interfaz (sin cambios)
        function toggleStartMenu() {
            alert('[Start Menu]\n\nPrograms:\n• MaidCore Player\n• MaidCore Explorer\n• MaidCore Browser\n\nDocuments\n• Settings\n• Help\n• About\n\nShut Down...');
        }

        function focusWindow() {
            document.querySelector('.window').style.zIndex = '1000';
        }

        function openExplorer() {
            alert('Opening MaidCore Explorer...\n\nLocal Files:\nC:\\MaidCore\\\n│── Artists\\\n│── Music\\\n│── Events\\\n│── Merch\\\n│── Community\\');
        }

        function openBrowser() {
            alert('Opening MaidCore Browser...\n\nConnecting to: http://maidcore-valencia.es\n\nFeatured:\n• Artist Profiles\n• Event Tickets\n• Community Forum\n• Online Store');
        }

        // Reloj
        function updateClock() {
            const now = new Date();
            const time = now.toLocaleTimeString('es-ES', { hour12: false });
            document.getElementById('clock').textContent = time;
        }
        setInterval(updateClock, 1000);
        updateClock();

        // Arrastre de ventana (igual)
        let isDragging = false;
        let offsetX, offsetY;
        const windowEl = document.querySelector('.window');
        const titleBar = document.querySelector('.title-bar');

        titleBar.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDrag);

        function startDrag(e) {
            isDragging = true;
            offsetX = e.clientX - windowEl.offsetLeft;
            offsetY = e.clientY - windowEl.offsetTop;
            windowEl.style.cursor = 'move';
        }

        function drag(e) {
            if (!isDragging) return;
            windowEl.style.left = (e.clientX - offsetX) + 'px';
            windowEl.style.top = (e.clientY - offsetY) + 'px';
        }

        function stopDrag() {
            isDragging = false;
            windowEl.style.cursor = 'default';
        }

        // Controles de ventana
        document.querySelectorAll('.control-btn').forEach((btn, index) => {
            btn.addEventListener('click', function() {
                if (index === 0) { // Minimizar
                    windowEl.style.display = 'none';
                    document.querySelector('.taskbar-item').textContent = 'MaidCore Player [Minimized]';
                } else if (index === 1) { // Maximizar/Restaurar
                    if (windowEl.style.width === '100%') {
                        windowEl.style.width = '300px';
                        windowEl.style.height = '400px';
                        windowEl.style.top = '50%';
                        windowEl.style.left = '50%';
                        windowEl.style.transform = 'translate(-50%, -50%)';
                    } else {
                        windowEl.style.width = '100%';
                        windowEl.style.height = 'calc(100vh - 40px)';
                        windowEl.style.top = '0';
                        windowEl.style.left = '0';
                        windowEl.style.transform = 'none';
                    }
                } else if (index === 2) { // Cerrar
                    if (confirm('Close MaidCore Player?')) {
                        windowEl.style.display = 'none';
                        document.querySelector('.taskbar-item').textContent = 'MaidCore Player [Closed]';
                        document.querySelector('.taskbar-item').classList.remove('active');
                    }
                }
            });
        });

        // Restaurar ventana desde taskbar
        document.querySelector('.taskbar-item').addEventListener('click', function() {
            windowEl.style.display = 'block';
            this.textContent = 'MaidCore Player';
            this.classList.add('active');
        });

        // Inicialización
        renderPlaylist();
        updateDisplay();
    </script>
</body>
</html>
Principales cambios:
Añadido elemento <audio> oculto con id audio-player.

Estructura de datos songs ahora incluye file (nombre) y url (ruta de ejemplo de SoundHelix para que suene algo real). También está preparada para usar blobs mediante el mapa fileBlobs (aunque en esta demo no se usa, la función getTrackUrl ya lo soporta).

Función playSong adaptada: obtiene la URL (blob o ruta) y la asigna al audio.

Eventos de audio para actualizar el display en tiempo real (timeupdate, loadedmetadata, etc.).

Actualización del display muestra el tiempo transcurrido/duración real.

Reproducción automática al cambiar de canción si ya estaba sonando.

Playlist generada dinámicamente desde JavaScript para facilitar cambios.

Ahora el reproductor funciona exactamente igual que el del admin dashboard pero con el estilo retro Windows XP. Puedes probarlo directamente (las URLs de SoundHelix son válidas). Si en el futuro quieres usar archivos locales o blobs, solo tienes que modificar getTrackUrl y poblar fileBlobs.
