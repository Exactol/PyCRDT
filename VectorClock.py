from typing import Dict

class VectorClock():
  def __init__(self, user_id, vector: Dict = None):
    self.user_id = user_id
    if vector:
      self.vector = vector
    else:
      self.vector = {user_id: 0}

  # doesnt mutate original object. We only want to set a new version once an update has been merged
  def increment(self):
    newVector = self.vector.copy()
    if self.user_id in newVector:
        newVector[self.user_id] += 1
    else:
        newVector[self.user_id] = 0
    return VectorClock(self.user_id, newVector)

  def merge(self, new_vector):
    # update id vector clock with maximum id for each id
    for id, value in new_vector.vector.items():
        # must cast id to int, as ints cannot be JSON keys
        if id in self.vector:
            self.vector[int(id)] = max(self.vector[int(id)], value)
        else:
            self.vector[int(id)] = value

  def __eq__(self, vector):
    return self.vector == vector.vector

  def __ne__(self, vector):
    return self.vector != vector.vector

  def __lt__(self, vector):
    if (self.vector == vector.vector):
      return False

    isBefore = False

    for user_id in zip(self.vector.items(), vector.vector.items()):
      print(user_id)
      pass
    # print(list(zip(self.vector, vector.vector)))

    # for user_id, version in self.vector:


  def __gt__(self, vector):
    pass

  def __str__(self):
    return f"Vector Version: {str(self.vector)}"