# RGBDControls / CameraControls

## Unified base for recording with RGB-D cameras.

### Currently supported RGB-D
- OakD cameras (Supported with DepthAI)[https://github.com/luxonis/depthai]
- Intel RealSense RGB-D cameras (supported with PyRealSense2)[https://pypi.org/project/pyrealsense2/]

### Tested with
- OakD Pro Wide
- Intel RealSense D455

### HOW TO USE

1. Plug in your cameras
2. Install dependencies with `pip install -r requirements.txt'
3. Start the recording `python3.10 recording/main.py [-dir|--directory]`
4. Stop with `ctrl-C`

The recordings will be saved in the terminal's working directory unless specified otherwise with the arg `--directory`.


#### Feel free to change and reuse this code. Any contributions are welcome :p 

#### P.S. Any changes related to the DepthAI library are to be carefully tested, since the SDK is still in alpha and changes very often. The current version of this repository supports version 1.10 of DepthAI SDK
