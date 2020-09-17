from Ops.Op import Op
from Ops.OpType import OpType
from VectorClockEntry import VectorClockEntry
from VectorClock import VectorClock
from typing import Any, Dict
from CRDT.CRDTEntry import CRDTEntry

class SetOp(Op):
  """
  Sets the value of a field. Not commutative, but will converge using Last-Write-Wins
  """
  def __init__(self, field: str, value: Any, clock_entry: VectorClockEntry):
    super().__init__(field, value, OpType.Set, clock_entry)
    self.previous = None

  def apply(self, state: Dict[str, CRDTEntry], clock: VectorClock):
    # check if op has already been seen
    if clock.get(self.clock_entry.identifier) >= self.clock_entry.counter:
      return

    entry = state.get(self.field, CRDTEntry(None))

    # update clock of CRDTEntry
    entry.clock.apply(self.clock_entry)

    # TODO: check if nested CRDT?
    entry.value = self.value

    state[self.field] = entry
    # Update master clock
    clock.apply(self.clock_entry)
    return state

  def undo(self, state):
    # TODO: if previous is null, field didnt previously exist and should be tombstoned
    state[self.field] = self.previous
