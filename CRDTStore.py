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
        self.history = [] # TODO: make own class so history can be stored in order of version clock

        self.ids = {} # vector clock to hold all ids
        self.user_id = user_id
        self.ids[self.user_id] = 0 # initialize vectorclock

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
        # TODO: ignore duplicates

        # update id vector clock with maximum id for each id
        for id, value in op.id.items():
            # must cast id to int, as ints cannot be JSON keys
            if id in self.ids:
                self.ids[int(id)] = max(self.ids[int(id)], value)
            else:
                self.ids[int(id)] = value

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

    def create_id(self):
        newIds = self.ids.copy()
        if self.user_id in newIds:
            newIds[self.user_id] += 1
        else:
            newIds[self.user_id] = 0
        return newIds

    def get(self, field: str):
        if field in self.state:
            return self.state[field][1] # TODO: check if tombstoned

        return None