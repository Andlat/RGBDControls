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

import argparse
import os
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
from CameraSettings import CameraSetting, CameraSettings

##########################
#     Global settings    #
##########################

ENABLE_REALSENSE_DEVICES = True
ENABLE_OAKD_DEVICES = True

RECORDING_DIR = "./"

##########################
##########################

##########################
#       Global vars      #
##########################

should_exit = False
cam_handlers: List[CameraHandler] = []
threads_handler = ThreadHandler()

##########################
##########################


def setup_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
                prog='RGB-D multi recorder',
                description='Record RGB-D data from multiple RGB-D cameras using only one machine',
            )

    parser.add_argument('-dir', '--directory', type=str, help='Directory where the recordings will be saved', required=False)

    return parser


def record_oak(cam_id: str):
    with OakCamera(cam_id) as oak:
        handler = OakHandler(oak, rec_dir=RECORDING_DIR)
        cam_handlers.append(handler)

        handler.setup()
        handler.start()


def record_rs(device):
    handler = RealSenseHandler(device, rec_dir=RECORDING_DIR)
    cam_handlers.append(handler)

    handler.setup(settings = CameraSettings(CameraSetting.STEREO_720, CameraSetting.COLOR_720, CameraSetting.FPS_30, CameraSetting.IMU))
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
    args: dict[str, str] = setup_arg_parser().parse_args()

    # Parse and format the dir for the recordings
    if args.directory:
        RECORDING_DIR = args.directory
    RECORDING_DIR = os.path.expanduser(RECORDING_DIR)

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
