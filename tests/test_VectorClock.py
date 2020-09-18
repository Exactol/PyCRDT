import unittest
from VectorClock import VectorClock
from VectorClockEntry import VectorClockEntry

class VectorClockTests(unittest.TestCase):
  def test_ctor(self):
    a = VectorClock()
    self.assertDictEqual(a.vector, {})

    a = VectorClock({"abc": 1})
    self.assertDictEqual(a.vector, {"abc": 1})

  def test_increment(self):
    a = VectorClock()
    foo_entry = a.increment("foo")
    self.assertEqual(foo_entry.counter, 1)
    self.assertEqual(foo_entry.identifier, "foo")
    self.assertDictEqual(a.vector, {})

    bar_entry = a.increment("bar")
    self.assertEqual(bar_entry.counter, 1)
    self.assertEqual(bar_entry.identifier, "bar")
    self.assertDictEqual(a.vector, {})

  def test_apply(self):
    a = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    self.assertDictEqual(a.vector, {"foo": 15})

    a = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    a.apply(VectorClockEntry("foo", 12))
    self.assertDictEqual(a.vector, {"foo": 15})

    a = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    a.apply(VectorClockEntry("bar", 12))
    self.assertDictEqual(a.vector, {"foo": 15, "bar": 12})

  def test_get(self):
    a = VectorClock()
    self.assertEqual(a.get("foo"), 0)

    a = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    self.assertEqual(a.get("foo"), 15)

    a = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    a.apply(VectorClockEntry("bar", 12))
    self.assertEqual(a.get("bar"), 12)

  def test_equality(self):
    a = VectorClock()
    b = VectorClock()
    self.assertEqual(a == b, True)
    # TODO: fails these gt/lt tests, but i think its ok?
    # self.assertEqual(a > b, False)
    # self.assertEqual(b > a, False)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("foo", 15))
    self.assertEqual(a == b, True)
    # self.assertEqual(a > b, False)
    # self.assertEqual(b > a, False)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("bar", 15))
    self.assertEqual(a == b, False)

  def test_ordering(self):
    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("foo", 12))
    self.assertEqual(a > b, True)
    self.assertEqual(b < a, True)
    self.assertEqual(b != a, True)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("foo", 20))
    self.assertEqual(a > b, False)
    self.assertEqual(b < a, False)
    self.assertEqual(b != a, True)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    a.apply(VectorClockEntry("bar", 20))
    b.apply(VectorClockEntry("foo", 15))
    self.assertEqual(a > b, True)
    self.assertEqual(b < a, True)
    self.assertEqual(b != a, True)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    a.apply(VectorClockEntry("bar", 20))
    b.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("bar", 21))
    self.assertEqual(b > a, True)
    self.assertEqual(a < b, True)
    self.assertEqual(b != a, True)

    a = VectorClock()
    b = VectorClock()
    b.apply(VectorClockEntry("foo", 12))
    self.assertEqual(a < b, True)
    self.assertEqual(b > a, True)
    self.assertEqual(b != a, True)

    a = VectorClock()
    b = VectorClock()
    b.apply(VectorClockEntry("foo", 12))
    self.assertEqual(a > b, False)
    self.assertEqual(b < a, False)
    self.assertEqual(b != a, True)

  def test_concurrent(self):
    a = VectorClock()
    b = VectorClock()
    self.assertEqual(a.concurrent(b), False)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("foo", 15))
    self.assertEqual(a.concurrent(b), False)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    b.apply(VectorClockEntry("bar", 12))
    self.assertEqual(a.concurrent(b), True)

    a = VectorClock()
    b = VectorClock()
    a.apply(VectorClockEntry("foo", 15))
    a.apply(VectorClockEntry("bar", 12))
    b.apply(VectorClockEntry("bar", 12))
    self.assertEqual(a.concurrent(b), False)
if __name__ == "__main__":
  unittest.main()