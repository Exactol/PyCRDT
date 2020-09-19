import unittest
from CRDT.LWWRegister import LWWRegister
from CRDT.Map import Map
from CRDT.CRDTEntry import CRDTEntry
from Ops.SetOp import SetOp
from Ops.DummyOp import DummyOp
from Causality.VectorClock import VectorClock
from Causality.VectorClockEntry import VectorClockEntry

class CRDTStoreTests(unittest.TestCase):
  def test_ctor(self):
    a = Map()
    self.assertEqual(a.clock(), VectorClock())
    self.assertDictEqual(a._state, {})
    self.assertDictEqual(a._initial_state, {})

    a = Map(initial_clock=VectorClock({"foo": 15}))
    self.assertEqual(a.clock(), VectorClock({"foo": 15}))
    self.assertDictEqual(a._state, {})
    self.assertDictEqual(a._initial_state, {})

    a = Map({"foo": CRDTEntry("bar")})
    self.assertEqual(a.clock(), VectorClock())
    self.assertDictEqual(a._state, {"foo": CRDTEntry("bar")})
    self.assertDictEqual(a._initial_state, {"foo": CRDTEntry("bar")})

    a = Map({"foo": CRDTEntry("bar")}, VectorClock( {"foo": 15} ))
    self.assertEqual(a.clock(), VectorClock({"foo": 15}))
    self.assertDictEqual(a._state, {"foo": CRDTEntry("bar")})
    self.assertDictEqual(a._initial_state, {"foo": CRDTEntry("bar")})

    # ensure mutating initial_version and initial_state doesn't affect default param values
    a = Map()
    a._state["foo"] = 15
    a._clock.vector["foo"] = VectorClockEntry("foo", 1)
    a = Map()
    self.assertEqual(a.clock(), VectorClock())
    self.assertDictEqual(a._state, {})
    self.assertDictEqual(a._initial_state, {})

  def test_get(self):
    a = Map()
    self.assertEqual(a.get("foo"), None)

    a = Map()
    a._state["foo"] = CRDTEntry("bar")
    self.assertEqual(a.get("foo"), CRDTEntry("bar"))
    self.assertEqual(a._state["foo"], CRDTEntry("bar"))

  def test_apply(self):
    a = Map()
    op = SetOp("foo", "bar", a.clock().increment("baz"))
    a.apply(op)
    self.assertEqual(a.clock(), VectorClock({"baz": 1}))
    self.assertDictEqual(a._state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 1 }))})
    self.assertDictEqual(a._initial_state, {})

    # test idempotency
    a = Map()
    op = SetOp("foo", "bar", a.clock().increment("baz"))
    a.apply(op)
    a.apply(op)
    self.assertEqual(a.clock(), VectorClock({"baz": 1}))
    self.assertDictEqual(a._state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 1 }))})
    self.assertDictEqual(a._initial_state, {})

    # test idempotency
    a = Map()
    op = SetOp("foo", "bar", a.clock().increment("baz"))
    a.apply(op)
    op2 = SetOp("foo", "bar", a.clock().increment("baz"))
    a.apply(op2)
    self.assertEqual(a.clock(), VectorClock({"baz": 2}))
    self.assertDictEqual(a._state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 2 }))})
    self.assertDictEqual(a._initial_state, {})

    # test nested CRDTs
    a = Map()
    op = SetOp("reg", LWWRegister(), a.clock().increment("User1"))
    a.apply(op)
    self.assertEqual(a.clock(), VectorClock({"User1": 1}))
    self.assertEqual(a.get("reg").value, LWWRegister())
    self.assertEqual(a.get("reg").value.clock(), VectorClock())
    self.assertDictEqual(a._initial_state, {})

    # test applying operations to nested CRDTs
    a = Map()
    op = SetOp("reg", LWWRegister(), a.clock().increment("User1"))
    a.apply(op)
    op = SetOp("reg", SetOp(None, "Hello World", a.get("reg").value.clock().increment("User2")), a.clock().increment("User1"))
    a.apply(op)
    self.assertEqual(a.clock(), VectorClock({"User1": 2}))
    self.assertEqual(a.get("reg").value.get(), "Hello World")
    self.assertEqual(a.get("reg").value.clock(), VectorClock({"User2": 1}))
    self.assertDictEqual(a._initial_state, {})

    # test applying unsupported operations
    a = Map()
    op = DummyOp()
    with self.assertRaises(Exception):
      a.apply(op)
    self.assertEqual(a.clock(), VectorClock())
    self.assertDictEqual(a._state, {})
    self.assertDictEqual(a._initial_state, {})


  # def test_convergance(self):
  #   op = SetOp("foo", "bar", a.clock.increment("baz"))
  #   op2 = SetOp("foo", "bar", a.clock.increment("baz"))

  #   a = Map()
  #   b = Map()
  #   a.apply(op)
  #   self.assertDictEqual(a.clock.vector, {"baz": 1})
  #   self.assertDictEqual(a.state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 1 }))})
  #   self.assertDictEqual(a.initial_state, {})
