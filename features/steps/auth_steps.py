from behave import given, when, then
from django.test import Client
from bs4 import BeautifulSoup

@given('que existe un usuario registrado con username "{username}" y password "{password}"')
def step_existing_user(context, username, password):
  context.client = Client()
  response = context.client.post("/register/", {
      "username": username,
      "password1": password,
      "password2": password,
  })

  # Cerramos sesion para dejarlo registrado pero no logueado
  context.client.get("/logout/")

@when('el usuario completa el formulario de registro con username "{username}" y password "{password}"')
def step_register(context, username, password):
  # Si el cliente no existe, lo creamos
  if not hasattr(context, 'client'):
    context.client = Client()
  context.response = context.client.post("/register/", {
      "username": username,
      "password1": password,
      "password2": password,
  })

@when('el usuario completa el formulario de login con username "{username}" y password "{password}"')
def step_login(context, username, password):
  context.response = context.client.post("/login/", {
      "username": username,
      "password": password,
  })

@when('el usuario cierra sesion')
def step_logout(context):
  context.response = context.client.get("/logout/")

@then('el usuario es redirigido al home estando autenticado')
def step_redirected_home_authenticated(context):
  assert context.response.status_code == 302
  response = context.client.get("/")
  assert response.status_code == 200
  soup = BeautifulSoup(response.content, 'html.parser')
  # Verificamos que el usuario este autenticado buscando el boton de logout
  logout_button = soup.find('a', string='Logout')
  assert logout_button is not None, "El usuario no está autenticado, no se encontró el botón de logout en la página de inicio"

@then('el usuario ve un mensaje de error en el formulario de registro')
def step_error_in_register_form(context):
  assert context.response.status_code == 200
  soup = BeautifulSoup(context.response.content, 'html.parser')
  error_message = soup.find('ul', class_='errorlist')
  assert error_message is not None, "No se encontró un mensaje de error en el formulario de registro"

@then('el usuario ve un mensaje de error en el formulario de login')
def step_error_in_login_form(context):
  assert context.response.status_code == 200
  soup = BeautifulSoup(context.response.content, 'html.parser')
  error_message = soup.find('ul', class_='messages')
  assert error_message is not None, "No se encontró un mensaje de error en el formulario de login"

@then('el usuario es redirigido al home sin estar autenticado')
def step_redirected_home_unauthenticated(context):
  assert context.response.status_code == 302
  response = context.client.get("/")
  assert response.status_code == 200
  soup = BeautifulSoup(response.content, 'html.parser')
  # Verificamos que el usuario no este autenticado buscando el boton de login
  login_button = soup.find('a', string='Login')
  assert login_button is not None, "El usuario está autenticado, se encontró el botón de login en la página de inicio"

