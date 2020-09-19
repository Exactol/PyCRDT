from abc import ABC, abstractmethod
from Ops.Op import Op

class CmRDT(ABC):
  """
  Abstract base class for all CmRDT implementations
  """
  @abstractmethod
  def apply(self, op: Op):
    pass