from json import loads
import importlib

class Payload:
    def __init__(self, val):
        self.value = val
        self.type = type(val).__name__

    @staticmethod
    def from_dict(val: dict):
        p = Payload(None)
        p.__dict__ = val
        return p

    # TODO: kindof hacky
    def deserialize(self):
        inst = getattr(importlib.import_module(f"Ops.{self.type}"), self.type)(None, None, None)
        inst.__dict__ = self.value
        return inst