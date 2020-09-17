from typing import Dict

# TODO: comparison might be wrong: https://www.youtube.com/watch?v=OOlnp2bZVRs
class VectorClock():
  """
  A vector clock used for causality
  """
  def __init__(self, user_id: int, vector: Dict[int, int] = None):
    self.user_id = user_id
    if vector:
      self.vector = vector.copy()
      if user_id not in self.vector:
        self.vector[user_id] = 0
    else:
      self.vector = {user_id: 0}

  # doesnt mutate original object. We only want to set a new version once an update has been merged
  def increment(self):
    """
    Returns a new VectorClock with a incremented value based on user id
    """
    newVector = self.vector.copy()
    if self.user_id in newVector:
        newVector[self.user_id] += 1
    else:
        newVector[self.user_id] = 0
    return VectorClock(self.user_id, newVector)

  def merge(self, new_vector):
    """
    Merges two vector clocks
    """
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
    return not self == vector

  def __lt__(self, vector):
    if (self == vector):
      return False

    # ensure that shared user id versions come before
    isBefore = all(self.vector[user_id] <= vector.vector[user_id] for user_id, _ in zip(self.vector.keys(), vector.vector.keys()))

    # if before, make sure other vector doesnt have extra keys
    if isBefore:
      # if other vector contains more keys, it is older
      isBefore = len(self.vector.keys()) <= len(vector.vector.keys())
    return isBefore

  def __gt__(self, vector):
    return not self < vector

  def __le__(self, vector):
    return self < vector or self == vector

  def __ge__(self, vector):
    return self > vector or self == vector

  def __str__(self):
    return f"Vector Version: {str(self.vector)}"

  def __repr__(self):
    return str(self.vector)