from unittest import TestCase
from CRDT.LWWRegister import LWWRegister
from CRDT.CRDTEntry import CRDTEntry
from Ops.SetOp import SetOp
from VectorClock import VectorClock
from VectorClockEntry import VectorClockEntry

class LWWRegisterTests(TestCase):
  def test_ctor(self):
    a = LWWRegister()
    self.assertEqual(a.state.value, None)
    self.assertEqual(a.state.clock, VectorClock())

    a = LWWRegister(CRDTEntry("foo"))
    self.assertEqual(a.state.value, "foo")
    self.assertEqual(a.state.clock, VectorClock())

    a = LWWRegister(CRDTEntry("foo", VectorClock({"bar": 1})))
    self.assertEqual(a.state.value, "foo")
    self.assertEqual(a.state.clock, VectorClock({"bar": 1}))

    # ensure mutating initial_state doesn't affect default param values
    a = LWWRegister()
    a.state.value = 15
    a.state.clock = VectorClock({"foo": 1})
    a = LWWRegister()
    self.assertEqual(a.state.value, None)
    self.assertEqual(a.state.clock, VectorClock())

  def test_get(self):
    a = LWWRegister()
    self.assertEqual(a.get(), None)

    a = LWWRegister()
    a.state.value = "foo"
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.state.value, "foo")

    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.state.value, "foo")

  def test_set(self):
    # test update on default register
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    self.assertEqual(a.state.value, "foo")
    self.assertEqual(a.state.clock, VectorClock({"bar": 1}))

    # test normal update
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    a.apply(SetOp(None, "baz", VectorClockEntry("bar", 2)))
    self.assertEqual(a.state.value, "baz")
    self.assertEqual(a.state.clock, VectorClock({"bar": 2}))

    # test stale update - new op has older version
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 5)))
    a.apply(SetOp(None, "baz", VectorClockEntry("bar", 2)))
    self.assertEqual(a.state.value, "foo")
    self.assertEqual(a.state.clock, VectorClock({"bar": 5}))

    # test duplicate update - new op has same value and clock
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 2)))
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 2)))
    self.assertEqual(a.state.value, "foo")
    self.assertEqual(a.state.clock, VectorClock({"bar": 2}))

    # test bad update - new op has different value and same clock
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 2)))
    self.assertRaises(Exception("Conflicting Clocks"), a.apply(SetOp(None, "baz", VectorClockEntry("bar", 2))))
    self.assertEqual(a.state.value, "foo")
    self.assertEqual(a.state.clock, VectorClock({"bar": 2}))