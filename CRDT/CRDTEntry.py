from VectorClock import VectorClock
from typing import Any

class CRDTEntry():
  """
  A entry in the CRDT state data structure
  """
  def __init__(self, value: Any, clock: VectorClock = None):
    self.value: Any = value
    self.clock = clock if clock is not None else VectorClock()

  def __repr__(self):
    return f"{self.value}@{self.clock}"