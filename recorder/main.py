#!/usr/bin/env python

"""
Record using multiple Oak-D and Intel RealSense cameras

Inspired from:
    - https://docs.luxonis.com/projects/sdk/en/latest/features/recording/#rosbag
    - https://docs.luxonis.com/projects/api/en/latest/samples/mixed/multiple_devices/
    - https://github.com/IntelRealSense/librealsense/blob/master/doc/record-and-playback.md

Nikola Zelovic
2023-05-12--->2023-05-..
"""

import signal
import time
from typing import List
from termcolor import colored
from depthai_sdk import OakCamera
import depthai

from CameraHandler import CameraHandler
from OakHandler import OakHandler
from RealSenseHandler import RealSenseHandler
from ThreadHandler import ThreadHandler

ENABLE_REALSENSE_DEVICES = True
ENABLE_OAKD_DEVICES = True

##########################
# Global vars #
##########################

should_exit = False
cam_handlers: List[CameraHandler] = []
threads_handler = ThreadHandler()

##########################
##########################


def record_oak(cam_id: str):
    with OakCamera(cam_id) as oak:
        handler = OakHandler(oak)
        cam_handlers.append(handler)

        handler.setup()
        handler.start()


def record_rs(device):
    handler = RealSenseHandler(device)
    cam_handlers.append(handler)

    handler.setup()
    handler.start()


def on_exit(signal, frame):
    print(colored("Stopping cameras", 'yellow'))
    for handler in cam_handlers:
        handler.stop()

    print("Joining threads")
    threads_handler.join_all()

    global should_exit
    should_exit = True


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_exit)

    if ENABLE_OAKD_DEVICES:
        oakd_devices = depthai.Device.getAllAvailableDevices()
        if len(oakd_devices) > 0:
            for device in oakd_devices:
                threads_handler.launch(record_oak, device.getMxId()) # TODO Make sure device.state says XLinkDeviceState.X_LINK_UNBOOTED
        else:
            print("No Oak-D devices connected")

    if ENABLE_REALSENSE_DEVICES:
        intel_devices = RealSenseHandler.get_devices()
        if len(intel_devices) > 0:
            for device in intel_devices:
                threads_handler.launch(record_rs, device)
        else:
            print("No Intel RealSense devices conected")

    while not should_exit:
        time.sleep(1)

    print(colored("Quitting...", 'green'))
