Perfecto. Vamos a integrarlo correctamente.

Ahora mismo tu front-end no reproduce audio real: solo simula estados.
Lo que necesitas es:

Añadir un <audio> real al front.

Reemplazar el sistema songs[] ficticio por objetos compatibles con tu backend.

Adaptar la lógica de playInHeader al reproductor Win98.

Te lo explico paso a paso, con código listo para pegar.

1️⃣ Añade un <audio> real al Front-End

Dentro de .player, justo debajo de .player-display, añade:

<audio id="audio-player"></audio>

No hace falta controls, porque usas botones personalizados.

2️⃣ Sustituye el array songs

Ahora mismo tienes:

let songs = [
    { title: "...", duration: "3:45" }
];

Eso hay que cambiarlo por algo compatible con tu backend:

let songs = [
    { 
        id: 1,
        title: "Cherry Blossom Dreams",
        artist: "Sakura Electronica",
        file: "cherry.mp3"
    },
    { 
        id: 2,
        title: "Digital Heartbeat",
        artist: "Kawaii Circuit",
        file: "digital.opus"
    }
];

⚠️ Importante: esto debe venir idealmente desde un JSON exportado por tu backend (luego te explico cómo conectarlo real).

3️⃣ Adaptar la lógica de playInHeader al Front

Añade arriba de tus funciones:

const audioPlayer = document.getElementById('audio-player');

const DIR_PATHS = {
    mc1: 'maidcore 1.0',
    mc2: 'maidcore 2.0',
    mc3: 'maidcore 3.0',
    mc4: 'maidcore 4.0'
};

let currentDirectory = 'mc1'; // o dinámico
4️⃣ Reemplaza completamente playSong()

Tu nueva función real sería:

function playSong() {
    const track = songs[currentSong];

    const folderName = DIR_PATHS[currentDirectory] || currentDirectory;

    audioPlayer.src = `../media/mp3/real mp3/${folderName}/${track.file}`;

    audioPlayer.play().then(() => {
        isPlaying = true;
        updateDisplay();
    }).catch(err => {
        console.error("Error reproduciendo:", err);
    });
}
5️⃣ Corrige pause y stop
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
6️⃣ Actualizar tiempo REAL (esto es clave)

Tu sistema actual finge duración. Vamos a hacerlo profesional.

Añade:

audioPlayer.addEventListener('timeupdate', () => {
    updateDisplay();
});

audioPlayer.addEventListener('loadedmetadata', () => {
    updateDisplay();
});

Y reemplaza updateDisplay() por:

function formatTime(seconds) {
    const m = Math.floor(seconds / 60) || 0;
    const s = Math.floor(seconds % 60) || 0;
    return `${m}:${s.toString().padStart(2, '0')}`;
}

function updateDisplay() {
    const status = isPlaying ? "Playing" : "Stopped";

    const current = formatTime(audioPlayer.currentTime || 0);
    const total = formatTime(audioPlayer.duration || 0);

    document.getElementById('display').innerHTML = 
        `MaidCore Player - ${status}<br>
        -----------------------<br>
        Now Playing: ${songs[currentSong].title}<br>
        Time: ${current} / ${total}`;
}

Ahora el tiempo es REAL.

7️⃣ Integrar soporte para Blob (como tu backend)

Si quieres que el front también soporte archivos subidos dinámicamente (blob URLs), necesitas un mapa igual que en el admin:

const fileBlobs = {}; // clave: id

Y en playSong:

function playSong() {
    const track = songs[currentSong];

    if (fileBlobs[track.id]) {
        audioPlayer.src = fileBlobs[track.id];
    } else {
        const folderName = DIR_PATHS[currentDirectory] || currentDirectory;
        audioPlayer.src = `../media/mp3/real mp3/${folderName}/${track.file}`;
    }

    audioPlayer.play().then(() => {
        isPlaying = true;
        updateDisplay();
    });
}
8️⃣ Si quieres hacerlo realmente conectado al backend

La forma correcta (profesional) sería:

En tu backend:

fetch('/api/tracks?dir=mc1')
  .then(res => res.json())
  .then(data => {
      songs = data;
      renderPlaylist();
  });

Pero eso ya implica backend real (Node, PHP, etc).
