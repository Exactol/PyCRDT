from CRDTStore import CRDTStore
from Ops import Op, InitializeOp
from Server import ServerBase

class RemoteCRDTStore(CRDTStore):
  def __init__(self, server: ServerBase, user_id = 0, initial_version = None, initial = {}):
    super().__init__(user_id, initial_version, initial)

    self.server: ServerBase = server
    self.server.on_recieve += self.on_recieve

    self.server.send(InitializeOp())

  def on_recieve(self, op: Op):
    # merge
    self.merge(op)

    if (isinstance(op, InitializeOp)):
      print("INITIALIZE RECIEVED")

  def apply(self, op: Op):
    super().apply(op)

    # send op to clients
    if self.server is not None:
      self.server.send(op)