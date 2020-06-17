from CRDTStore import CRDTStore
from Ops import Op
from Server import ServerBase

class RemoteCRDTStore(CRDTStore):
  def __init__(self, server: ServerBase, user_id = 0, initial_version = None, initial = {}):
    super().__init__(user_id, initial_version, initial)

    self.server = server
    self.server.on_recieve += self.on_recieve

  def on_recieve(self, op: Op):
    # merge
    self.merge(op)

  def apply(self, op: Op):
    super().apply(op)

    # send op to clients
    if self.server is not None:
      self.server.send(op)