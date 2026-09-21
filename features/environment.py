# En este archivo se definen los pasos de configuración del entorno de pruebas para el proyecto Django. Contiene configuraciones específicas para la ejecución de pruebas de comportamiento (BDD) utilizando la biblioteca behave.
import os

# Configuramos Django para que utilice el archivo de configuración de settings del proyecto. Esto es necesario para que behave pueda interactuar con la base de datos y otros componentes de Django durante las pruebas.
os.environ["DJANGO_SETTINGS_MODULE"] = "personal_project.settings"
# Ademas definimos variables de entorno para la base de datos de testing, que se utilizará durante la ejecución de las pruebas. Esto permite que las pruebas se ejecuten en un entorno aislado sin afectar la base de datos de desarrollo
os.environ["DB_NAME"] = os.environ.get("TEST_DB_NAME")
os.environ["DB_USER"] = os.environ.get("TEST_DB_USER")
os.environ["DB_PASSWORD"] = os.environ.get("TEST_DB_PASSWORD")
os.environ["DB_HOST"] = os.environ.get("TEST_DB_HOST")
os.environ["DB_PORT"] = "5432" # Usamos puerto interno del contenedor, siempre fijo

import django
# Inicializamos Django para que pueda cargar la configuración del proyecto y preparar el entorno de pruebas. Esto es necesario para que behave pueda interactuar con los modelos, vistas y otros componentes de Django durante las pruebas.
django.setup()

from django.test.utils import setup_test_environment
setup_test_environment()  # Configuramos el entorno de pruebas de Django para que las pruebas se ejecuten en un entorno controlado y aislado. Esto incluye la configuración de la base de datos de pruebas, la limpieza de datos entre pruebas y otras configuraciones necesarias para garantizar la consistencia y confiabilidad de las pruebas.

# Definimos un hook de behave que se ejecuta antes de todas las pruebas. Este hook se utiliza para realizar configuraciones adicionales necesarias para el entorno de pruebas, como la creación de la base de datos de pruebas y la aplicación de migraciones.
def before_all(context):
  from django.core.management import call_command
  from django.db import connection
  try:
    # Antes de todo intentamos verificar si la base de datos de pruebas ya está creada y accesible. Si no lo está, se lanzará una excepción y procederemos a crearla.
    with connection.cursor() as cursor:
      cursor.execute("SELECT 1 FROM django_migrations LIMIT 1;")  # Intentamos ejecutar una consulta simple para verificar si la base de datos de pruebas está disponible y accesible. Si la consulta falla, significa que la base de datos no está lista y debemos crearla.
  except Exception:
    # Si la base de datos de pruebas no está creada, la creamos utilizando el comando de gestión de Django. Esto asegura que la base de datos esté disponible para las pruebas.
    call_command("migrate", verbosity=0)  # Aplicamos las migraciones de la base de datos antes de ejecutar todas las pruebas para garantizar que la estructura de la base de datos esté actualizada y consistente con el estado esperado por las pruebas. Esto incluye la creación de tablas, la aplicación de cambios en los esquemas y otras configuraciones necesarias para garantizar que la base de datos esté lista para ser utilizada durante la ejecución de las pruebas.

# Definimos un hook de behave que se ejecuta después de todas las pruebas. Este hook se utiliza para realizar tareas de limpieza y restauración del entorno de pruebas, como la eliminación de la base de datos de pruebas y la restauración de configuraciones previas.
def after_all(context):
  pass # No hacemos nada

# Definimos un hook de behave que se ejecuta antes de cada escenario de prueba. Este hook se utiliza para realizar configuraciones adicionales necesarias para el entorno de pruebas, como la limpieza de datos entre escenarios y la preparación del entorno para cada escenario individual.
def before_scenario(context, scenario):
  from django.db import connection
  with connection.cursor() as cursor:
    tables = connection.introspection.table_names()
    for table in reversed(tables):
      cursor.execute(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE;')  # Limpiamos los datos de todas las tablas de la base de datos de pruebas antes de cada escenario para garantizar que cada escenario se ejecute en un entorno limpio y aislado. Esto incluye la eliminación de todos los registros existentes y el reinicio de los contadores de identidad para garantizar que los IDs generados sean consistentes entre escenarios.

# Definimos un hook de behave que se ejecuta antes de cada característica de prueba. Este hook se utiliza para realizar configuraciones adicionales necesarias para el entorno de pruebas, como la preparación del entorno para cada característica individual.
def before_feature(context, feature):
  pass # No hacemos nada