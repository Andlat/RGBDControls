from threading import Lock
from typing import TypeVar, Generic

T = TypeVar('T')

class SpinLockVar(Generic[T]):
    def __init__(self, initial_val: T):
        self._lock = Lock()
        self._value = initial_val


    def __eq__(self, other: T):
        return self._value == other


    def __bool__(self):
        return self._value


    def read(self) -> T:
        self._lock.acquire(blocking=True)

        v = self._value
        self._lock.release()

        return v


    def set(self, v: T) -> None:
        self._lock.acquire(blocking=True)

        self._value = v
        self._lock.release()
