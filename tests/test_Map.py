import unittest
from CRDT.Map import Map
from CRDT.CRDTEntry import CRDTEntry
from Ops.SetOp import SetOp
from VectorClock import VectorClock
from VectorClockEntry import VectorClockEntry

class CRDTStoreTests(unittest.TestCase):
  def test_ctor(self):
    a = Map()
    self.assertEqual(a.clock, VectorClock())
    self.assertDictEqual(a.state, {})
    self.assertDictEqual(a.initial_state, {})

    a = Map(VectorClock({"foo": 15}))
    self.assertEqual(a.clock, VectorClock({"foo": 15}))
    self.assertDictEqual(a.state, {})
    self.assertDictEqual(a.initial_state, {})

    a = Map(initial_state={"foo": CRDTEntry("bar")})
    self.assertEqual(a.clock, VectorClock())
    self.assertDictEqual(a.state, {"foo": CRDTEntry("bar")})
    self.assertDictEqual(a.initial_state, {"foo": CRDTEntry("bar")})

    a = Map(VectorClock( {"foo": 15} ), initial_state={"foo": CRDTEntry("bar")})
    self.assertDictEqual(a.clock.vector, {"foo": 15})
    self.assertDictEqual(a.state, {"foo": CRDTEntry("bar")})
    self.assertDictEqual(a.initial_state, {"foo": CRDTEntry("bar")})

    # ensure mutating initial_version and initial_state doesn't affect default param values
    a = Map()
    a.state["foo"] = 15
    a.clock.vector["foo"] = VectorClockEntry("foo", 1)
    a = Map()
    self.assertEqual(a.clock, VectorClock())
    self.assertDictEqual(a.state, {})
    self.assertDictEqual(a.initial_state, {})

  def test_get(self):
    a = Map()
    self.assertEqual(a.get("foo"), None)

    a = Map()
    a.state["foo"] = CRDTEntry("bar")
    self.assertEqual(a.get("foo"), CRDTEntry("bar"))
    self.assertEqual(a.state["foo"], CRDTEntry("bar"))

  def test_apply(self):
    a = Map()
    op = SetOp("foo", "bar", a.clock.increment("baz"))
    a.apply(op)
    self.assertEqual(a.clock, VectorClock({"baz": 1}))
    self.assertDictEqual(a.state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 1 }))})
    self.assertDictEqual(a.initial_state, {})

    # test idempotency
    a = Map()
    op = SetOp("foo", "bar", a.clock.increment("baz"))
    a.apply(op)
    a.apply(op)
    self.assertEqual(a.clock, VectorClock({"baz": 1}))
    self.assertDictEqual(a.state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 1 }))})
    self.assertDictEqual(a.initial_state, {})

    # test idempotency
    a = Map()
    op = SetOp("foo", "bar", a.clock.increment("baz"))
    a.apply(op)
    op2 = SetOp("foo", "bar", a.clock.increment("baz"))
    a.apply(op2)
    self.assertEqual(a.clock, VectorClock({"baz": 2}))
    self.assertDictEqual(a.state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 2 }))})
    self.assertDictEqual(a.initial_state, {})

  # def test_convergance(self):
  #   op = SetOp("foo", "bar", a.clock.increment("baz"))
  #   op2 = SetOp("foo", "bar", a.clock.increment("baz"))

  #   a = Map()
  #   b = Map()
  #   a.apply(op)
  #   self.assertDictEqual(a.clock.vector, {"baz": 1})
  #   self.assertDictEqual(a.state, {"foo": CRDTEntry("bar", VectorClock({ "baz": 1 }))})
  #   self.assertDictEqual(a.initial_state, {})
