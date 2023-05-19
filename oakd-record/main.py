"""
Record using an Oak-D camera
Inspired from:
    - https://docs.luxonis.com/projects/sdk/en/latest/features/recording/#rosbag
    - https://docs.luxonis.com/projects/api/en/latest/samples/mixed/multiple_devices/

Nikola Zelovic
2023-05-12--->2023-05-..
"""

import signal
import time
from typing import List
from termcolor import colored
from depthai_sdk import OakCamera
from OakHandler import OakHandler
from ThreadHandler import ThreadHandler

ENABLE_OAKD_PRO_W_1 = True
ENABLE_OAKD_PRO_W_2 = True

OAKD_PRO_W_1 = "18443010418D850E00"
OAKD_PRO_W_2 = "18443010912E9A0F00"


##########################
# DO NOT TOUCH VARIABLES #
##########################

should_exit = False
oak_handlers: List[OakHandler] = []
threads_handler = ThreadHandler()

##########################
##########################


def record_oak(cam_id: str):
    with OakCamera(cam_id) as oak:
        handler = OakHandler(oak)
        oak_handlers.append(handler)

        handler.setup()
        handler.start()


def on_exit(signal, frame):
    print(colored("Stopping oak cameras", 'yellow'))
    for handler in oak_handlers:
        handler.stop()

    print("Joining threads")
    threads_handler.join_all()

    global should_exit
    should_exit = True


if __name__ == '__main__':
    signal.signal(signal.SIGINT, on_exit)

    if ENABLE_OAKD_PRO_W_1:
        threads_handler.launch(record_oak, OAKD_PRO_W_1)

    if ENABLE_OAKD_PRO_W_2:
        threads_handler.launch(record_oak, OAKD_PRO_W_2)

    while not should_exit:
        time.sleep(1)

    print(colored("Quitting...", 'green'))