# Arquitectura del Sistema
El proyecto utiliza una arquitectura Client-Server desacoplada:

Backend: FastAPI (Python) actuando como API REST.

Base de Datos: MySQL (Relacional) para persistencia de tracks y registros de acceso con una base.

Frontend: HTML5, CSS3 (diseño retro Win95/XP) y JavaScript Vanilla.

Servidor de Archivos: FastAPI gestiona la entrega de archivos estáticos y multimedia.

# Requisitos e Instalación
## Dependencias de Python:

    pip install fastapi uvicorn pymysql python-multipart qrcode gunicorn
    
## Configuración de Base de Datos:
La primera tabla, tracks , contiene la siguiente estructura:

id (INT, PK, AI)
title (VARCHAR)
artist (VARCHAR)
tags (TEXT)
file (VARCHAR) - Nombre del archivo físico.
dir (VARCHAR) - Categoría (mc1, mc2, mc3, mc4).    

## Endpoints de la API (app.py)
**GET /api/tracks?dir={nombre}**: Devuelve un JSON con las canciones de un directorio o todas (all).

**POST /api/tracks**: Sube archivos físicos y registra metadatos en MySQL.

**GET /api/stats**: Devuelve el conteo total de canciones y el desglose por categorías.

**DELETE /api/tracks/{id}**: Elimina el registro en BD y el archivo físico.

**POST /api/registro-acceso**: Guarda logs de usuarios (Entradas/Salidas/Comentarios)

## Estructura de Archivos
**/media/**: Almacenamiento organizado de archivos .mp3 y .opus.

**/frontend/**: Contiene el Player (index.html) y el Dashboard de administración.

**/js/**: Lógica dividida en módulos (CRUD, Renderizado, Reproductor).
