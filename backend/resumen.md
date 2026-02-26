Con las versiones 001 a 012 (solo JS + localStorage)

Mono‑usuario
Los datos viven en el navegador, no en el servidor
No hay autenticación
No hay persistencia real
Muy difícil compartir información
No escalable a +1.000 tracks
No puedes usarlo en una instalación real (empresa, institución, red local)

 (Python FastAPI-backend + frontend JS)

Multiusuario, multi‑cliente
Todos leen/escriben en la misma base de datos (o JSON)
Metadatos centralizados
Archivos servidos desde carpetas reales
Control total: edición, borrado, seguridad
APIs claras como REST donde el frontend retro y el admin pueden conectarse a lo mismo
Escalable a miles de tracks y múltiples paneles

POST /api/tracks
Content-Type: multipart/form-data
PUT /api/tracks/{dir}/{id}
DELETE /api/tracks/{dir}/{id}
