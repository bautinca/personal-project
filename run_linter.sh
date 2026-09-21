#!/bin/bash
set -e

echo "Corriendo linter Ruff..."
docker compose up -d --build web db
docker compose exec web ruff check .

echo "Linter finalizado"