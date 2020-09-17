from VectorClock import VectorClock
from typing import Any


class CRDTEntry():
  """
  A entry in the CRDT state data structure
  """
  def __init__(self, value: Any, version: VectorClock = VectorClock(0)):
    self.value: Any = value
    self.version = version
