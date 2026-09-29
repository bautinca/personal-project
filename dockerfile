# Contenedor individual para levantar un contenedor y dentro de ese contenedor
# Instalar todas las dependencias necesarias para usar Django
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Reemplazamos el runserver de Django por Gunicorn para produccion.
# ya que Runserver no es recomendado para produccion, Gunicorn en cambio 
# es un servidor WSGI que es más adecuado para entornos de producción.
# WSGI (Web Server Gateway Interface) es un estándar que define cómo los servidores web se comunican con las aplicaciones web escritas en Python. Gunicorn es un servidor WSGI que permite ejecutar aplicaciones web de manera eficiente y escalable.
# Entonces lo que hacemos en la sig linea es ejecutar Gunicorn y le pasamos como argumento el archivo wsgi.py de nuestro proyecto Django, que es el punto de entrada para la aplicación web. Además, le indicamos que escuche en todas las interfaces de red (0.0.0.0:8000)
# a traves del argumento --bind, lo que significa que la aplicación estará disponible en el puerto 8000 de la máquina donde se ejecute el contenedor.
CMD ["gunicorn", "personal_project.wsgi:application", "--bind", "0.0.0.0:8000"]