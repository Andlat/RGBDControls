from typing import List, Union

import pyrealsense2 as rs
import cv2
import os
import logging

from CameraHandler import CameraHandler
from CameraSettings import CameraSetting, CameraSettings, CameraSettingsMisconfigurationException, SettingType
from SpinLockVar import SpinLockVar


class RealSenseHandler(CameraHandler):
    def __init__(self, device: Union[rs.device, None], rec_dir: str = './'):
        """
        Instantiate a handler for RealSense depth cameras
        :param device:  the device to use within this handler. If none is given, the first device
                        available is used (no check is done to make sure the device is not used by another handler)
        """
        self.device = device if device else RealSenseHandler.get_devices()[0]
        self.device_id = RealSenseHandler.get_device_id(self.device)

        self.rec_dir = RealSenseHandler._create_recording_dir(self.device, rec_dir)

        self.pipe = rs.pipeline()
        self.config = rs.config()

        self._is_running = SpinLockVar[bool](False)


    @staticmethod
    def _extract_camera_settings(settings: CameraSettings) -> tuple[str | int]: # Might throw an exception
        set = settings.as_dict()
        stereo = set[SettingType.STEREO]
        color = set[SettingType.COLOR]
        fps = set[SettingType.FPS]

        return stereo, color, fps


    def setup(self, settings: CameraSettings = CameraSettings(CameraSetting.STEREO_720, CameraSetting.COLOR_720, CameraSetting.FPS_30)):
        self.config.enable_device(self.device_id)
        self.config.enable_record_to_file(f"{self.rec_dir}/recording.bag")

        try:
            # Get the camera settings
            stereo, color, fps = RealSenseHandler._extract_camera_settings(settings)

            # Apply the settings to the streams
            self.config.enable_stream(rs.stream.color, color[0], color[1], rs.format.rgb8, fps)
            self.config.enable_stream(rs.stream.depth, stereo[0], stereo[1], rs.format.z16, fps)
        except:
            raise CameraSettingsMisconfigurationException("Bad camera settings configuration for Intel RealSense cameras")


    def start(self):
        print(f"Starting recording for Intel RealSense {self.device_id}")
        self.pipe.start(self.config)

        self._is_running.set(True)
        while self._is_running:
            try:
                frames = self.pipe.wait_for_frames()
            except RuntimeError as e:
                logging.warning(f"RealSense {self.device_id} : {e}")
                continue

        self.pipe.stop()

    def stop(self):
        self._is_running.set(False)

    @staticmethod
    def global_setup() -> None:
        """
        Call before instanciating any RealSenseHandler
        """
        rs.align(rs.stream.color)

    @staticmethod
    def get_devices() -> List[rs.device]:
        return list(rs.context().query_devices())

    @staticmethod
    def get_device_id(device: rs.device) -> str:
        return device.get_info(rs.camera_info.serial_number)


    @staticmethod
    def _create_recording_dir(device: rs.device, root: str = "./") -> Union[str, None]:
        device_id = RealSenseHandler.get_device_id(device)

        i = 1
        while True:
            directory = f"{root}{i}-{device_id}"
            i += 1

            if not os.path.exists(directory):
                os.makedirs(directory)
                break

        return directory

def cv_show_from_frames(): # https://github.com/IntelRealSense/librealsense/blob/master/doc/record-and-playback.md
    ...