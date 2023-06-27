from threading import Lock
from typing import TypeVar, Generic

T = TypeVar('T')

class SpinLockVar(Generic[T]):
    class ScopedLock:
        def __init__(self, lock: Lock):
            self._lock = lock

        def __enter__(self):
            self._lock.acquire(blocking=True)

        def __exit__(self, exc_type, exc_value, traceback):
            self._lock.release()


    def __init__(self, initial_val: T):
        self._lock = Lock()
        self._value = initial_val


    def __eq__(self, other: T):
        return self._value == other


    def __bool__(self):
        return self._value


    def __add__(self, other: T):
        """
        Addition the lock's variable with the other value
        Returns the resulting value (not a lock!)
        """
        with SpinLockVar.ScopedLock(self._lock):
            return self._value + other


    def __iadd__(self, other: T):
        """
        Adds to the lock's variable
        Returns the lock itself
        """
        with SpinLockVar.ScopedLock(self._lock):
            self._value += other
            return self


    def __sub__(self, other: T):
        with SpinLockVar.ScopedLock(self._lock):
            return self._value - other


    def __isub__(self, other: T):
        with SpinLockVar.ScopedLock(self._lock):
            self._value -= other
            return self


    def read(self) -> T:
        with SpinLockVar.ScopedLock(self._lock):
            return self._value


    def set(self, v: T) -> None:
        with SpinLockVar.ScopedLock(self._lock):
            self._value = v