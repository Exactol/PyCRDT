from VectorClock import VectorClock
from History import History
from Ops.AddOp import AddOp
from Ops.Op import Op
from Ops.OpType import OpType
from json import loads
from Callback import Callback

class CRDTStore:
    def __init__(self, user_id = 0, initial_version = None, initial = {}):
        self.state = initial
        self.initial_state = initial
        self.history = History()

        self.user_id = user_id
        self.version = VectorClock(user_id, initial_version)

        self.on_update = Callback()

    def merge(self, op: Op):
        # TODO: ignore duplicates?

        # update version
        self.version.merge(op.id)

        # apply and store history
        self.state = op.apply(self.state)
        self.history.append(op)

        self.on_update()

    def apply(self, op: Op):
        # merge op
        self.merge(op)

    def get(self, field: str):
        if field in self.state:
            return self.state[field][1] # TODO: check if tombstoned

        return None