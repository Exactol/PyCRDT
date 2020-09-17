from typing import Any

class VectorClockEntry():
  """
  An entry in the VectorClock which holds the current version for an identifier
  """
  def __init__(self, identifier: Any, counter: int = 0):
    self.identifier = identifier
    self.counter = counter

  def increment(self):
    # TODO: should identifier be cloned incase it is a type that isnt passed by copy
    return VectorClockEntry(self.identifier, self.counter + 1)

  def __eq__(self, other):
    return self.identifier == other.identifier and self.counter == other.counter

  def __ne__(self, other):
    return not self == other

  def __lt__(self, other):
    if self.identifier == other.identifier:
      return self.counter < other.counter

    return None

  def __gt__(self, other):
    result = self < other
    if result != None:
      return not result
    return result

  def __le__(self, other):
    result = self < other
    if result != None:
      return result or self == other

    result = self == other
    return result

  def __ge__(self, other):
    result = self < other
    if result != None:
      return result or self == other

    result = self == other
    return result

  def __str__(self):
    return f"{self.identifier}: {self.counter}"

  def __repr__(self):
    return str(self)