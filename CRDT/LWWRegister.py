from CRDT.CmRDT import CmRDT
from CRDT.CRDTEntry import CRDTEntry
from VectorClock import VectorClock
from typing import Dict, Any
from Callback import Callback
from Ops.Op import Op
from Ops.SetOp import SetOp

class LWWRegister(CmRDT):
  """
  Last-Writer-Wins Register CRDT

  Holds an arbitrary value. The value is updated according to the timestamp of the Op
  """
  def __init__(self, initial_state: Any = None, initial_clock: VectorClock = VectorClock()):
    # TODO: does initial state need to be cloned
    self._state = initial_state
    self._clock = initial_clock.copy()
    self.on_update: Callback = Callback()
    # TODO: does this need initial_state?

  def apply(self, op: Op):
    """
    Applies an operation to the LWWRegister.
    Accepts: SetOp
    """
    # TODO: handle concurrent clocks. Ex. <1, 2>, <2, 1> Updates happen concurrently, need some kind of tie breaker. maybe assign user ids based on order joined or assign users priority?
    # TODO: should lww have a delete op?
    # TODO: implement undo op
    if isinstance(op, SetOp):
      # update the register if this operation has a newer clock
      if self.clock().get(op.clock_entry.identifier) < op.clock_entry.counter:
        self._state = op.value
        self._clock = self._clock.apply(op.clock_entry)

      # if clocks are equal but the value differs something went wrong
      elif self.clock().get(op.clock_entry.identifier) == op.clock_entry.counter and self.get() != op.value:
        raise Exception("Conflicting clocks")
      else:
        # op has older clock version, do nothing
        return
    else:
      raise Exception("Unsupported operation")

    self.on_update()

  def get(self):
    """
    Returns the value of the register.
    """
    # TODO: check if tombstoned?
    return self._state

  def clock(self):
    """
    Returns the clock of the register.
    """
    # TODO: check if tombstoned?
    return self._clock

  def clone(self):
    """
    Returns a new instance of LWWRegister with cloned values
    """
    return LWWRegister(self.get(), self.clock())

  def __str__(self):
    return f"{self.get()}@{self.clock()}"

  def __eq__(self, other):
    return isinstance(other, LWWRegister) and self._clock == other._clock and self._state == other._state