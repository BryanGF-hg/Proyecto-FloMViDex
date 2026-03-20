#!/bin/bash

# 1. Definición de rutas con comillas
SOURCE="/var/www/html/1DAM/@CEAC/[Proyecto] FloMViDex/backend/data/tracks.json"
DEST_DIR="/var/www/html/1DAM/@CEAC/[Proyecto] FloMViDex/backend/backups"
DATE=$(date +%d-%m-%Y_%H%M)

# 2. Crea el directorio de destino donde la ruta es una sola cadena
mkdir -p "$DEST_DIR"

# 3. Comprueba si el origen existe y copia usando comillas en origen y destino
if [ -f "$SOURCE" ]; then
    # Usamos comillas dobles para que cp vea UNA sola ruta, no varias palabras
    cp "$SOURCE" "$DEST_DIR/tracks_backup_$DATE.json"
    
    # Verifica si el comando anterior fue exitoso
    if [ $? -eq 0 ]; then
        echo "LOG: Backup exitoso el $DATE"
        echo "Ruta: $DEST_DIR/tracks_backup_$DATE.json"
    else
        echo "ERROR: Falló la copia del archivo."
        exit 1
    fi
else
    echo "ERROR: El archivo original no existe en: $SOURCE"
    exit 1
fi
