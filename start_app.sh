#!/bin/bash
set -e

echo "Levantando la aplicacio web y su base de datos de desarrollo"
docker compose up -d --build web db # Esto levantará los contenedores en segundo plano y construirá las imágenes si es necesario.

echo "Mostrando logs del servicio web"
docker compose logs -f web # Esto mostrará los logs del contenedor web en tiempo real. Puedes detener la visualización de logs con Ctrl+C.
