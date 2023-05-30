import time
import threading
import depthai as dai
from depthai_sdk import OakCamera, RecordType

from CameraHandler import CameraHandler
from CameraSettings import CameraSetting, CameraSettings, CameraSettingsMisconfigurationException, SettingType


class OakHandler(CameraHandler):
    def __init__(self, oak: OakCamera, rec_dir: str = './'):
        self.oak = oak
        self._thread_lock = threading.Lock()
        self.rec_dir = rec_dir


    def _is_running(self):
        self._thread_lock.acquire(blocking=True)
        is_running = self.oak.running()
        self._thread_lock.release()

        return is_running


    @staticmethod
    def _extract_camera_settings(settings: CameraSettings) -> tuple[str | int]: # Might throw an exception
        set = settings.as_dict()
        fps = set[SettingType.FPS]

        stereo = set[SettingType.STEREO]
        stereo = '800p' if stereo[1] == 720 else f"{stereo[1]}p"

        color = set[SettingType.COLOR]
        color = '800p' if color[1] == 720 else f"{color[1]}p"

        return stereo, color, fps


    def setup(self, settings: CameraSettings = CameraSettings(CameraSetting.STEREO_720, CameraSetting.COLOR_1080, CameraSetting.FPS_30)):

        try:
            # Get the camera settings
            stereo, color, fps = OakHandler._extract_camera_settings(settings)

            # Apply the settings to the streams
            color = self.oak.create_camera('color', resolution=color, fps=fps, encode=True)
            left = self.oak.create_camera('left', resolution=stereo, fps=fps, encode=True)
            right = self.oak.create_camera('right', resolution=stereo, fps=fps, encode=True)
            stereo = self.oak.create_stereo(resolution=stereo, fps=fps, left=left, right=right, encode=True)
        except:
            raise CameraSettingsMisconfigurationException("Bad camera settings configuration for Intel RealSense cameras")


        # Synchronize & save all (encoded) streams
        self.oak.record([color.out.encoded, left.out.encoded, right.out.encoded, stereo.out.encoded, stereo.out.depth],
                        self.rec_dir,
                        RecordType.ROSBAG
                       )

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