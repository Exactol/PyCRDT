from json import JSONEncoder
from Ops.Op import Op
from Ops.OpType import OpType
from JSON.Payload import Payload

class OpSerializer(JSONEncoder):
  def default(self, object):
    if isinstance(object, Op) or isinstance(object, Payload):
      return object.__dict__
    elif isinstance(object, OpType):
      return object.value
    else:
      return JSONEncoder.default(self, object)