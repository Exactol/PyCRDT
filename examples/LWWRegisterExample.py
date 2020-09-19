import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from CRDT.LWWRegister import LWWRegister
from Ops.SetOp import SetOp

# Create register
reg = LWWRegister()

# Create a new Set operation and apply it. For LWW structures, the field name is unused
op = SetOp(None, "Test", reg.clock().increment("User1"))
reg.apply(op)
print(reg)

# Create another Set operation and apply it.
op = SetOp(None, "Hello World", reg.clock().increment("User1"))
reg.apply(op)
print(reg)

# Create a Set operation from another user and apply it.
op = SetOp(None, "CRDTS are cool", reg.clock().increment("User2"))
reg.apply(op)
print(reg)

reg2 = reg.clone()
# Apply 2 operations that happened concurrently
op = SetOp(None, "Hello from User1", reg.clock().increment("User1"))
op2 = SetOp(None, "Hello from User2", reg.clock().increment("User2"))
reg.apply(op)
reg2.apply(op2)
print(reg)
print(reg2)
if reg.clock().concurrent(reg2.clock()):
  print("Clocks have diverged!")