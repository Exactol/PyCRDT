from Op import Op
from OpType import OpType

class Store:
    def __init__(self, id = 0):
        self.state = {}
        self.history = []
        self.ids = (0,) # vector clock to hold ids
        self.id = id

    def merge(self, op: OpType):
        # TODO: ignore duplicates

        # update id vector clock
        self.ids = [max(id, newId) for id, newId in zip(self.ids, op.id)]
        if (op.opType == OpType.Add):
            self.state[op.id] = op.value
        else:
            raise "Not implemented"

        self.history.append(op)

    def add(self, value):
        newId = self.createId()
        op = Op(OpType.Add, newId, value)
        self.merge(op)
        # TODO: send out op update

    def createId(self):
        newId = list(self.ids)
        newId[self.id] += 1
        return tuple(newId)