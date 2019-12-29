from Ops.AddOp import AddOp
from Ops.Op import Op
from Ops.OpType import OpType


class CRDTStore:
    def __init__(self, server = None, id = 0, initial = {}):
        self.state = initial
        self.initial_state = initial
        self.history = [] # TODO: make own class so history can be stored in order of version clock

        self.ids = (0,) # vector clock to hold all ids
        self.id = id # id of user

        self.server = server
        if server is not None:
            self.server.on_recieve += self.on_recieve

    def on_recieve(self, data):
        print(data)

    def merge(self, op: Op):
        # TODO: ignore duplicates

        # update id vector clock with maximum id for each id
        self.ids = [max(id, newId) for id, newId in zip(self.ids, op.id)]

        # apply and store history
        op.apply(self.state)
        self.history.append(op)

    def apply(self, op: Op):
        # merge op
        self.merge(op)

        # send op to clients
        if self.server is not None:
            self.server.send(op)

    def create_id(self):
        newId = list(self.ids)
        newId[self.id] += 1
        return newId
