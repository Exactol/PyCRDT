from typing import Callable, List


'''
Simple class to handle multiple callback listeners
'''
class Callback():
  def __init__(self):
    self.listeners: List[Callable] = []

  def __iadd__(self, value):
    self.listeners.append(value)
    return self

  def __isub__(self, value):
    self.listeners.remove(value)
    return self

  def __call__(self, *args, **kwargs):
    for listener in self.listeners:
      listener(*args, **kwargs)
