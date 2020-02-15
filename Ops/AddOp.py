from Ops.Op import Op
from Ops.OpType import OpType
from Ops.ProtoBuffers.AddOp_pb2 import AddOp as AddOp_pb2


class AddOp(Op):
  def __init__(self, id, field: str, value):
    super(AddOp, self).__init__(OpType.Add, id, field, value)

  def apply(self, state: dict):
    state[self.field] = (id, self.value)
    return state

  def undo(self, state):
    pass

  def from_proto(self, proto):
    pass

  def to_proto(self):
    proto = AddOp_pb2()
    proto.id = self.id
    return proto