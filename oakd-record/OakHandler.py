import time
from depthai_sdk import OakCamera, RecordType

class OakHandler:
    def __init__(self, oak: OakCamera):
        self.oak = oak

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
        self.oak.start()

        while self.oak.running():
            time.sleep(0.001)
            self.oak.poll()

    def stop(self):
        self.oak._stop = True