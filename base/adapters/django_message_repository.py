from base import models
from base.domain.entities.message import Message
from base.domain.repositories.message_repository import MessageRepository


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

  def find_by_id(self, message_id: int) -> Message:
    orm_message = models.Message.objects.get(id=message_id)
    return Message(
      id=orm_message.id,
      room_id=orm_message.room_id,
      user_id=orm_message.user_id,
      user_username=orm_message.user.username,
      body=orm_message.body,
    )

  def delete(self, message_id: int) -> None:
    models.Message.objects.filter(id=message_id).delete()