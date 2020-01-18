from VectorClock import VectorClock
from History import History
from Ops.AddOp import AddOp
from Ops.Op import Op
from Ops.OpType import OpType
from json import loads
from JSON.Payload import Payload
from Callback import Callback


class CRDTStore:
    def __init__(self, server = None, user_id = 0, initial = {}):
        self.state = initial
        self.initial_state = initial
        # self.history = [] # TODO: make own class so history can be stored in order of version clock
        self.history = History()

        self.ids = {} # vector clock to hold all ids
        self.user_id = user_id
        # self.ids[self.user_id] = 0 # initialize vectorclock
        self.version = VectorClock(user_id)

        self.server = server
        if server is not None:
            self.server.on_recieve += self.on_recieve

        self.on_update = Callback()

    def on_recieve(self, payload: Payload):
        # deserialize
        op: Op = payload.deserialize()
        # merge
        self.merge(op)

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

        # send op to clients
        if self.server is not None:
            self.server.send(op)

    def get(self, field: str):
        if field in self.state:
            return self.state[field][1] # TODO: check if tombstoned

        return None