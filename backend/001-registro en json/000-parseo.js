const fs = require('fs');
const input = `

`.trim().split('\n');

const mc = input.map((line, index) => {
  const separator = ' - ';  const sepIndex = line.indexOf(separator);
  let artist = '';  let title = line;

  if (sepIndex !== -1) {
    artist = line.slice(0, sepIndex);    title = line.slice(sepIndex + separator.length);
  }
  return {    id: index + 1,   artist,    title  };
});

const result = { mc };
console.log(JSON.stringify(result, null, 2));
fs.writeFileSync('artista-mc4.json', JSON.stringify(result, null, 2), 'utf8'); // Guardar en archivo artista-mcX.json
console.log('Archivo guardado como artista-mcX.json');

