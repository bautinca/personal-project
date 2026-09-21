"""
ES EL PUERTO. DEFINE QUE NECESITA EL DOMINIO PARA PERSISTIR LAS SALAS SIN SABER EL COMO SE HACE YA QUE ESTO ES
EL DOMINIO (DE ESO SE ENCARGA EL ADAPTADOR COMO HACERLO, OSEA django_room_repository.py)

SIEMPRE ES CLASE ABSTRACTA PURA, NO IMPORTA SI ES DJANGO O POSTGRES, NADA
"""

from abc import ABC, abstractmethod
from base.domain.entities.room import Room

class RoomRepository(ABC):

  @abstractmethod
  def save(self, room: Room) -> Room:
    pass

  @abstractmethod
  def find_by_id(self, room_id: int) -> Room:
    pass

  @abstractmethod
  def delete(self, room_id: int) -> None:
    pass

  @abstractmethod
  def find_all(self) -> list[Room]:
    pass