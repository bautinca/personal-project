#!/bin/bash
set -e

# Levanto los contenedores web + base de datos de testeo
echo "Levantando contenedores necesarios..."
docker compose up -d --build web db_test # Esto levantará los contenedores en segundo plano y construirá las imágenes si es necesario. Levanta los contenedores web + db_test para ejecutar las pruebas unitarias y de aceptación.

# Ejecutar pruebas unitarias dentro del contenedor web
echo "Ejecutando pruebas unitarias..."
docker compose exec web pytest base/tests/unit/ -v

# Ahora ejecutamos tests de aceptacion
echo "Ejecutando tests de aceptacion..."
docker compose exec web behave features/ -v

# Eliminamos el contenedor base de datos de testeo para limpiar el entorno
echo "Eliminando contenedor de base de datos de testing y su volumen..."
docker compose stop db_test # Detenemos el contenedor de base de datos de testing
docker compose rm -f db_test # Eliminamos el contenedor de base de datos de testing
docker volume rm personal_project_postgres_test_data 2>/dev/null || true # Eliminamos el volumen de datos de la base de datos de testing. Si el volumen no existe, ignoramos el error.

echo "Tests finalizados"