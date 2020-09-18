from typing import Dict
from typing import Any
from VectorClockEntry import VectorClockEntry

# TODO: comparison might be wrong: https://www.youtube.com/watch?v=OOlnp2bZVRs
class VectorClock():
  """
  A vector clock used for causality
  """
  def __init__(self, vector: Dict[Any, int] = {}):
    if vector is not None:
      self.vector = vector.copy()
    else:
        self.vector = {}

  def get(self, identifier: Any):
    """
    Gets the clock value of an identifier, if it doesn't exist defaults to 0
    """
    return self.vector.get(identifier, 0)

  def entry(self, identifier: Any):
    """
    Return the VectorClockEntry for the identifier
    """
    return VectorClockEntry(identifier, self.get(identifier))

  # doesnt mutate original object. We only want to set a new version once an update has been merged
  def increment(self, identifier: Any):
    """
    Returns a new VectorClockEntry with a incremented value based on user id. Does not mutate the clock
    """
    # TODO: does identifier need to be cloned?
    return self.entry(identifier).increment()

  def apply(self, entry: VectorClockEntry):
    """
    Applies a VectorClockEntry to the clock. Clock is only updated if the new VectorClockEntry has a greater value than the existing one
    """
    # only apply if the entry is a newer version
    if self.get(entry.identifier) < entry.counter:
      self.vector[entry.identifier] = entry.counter

    return self

  # TODO: should there be a custom sort function?
  # VectorClocks have a partial order, so VectorClock A might not be comparable to VectorClock B and should return None.
  # This happens when A != B and !(A < B) and !(A > B)
  def concurrent(self, clock):
    """
    Determines if two vector clocks have diverged
    This happens when A != B and !(A < B) and !(A > B)
    """
    return (self != clock and not (self < clock) and not (self > clock))

  def __eq__(self, other):
    """
    VectorClock A == VectorClock B if all VectorClockEntries are equal
    """
    return self.vector == other.vector

  def __ne__(self, other):
    return not self == other

  def __lt__(self, other):
    """
    VectorClock A < VectorClock B if all counters in A are less than those in B, using the identifiers from A
    """
    return all(self.get(identifier) <= other.get(identifier) for identifier in self.vector.keys())

  def __gt__(self, other):
    """
    VectorClock A > VectorClock B if all counters in A are greater than those in B, using the identifiers from B
    """
    return all(self.get(identifier) >= other.get(identifier) for identifier in other.vector.keys())

  def __le__(self, other):
    return self < other or self == other

  def __ge__(self, other):
    return self > other or self == other

  def __str__(self):
    return f"v{str(self.vector)}"

  def __repr__(self):
    return str(self.vector)

  def copy(self):
    return VectorClock(self.vector)