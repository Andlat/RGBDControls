import time
import threading
from depthai_sdk import OakCamera, RecordType

from CameraHandler import CameraHandler


class OakHandler(CameraHandler):
    def __init__(self, oak: OakCamera):
        self.oak = oak
        self._thread_lock = threading.Lock()


    def _is_running(self):
        self._thread_lock.acquire(blocking=True)
        is_running = self.oak.running()
        self._thread_lock.release()

        return is_running

    def setup(self):
        color = self.oak.create_camera('color', resolution='1080p', fps=30, encode=True)
        left = self.oak.create_camera('left', resolution='800p', fps=30, encode=True)
        right = self.oak.create_camera('right', resolution='800p', fps=30, encode=True)
        stereo = self.oak.create_stereo(resolution='800p', fps=30, left=left, right=right, encode=True)

        # pipeline = oak.build()

        # Synchronize & save all (encoded) streams
        self.oak.record([color.out.encoded, left.out.encoded, right.out.encoded, stereo.out.encoded, stereo.out.depth], './',
                   RecordType.ROSBAG)

        # Show color stream
        # oak.visualize([color.out.encoded], scale=0.5, fps=True)

    def start(self):
        print(f"Starting recording for Oak-D {self.oak.device.getMxId()}")
        self.oak.start()

        while self._is_running():
            time.sleep(0.001)
            self.oak.poll()

    def stop(self):
        self._thread_lock.acquire(blocking=True)
        """
        P.S.:   The oak._stop variable is internal to the DepthAI SDK (which is in alpha).
                This might not work for other depthai-sdk versions (tested in versions 1.9.5 and 1.10.1)
        """
        self.oak._stop = True
        self._thread_lock.release()