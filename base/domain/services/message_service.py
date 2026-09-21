from base.domain.entities.message import Message
from base.domain.repositories.message_repository import MessageRepository


class MessageService:

  def __init__(self, repository: MessageRepository):
    self._repository = repository

  # Logica de enviar un mensaje
  def send_message(self, room_id: int, user_id: int, user_username: str, body: str) -> Message:
    message = Message(
      room_id=room_id,
      user_id=user_id,
      user_username=user_username,
      body=body,
    )
    return self._repository.save(message)

  # Logica de obtener mensajes de una sala
  def get_room_messages(self, room_id: int) -> list[Message]:
    return self._repository.find_by_room(room_id)

