"""
TEST UNITARIOS MESSAGE SERVICE
"""

from unittest.mock import MagicMock

from base.domain.entities.message import Message
from base.domain.services.message_service import MessageService

# Test crear mensaje con contenido valido
def test_send_message():
  mock_repository = MagicMock() # El mock simula un repositorio sin necesidad de usar una base de datos real, todo en memoria
  # Hacemos que el repositorio falso cuando alguien le llame .save() devuelva ese mensaje
  mock_repository.save.return_value = Message(
    id=1,
    room_id=1,
    user_id=1,
    user_username="Bauti",
    body="Hola, este es un mensaje de prueba"
  )

  # Esta es la accion que queremos testear, instanciamos MessageService pasandole el repositorio falso
  service = MessageService(repository=mock_repository)
  # Creamos un mensaje usando el servicio, que internamente llama save() al repositorio
  result = service.send_message(
    room_id=1,
    user_id=1,
    user_username="Bauti",
    body="Hola, este es un mensaje de prueba"
  )

  # el send_message() internamente llama a save() en el repositorio. Recordar
  # que el send_message() devuelve el mensaje que creamos
  assert result.id == 1
  assert result.user_username == "Bauti"
  assert result.body == "Hola, este es un mensaje de prueba"
  mock_repository.save.assert_called_once()

# Test para obtener mensajes de una sala
def test_get_room_messages():
  mock_repository = MagicMock()
  # Hacemos que el repositorio falso cuando alguien le llame .get_by_room_id() devuelva una lista de mensajes
  mock_repository.find_by_room.return_value = [
    Message(
      id=1,
      room_id=1,
      user_id=1,
      user_username="Bauti",
      body="Hola, este es un mensaje de prueba"
    ),
    Message(
      id=2,
      room_id=1,
      user_id=2,
      user_username="Juan",
      body="Hola Bauti, este es otro mensaje de prueba"
    )
  ]

  service = MessageService(repository=mock_repository)
  result = service.get_room_messages(room_id=1)

  assert len(result) == 2
  assert result[0].user_username == "Bauti"
  assert result[1].user_username == "Juan"
  assert result[0].body == "Hola, este es un mensaje de prueba"
  assert result[1].body == "Hola Bauti, este es otro mensaje de prueba"
  mock_repository.find_by_room.assert_called_once_with(1)