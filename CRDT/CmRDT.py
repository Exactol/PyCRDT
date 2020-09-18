from abc import ABC, abstractmethod
from Ops.Op import Op

class CmRDT(ABC):
  @abstractmethod
  def apply(self, op: Op):
    pass