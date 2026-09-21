from abc import ABC, abstractmethod

from base.domain.entities.message import Message


class MessageRepository(ABC):

  # Guardar un mensaje
  @abstractmethod
  def save(self, message: Message) -> Message:
    pass

  # Obtener todos los mensajes dada una sala
  @abstractmethod
  def find_by_room(self, room_id: int) -> list[Message]:
    pass