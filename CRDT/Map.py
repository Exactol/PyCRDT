from VectorClock import VectorClock
from History import History
from Ops import SetOp, Op, OpType
from json import loads
from Callback import Callback
from typing import Dict, Any, Tuple
from collections import namedtuple
from CRDT.CRDTEntry import CRDTEntry
from CRDT.CmRDT import CmRDT

class Map(CmRDT):
  """
  Map CRDT

  Compositions of CRDTS are themselves CRDTS. This means that the map can hold values that are CRDTs
  """
  def __init__(self, initial_state: Dict[str, CRDTEntry] = {}, initial_clock: VectorClock = VectorClock()):
    self._state: Dict[str, CRDTEntry] = initial_state.copy()
    self._initial_state: Dict[str, CRDTEntry] = initial_state.copy()

    # this clock is the current version of the CRDTStore and should be greater or equal to all entry clock values
    self._clock: VectorClock = initial_clock.copy()

    # TODO: make history a global provider
    # self.history: History = History()


    self.on_update: Callback = Callback()

  def apply(self, op: Op):
    """
    Applies an operation to the Map
    Accepts: SetOp
    """
    if isinstance(op, SetOp):
      # check if op has already been seen
      if self.clock().get(op.clock_entry.identifier) >= op.clock_entry.counter:
        return

      entry = self._state.get(op.field, CRDTEntry(None))

      # update clock of CRDTEntry
      entry.clock.apply(op.clock_entry)

      # if op is referenced a nested CRDT and the value is also an op, apply it
      if isinstance(entry.value, CmRDT) and isinstance(op.value, Op):
        entry.value.apply(op.value)
      else:
        entry.value = op.value

      # apply and store history
      # self.history.append(op)
      self._state[op.field] = entry
      # Update master clock
      self._clock.apply(op.clock_entry)
    else:
      raise Exception("Unsupported operation")

    self.on_update()

  def get(self, field: str):
    """
    Returns a field. Defaults to None if the field doesn't exist
    """
    # TODO: check if tombstoned?
    # TODO: should this return a default CRDTEntry instead of None?
    # TODO: should this throw an error instead of defaulting?
    return self._state.get(field, None)

  def clock(self):
    """
    Returns the map's clock
    """
    return self._clock

  def keys(self):
    pass