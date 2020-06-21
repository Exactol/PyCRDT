from CRDTStore import CRDTStore
from Ops import Op
from Server import ServerProvider
from typing import Union

class RemoteCRDTStore(CRDTStore):
  def __init__(self, server: ServerProvider, user_id = 0, initial_version = None, initial = {}):
    super().__init__(user_id, initial_version, initial)

    self.server = server
    self.server.on_recieve += self.on_recieve

    self.server.initialize()

  def on_recieve(self, op: Union[Op, str]):
    if (isinstance(op, Op)):
      self.merge(op)

    # elif (op == "__INITIALIZE__"):


  def apply(self, op: Op):
    super().apply(op)

    # send op to clients
    self.server.send(op)