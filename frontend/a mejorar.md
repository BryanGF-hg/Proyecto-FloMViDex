        // Generar títulos de canciones (simulado)
        function generateSongTitle(index, artist) {
            const titles = [
                'Digital Dreams', 'Neon Paradise', 'Cherry Blossom', 
                'Midnight Cafe', 'Electric Heart', 'Virtual Love',
                'Cyberpunk Maid', 'Tokyo Rain', 'Starlight', 'Eternal Promise',
                'Binary Emotion', 'Quantum Wave', 'Crystal Tears', 'Maidcore Anthem'
            ];
            return `${artist} - ${titles[index % titles.length]} ${Math.floor(index / titles.length) + 1}`;
        }
