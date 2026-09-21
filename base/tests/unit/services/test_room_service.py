"""
TESTS UNITARIOS ROOM SERVICE
"""

from unittest.mock import MagicMock

from base.domain.entities.room import Room
from base.domain.services.room_service import (
  InvalidTopicError,
  RoomService,
  UnauthorizedError,
)


# Test crear sala con topic valido
def test_create_room_with_valid_topic():
  mock_repository = MagicMock() # El mock simula un repositorio sin necesidad de usar una base de datos real, todo en memoria
  # Hacemos que el repositorio falso cuando alguien le llame .save() devuelva esa sala
  mock_repository.save.return_value = Room(
    id=1,
    name="Sala Python",
    host_id=1,
    host_username="Bauti",
    topic="Programacion",
    description="Una sala de python"
  )

  # Esta es la accion que queremos testear, instanciamos RoomService pasandole el repositorio falso
  service = RoomService(repository=mock_repository)
  # Creamos una sala usando el servicio, que internamente llama save() al repositorio falso
  result = service.create_room(
    name="Sala Python",
    host_id=1,
    topic="Programacion",
    description="Una sala de python"
  )

  # el create_room() internamente llama a save() en el repositorio. Recordar
  # que el create_room() devuelve la sala que creamos
  assert result.id == 1
  assert result.name == "Sala Python"
  assert result.topic == "Programacion"
  mock_repository.save.assert_called_once()

# Test crear sala con topico invalido
def test_create_room_with_invalid_topic():
  mock_repository = MagicMock()
  service = RoomService(repository=mock_repository)

  try:
    service.create_room(
      name="Sala Python",
      host_id=1,
      topic="TopicoInvalido",
      description="Esto es una sala de python",
    )
    assert False, "Deberia haber lanzado InvalidTopicError"
  except InvalidTopicError:
    pass

  mock_repository.save.assert_not_called() # No deberia haberse llamado el assert. Si el test no lanza la excepcion el test falla

# Test eliminar sala como host
def test_delete_room_as_host():
  mock_repository = MagicMock()
  service = RoomService(repository=mock_repository)

  # Simulamos que la sala existe y pertenece al host
  mock_repository.find_by_id.return_value = Room(
    id=1,
    name="Sala Python",
    host_id=1,
    host_username="Bauti",
    topic="Programacion",
    description="Una sala de python"
  )

  # Eliminamos la sala usando el servicio, que internamente llama delete() al repositorio falso
  service.delete_room(room_id=1, requesting_user_id=1)

  # Verificamos que el metodo delete() del repositorio falso fue llamado con el id de la sala
  mock_repository.delete.assert_called_once_with(1) 

# Test eliminar sala como usuario que no es host
def test_delete_room_as_non_host():
  mock_repository = MagicMock()
  service = RoomService(repository=mock_repository)

  # Simulamos que la sala existe y pertenece a otro host
  mock_repository.get_by_id.return_value = Room(
    id=1,
    name="Sala Python",
    host_id=1,
    host_username="Bauti",
    topic="Programacion",
    description="Una sala de python"
  )

  try:
    service.delete_room(room_id=1, requesting_user_id=2) # Intentamos eliminar la sala con un usuario que no es el host
    assert False, "Deberia haber lanzado PermissionError"
  except UnauthorizedError:
    pass

  mock_repository.delete.assert_not_called() # No deberia haberse llamado el delete. Si el test no lanza la excepcion el test falla
