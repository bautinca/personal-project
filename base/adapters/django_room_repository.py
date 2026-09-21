"""
ES EL ADAPTADOR DEL PUERTO DE PERSISTENCIA USANDO ORM DE DJANGO.
ES EL UNICO LUGAR DEL PROYECTO DONDE EL DOMINIO TOCA LA BASE DE DATOS. SI MAÑANA CAMBIAMOS DE DJANGO A FASTAPI O DE POSTGRES A MYSQL
ENTONCES TOCARIAMOS ESTE ARCHIVO

ES LOGICO QUE COMO ESTA EN CONTACTO CON LA BASE DE DATOS POSTGRESQL ESTA POR FUERA DEL HEXAGONO EL ADAPTADOR
"""

from base import models
from base.domain.entities.room import Room
from base.domain.repositories.room_repository import RoomRepository


class DjangoRoomRepository(RoomRepository):

  def save(self, room: Room) -> Room:
      if room.id is None:
          orm_room = models.Room(
              name=room.name,
              host_id=room.host_id,
              topic=room.topic,
              description=room.description,
          )
      else:
          orm_room = models.Room.objects.get(id=room.id)
          orm_room.name = room.name
          orm_room.description = room.description
          orm_room.topic = room.topic

      orm_room.save()
      room.id = orm_room.id
      return room

  def find_by_id(self, room_id: int) -> Room:
    orm_room = models.Room.objects.get(id=room_id)
    return Room(
      id=orm_room.id,
      name=orm_room.name,
      host_id=orm_room.host_id,
      host_username=orm_room.host.username,
      topic=orm_room.topic,
      description=orm_room.description or "",
    )

  def delete(self, room_id: int) -> None:
    models.Room.objects.filter(id=room_id).delete()

  def find_all(self) -> list[Room]:
    return [
      Room(
        id=r.id,
        name=r.name,
        host_id=r.host_id,
        host_username=r.host.username,
        topic=r.topic,
        description=r.description or "",
      )
      for r in models.Room.objects.all()
    ]