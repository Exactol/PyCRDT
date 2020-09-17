import unittest
from VectorClockEntry import VectorClockEntry

class VectorClockEntryTests(unittest.TestCase):
  def test_new(self):
    a = VectorClockEntry("abc")
    self.assertEqual(a.identifier, "abc")
    self.assertEqual(a.counter, 0)

    a = VectorClockEntry(0, 10)
    self.assertEqual(a.identifier, 0)
    self.assertEqual(a.counter, 10)

  def test_incremment(self):
    a = VectorClockEntry("abc")
    a = a.increment()
    self.assertEqual(a.identifier, "abc")
    self.assertEqual(a.counter, 1)

    a = VectorClockEntry(0, 10)
    a = a.increment()
    self.assertEqual(a.identifier, 0)
    self.assertEqual(a.counter, 11)

  def test_equality(self):
    a = VectorClockEntry("abc")
    b = VectorClockEntry("abc")
    result = a == b
    self.assertEqual(result, True)

    a = VectorClockEntry("abc")
    b = VectorClockEntry("def")
    result = a == b
    self.assertEqual(result, False)

    a = VectorClockEntry("abc")
    b = VectorClockEntry("abc", 1)
    result = a == b
    self.assertEqual(result, False)

    a = VectorClockEntry("abc")
    b = VectorClockEntry("abc", 1)
    result = a != b
    self.assertEqual(result, True)

  def test_partial_order(self):
    # less than
    a = VectorClockEntry("abc")
    b = VectorClockEntry("abc", 1)
    result = a < b
    self.assertEqual(result, True)

    a = VectorClockEntry("abc", 1)
    b = VectorClockEntry("abc")
    result = a < b
    self.assertEqual(result, False)

    a = VectorClockEntry("abc")
    b = VectorClockEntry("def", 1)
    result = a < b
    self.assertEqual(result, None)

    # greater than
    a = VectorClockEntry("abc")
    b = VectorClockEntry("abc", 1)
    result = a > b
    self.assertEqual(result, False)

    a = VectorClockEntry("abc", 1)
    b = VectorClockEntry("abc")
    result = a > b
    self.assertEqual(result, True)

    a = VectorClockEntry("abc")
    b = VectorClockEntry("def", 1)
    result = a > b
    self.assertEqual(result, None)