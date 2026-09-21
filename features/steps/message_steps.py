from behave import then, when
from bs4 import BeautifulSoup


@when('el usuario entra a la sala "{name}" y envia el mensaje "{body}"')
def step_enter_room_and_send_message(context, name, body):
  response = context.client.get("/")
  assert response.status_code == 200

  soup = BeautifulSoup(response.content, 'html.parser')
  room_link = soup.find('a', string=name, href=True)
  assert room_link is not None, f"No se encontró el enlace de la sala '{name}'"

  room_url = room_link['href']
  response = context.client.get(room_url)
  assert response.status_code == 200, f"Error al acceder a la sala: got {response.status_code}"

  response = context.client.post(room_url, {
      "body": body,
  })
  assert response.status_code == 302, f"Error al enviar mensaje: got {response.status_code}"

  context.room_url = room_url  # Guardamos la URL de la sala en el contexto para usarla en el siguiente paso

@then('el mensaje "{body}" aparece en la sala "{name}"')
def step_message_visible(context, body, name):
  response = context.client.get(context.room_url)
  assert response.status_code == 200
  assert body.encode() in response.content, f"El mensaje '{body}' no aparece en la sala '{name}'"

@when('el usuario no registrado entra a la sala "{name}"')
def step_non_registered_user_enters_room(context, name):
  response = context.client.get("/")
  assert response.status_code == 200

  soup = BeautifulSoup(response.content, 'html.parser')
  room_link = soup.find('a', string=name, href=True)
  assert room_link is not None, f"No se encontró el enlace de la sala '{name}'"

  room_url = room_link['href']
  response = context.client.get(room_url)
  assert response.status_code == 200, f"Error al acceder a la sala: got {response.status_code}"

  context.response = response  # Guardamos la respuesta en el contexto para usarla en el siguiente paso

@then('no ve el formulario para enviar mensajes')
def step_non_message_form_visible(context):
  soup = BeautifulSoup(context.response.content, 'html.parser')
  form = soup.find('form')
  assert form is None, "El usuario no registrado deberia no ver el formulario para enviar mensajes en la sala"