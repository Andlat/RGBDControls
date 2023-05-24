from threading import Thread
from typing import List, Callable

class ThreadHandler:
    def __init__(self):
        self._threads: List[Thread] = []

    def threads(self):
        return tuple(self._threads)

    def launch(self, fn: Callable, *args):
        task = Thread(target=fn, args=list(args))
        self._threads.append(task)
        task.start()

    def join_all(self):
        for thread in self._threads:
            thread.join()