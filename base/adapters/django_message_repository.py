from base.domain.entities.message import Message
from base.domain.repositories.message_repository import MessageRepository
from base import models

class DjangoMessageRepository(MessageRepository):

  def save(self, message: Message) -> Message:
    orm_message = models.Message(
      room_id=message.room_id,
      user_id=message.user_id,
      body=message.body,
    )
    orm_message.save()
    message.id = orm_message.id
    return message

  def find_by_room(self, room_id: int) -> list[Message]:
    return [
      Message(
        id=m.id,
        room_id=m.room_id,
        user_id=m.user_id,
        user_username=m.user.username,
        body=m.body,
      )
      for m in models.Message.objects.filter(room_id=room_id)
    ]