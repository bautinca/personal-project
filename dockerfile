# Contenedor individual para levantar un contenedor y dentro de ese contenedor
# Instalar todas las dependencias necesarias para usar Django
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]