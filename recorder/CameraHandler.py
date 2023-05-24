from abc import ABC, abstractmethod


class CameraHandler:
    @abstractmethod
    def setup(self):
        ...

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def stop(self):
        ...