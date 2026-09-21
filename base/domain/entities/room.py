"""
OBJETO DE DOMINIO ROOM, CONCEPTO DE NEGOCIO 'SALA'. NO NECESITA SABER
NADA SI USAMOS DJANGO O QUE TIPO DE BASE DE DATOS. ESTO ES EL OBJETO DE DOMINIO
"""

from dataclasses import dataclass

VALID_TOPICS = ["Programacion", "Juegos", "Deporte"]

@dataclass
class Room:
  name: str
  host_id: int
  topic: str
  host_username: str = ""
  description: str = ""
  id: int = None