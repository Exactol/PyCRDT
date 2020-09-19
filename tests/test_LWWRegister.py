from unittest import TestCase
from CRDT.LWWRegister import LWWRegister
from CRDT.CRDTEntry import CRDTEntry
from Ops.SetOp import SetOp
from Ops.DummyOp import DummyOp
from VectorClock import VectorClock
from VectorClockEntry import VectorClockEntry

class LWWRegisterTests(TestCase):
  def test_ctor(self):
    a = LWWRegister()
    self.assertEqual(a.get(), None)
    self.assertEqual(a.clock(), VectorClock())

    a = LWWRegister("foo")
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.clock(), VectorClock())

    a = LWWRegister("foo", VectorClock({"bar": 1}))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.clock(), VectorClock({"bar": 1}))

    # ensure mutating initial_state doesn't affect default param values
    a = LWWRegister()
    a._state = 15
    a._clock = VectorClock({"foo": 1})
    a = LWWRegister()
    self.assertEqual(a.get(), None)
    self.assertEqual(a.clock(), VectorClock())

  def test_get(self):
    a = LWWRegister()
    self.assertEqual(a.get(), None)

    a = LWWRegister()
    a._state = "foo"
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a._state, "foo")

    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a._state, "foo")

  def test_set(self):
    # test update on default register
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.clock(), VectorClock({"bar": 1}))

    # test normal update
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    a.apply(SetOp(None, "baz", VectorClockEntry("bar", 2)))
    self.assertEqual(a.get(), "baz")
    self.assertEqual(a.clock(), VectorClock({"bar": 2}))

    # test stale update - new op has older version
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 5)))
    a.apply(SetOp(None, "baz", VectorClockEntry("bar", 2)))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.clock(), VectorClock({"bar": 5}))
    a.apply(SetOp(None, "bar", VectorClockEntry("bar", 10)))
    self.assertEqual(a.get(), "bar")
    self.assertEqual(a.clock(), VectorClock({"bar": 10}))

    # test duplicate update - new op has same value and clock
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 2)))
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 2)))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.clock(), VectorClock({"bar": 2}))

    # test bad update - new op has different value and same clock
    a = LWWRegister()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 2)))
    with self.assertRaises(Exception):
      a.apply(SetOp(None, "baz", VectorClockEntry("bar", 2)))
    self.assertEqual(a.get(), "foo")
    self.assertEqual(a.clock(), VectorClock({"bar": 2}))

    # test applying unsupported operations
    a = LWWRegister()
    op = DummyOp()
    with self.assertRaises(Exception):
      a.apply(op)
    self.assertEqual(a.clock(), VectorClock())
    self.assertEqual(a.get(), None)

  def test_clone(self):
    a = LWWRegister()
    b = a.clone()
    self.assertEqual(a.get(), b.get())
    self.assertEqual(a.clock(), b.clock())

    # test mutating A doesnt mutate B
    a = LWWRegister()
    b = a.clone()
    a.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    self.assertNotEqual(a.get(), b.get())
    self.assertNotEqual(a.clock(), b.clock())

    # test mutating B doesnt mutate A
    a = LWWRegister()
    b = a.clone()
    b.apply(SetOp(None, "foo", VectorClockEntry("bar", 1)))
    self.assertNotEqual(a.get(), b.get())
    self.assertNotEqual(a.clock(), b.clock())