from typing import List

import pyrealsense2 as rs
import cv2
import os
import logging

from CameraHandler import CameraHandler


class RealSenseHandler(CameraHandler):
    def __init__(self, device: rs.device | None):
        """
        Instantiate a handler for RealSense depth cameras
        :param device:  the device to use within this handler. If none is given, the first device
                        available is used (no check is done to make sure the device is not used by another handler)
        """
        self.device = device if device else RealSenseHandler.get_devices()[0]
        self.device_id = RealSenseHandler.get_device_id(self.device)

        self.rec_dir = RealSenseHandler._create_recording_dir(self.device)

        self.pipe = rs.pipeline()
        self.config = rs.config()

        self._is_running = False

    def setup(self):
        self.config.enable_device(self.device_id)
        self.config.enable_record_to_file(f"{self.rec_dir}/recording.bag")
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.rgb8, 30)
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

    def start(self):
        print(f"Starting recording for Intel RealSense {self.device_id}")
        self.pipe.start(self.config)

        self._is_running = True
        while self._is_running:
            try:
                frames = self.pipe.wait_for_frames()
            except RuntimeError as e:
                logging.warning(f"RealSense {self.device_id} : {e}")
                continue

        self.pipe.stop()

    def stop(self): ######## TODO thread-safety
        self._is_running = False

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
    def _create_recording_dir(device: rs.device) -> str | None:
        device_id = RealSenseHandler.get_device_id(device)

        i = 1
        while True:
            directory = f"{i}-{device_id}"
            i += 1

            if not os.path.exists(directory):
                os.makedirs(directory)
                break

        return directory

def cv_show_from_frames(): # https://github.com/IntelRealSense/librealsense/blob/master/doc/record-and-playback.md
    ...