import unittest

from SpinLockVar import SpinLockVar

class DummyClass():
    def __init__(self):
        ...

class TestSpinLockVar(unittest.TestCase):

    def test_eq(self):
        lock1 = SpinLockVar[bool](False)
        lock2 = SpinLockVar[bool](True)

        self.assertNotEqual(lock1.read(), lock2.read())
        self.assertFalse(lock1 == lock2)

        lock2.set(False)

        self.assertEqual(lock1.read(), lock2.read())
        self.assertTrue(lock1 == lock2)


    def test_generic_type(self):
        lock = SpinLockVar[DummyClass](DummyClass())

        self.assertTrue(isinstance(lock.read(), DummyClass))


    def test_no_init_val(self):
        caught_ex = False

        try:
            lock = SpinLockVar[DummyClass]()
        except:
            caught_ex = True

        self.assertTrue(caught_ex)



    def test_intrinsic_eq(self):
        lock = SpinLockVar[bool](False)

        if lock:
            self.fail()

        lock.set(True)
        if not lock:
            self.fail()


if __name__ == '__main__':
    unittest.main()