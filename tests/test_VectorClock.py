import unittest
from VectorClock import VectorClock

class VectorClockTests(unittest.TestCase):
  def test_new(self):
    a = VectorClock(0)
    self.assertEqual(a.user_id, 0)
    self.assertDictEqual(a.vector, {0: 0})

    a = VectorClock(1)
    self.assertEqual(a.user_id, 1)
    self.assertDictEqual(a.vector, {1: 0})

    a = VectorClock(0, {0: 1})
    self.assertEqual(a.user_id, 0)
    self.assertDictEqual(a.vector, {0: 1})

    a = VectorClock(0, {0: 1, 1: 15})
    self.assertEqual(a.user_id, 0)
    self.assertDictEqual(a.vector, {0: 1, 1: 15})

  def test_merge(self):
    a = VectorClock(0)
    b = VectorClock(1)
    a.merge(b)

    self.assertEqual(a.user_id, 0)
    self.assertDictEqual(a.vector, {0: 0, 1: 0})

    a = VectorClock(0, {0: 1})
    b = VectorClock(1)
    b.merge(a)

    self.assertEqual(b.user_id, 1)
    self.assertDictEqual(b.vector, {0: 1, 1: 0})

  def test_increment(self):
    a = VectorClock(0)
    b = a.increment()

    self.assertEqual(b.user_id, 0)
    self.assertDictEqual(b.vector, {0: 1})

  def test_increment_other_user(self):
    a = VectorClock(0)
    b = a.increment()
    self.assertEqual(b.user_id, 0)
    self.assertDictEqual(b.vector, {0: 1})

if __name__ == "__main__":
  unittest.main()