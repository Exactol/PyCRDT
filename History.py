from Ops.Op import Op
from typing import List

class History():
  def __init__(self):
    self.history: List[Op] = []

  def append(self, op: Op):
    # TODO: sort by version only when needed? could be better for performance

    # insert history in correct order by Vector clock versioning
    for i, item in enumerate(self.history):
      insert = True
      for user_id, version in op.id.vector.items():
        if user_id in item.id.vector and item.id.vector[user_id] <= version:
          insert = False
          break

      if (insert):
        self.history.insert(i, op)
        return

    self.history.append(op)

  def __iter__(self):
    return iter(self.history)