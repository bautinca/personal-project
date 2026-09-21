"""
LOGICA DE NEGOCIO PURA. ACA VIVEN REGLAS DEL DOMINIO RESPECTO A LAS SALAS,
POR EJEMPLO "SOLO EL DUEÑO PUEDE EDITAR SUS SALAS O BORRARLAS"
RECIBE COMO INSTANCIA EL REPOSITORIO DE SALAS PARA LA PERSISTENCIA DE LAS SALAS Y ABSTRAYENDOSE DE QUE TIPO DE BASE DE DATOS
ES PARA PERSISTIR, SOLO SABE QUE HAY UN REPOSITORIO DE SALAS QUE TIENE CONTACTO CON LA DB
"""

from base.domain.entities.room import VALID_TOPICS, Room
from base.domain.repositories.room_repository import RoomRepository


class UnauthorizedError(Exception):
  pass

class RoomNotFoundError(Exception):
  pass

class InvalidTopicError(Exception):
  pass

class RoomService:

  def __init__(self, repository: RoomRepository):
    self._repository = repository

  def create_room(self, name: str, host_id: int, topic: str, description: str = "") -> Room:
    if topic not in VALID_TOPICS:
      raise InvalidTopicError(f"Topic invalido: {topic}")
    room = Room(name=name, host_id=host_id, topic=topic, description=description)
    return self._repository.save(room)

  def get_all_rooms(self) -> list[Room]:
    return self._repository.find_all()

  def get_room(self, room_id: int) -> Room:
    return self._repository.find_by_id(room_id)

  def update_room(self, room_id: int, requesting_user_id: int, name: str, topic: str, description: str = "") -> Room:
    if topic not in VALID_TOPICS:
      raise InvalidTopicError(f"Topic invalido: {topic}")
    room = self._repository.find_by_id(room_id)
    if room.host_id != requesting_user_id:
      raise UnauthorizedError("Solo el host puede editar esta sala")
    room.name = name
    room.topic = topic
    room.description = description
    return self._repository.save(room)

  def delete_room(self, room_id: int, requesting_user_id: int) -> None:
    room = self._repository.find_by_id(room_id)
    if room.host_id != requesting_user_id:
      raise UnauthorizedError("Solo el host puede borrar esta sala")
    self._repository.delete(room_id)