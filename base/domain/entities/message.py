from dataclasses import dataclass


@dataclass
class Message:
  room_id: int
  user_id: int
  user_username: str
  body: str
  id: int = None