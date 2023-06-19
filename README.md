# RGBDControls / CameraControls

## Unified base for recording with RGB-D cameras.
## Hi — Python 3.10 is needed

### Currently supported RGB-D
- OakD cameras (Supported with DepthAI)[https://github.com/luxonis/depthai]
- Intel RealSense RGB-D cameras (supported with PyRealSense2)[https://pypi.org/project/pyrealsense2/]

### Tested with
- OakD Pro Wide
- Intel RealSense D455

### HOW TO USE

1. Plug in your cameras
2. Install dependencies with `pip install -r requirements.txt'
3. Start the recording `python3.10 recorder/main.py [-dir|--directory]` <br/>:warning: do not forget a `/` at the end of the path when specifying a directory
4. Stop with `ctrl-C`

The recordings will be saved in the terminal's working directory unless specified otherwise with the arg `--directory`.

### Recording configurations
- The recording configurations can be changed in `recorder/main.py` via the `CameraHandler::setup` method called for each RGB-D camera type.
- See `CameraSettings` and `CameraSetting` classes in `CameraSettings.py` for more details

##### Possible configurations:
- STEREO_480
- STEREO_720
- STEREO_1080
- COLOR_480
- COLOR_720
- COLOR_1080
- FPS_24
- FPS_30
- FPS_60
- IMU


#### Feel free to change and reuse this code. Any contributions are welcome :p

#### P.S. Any changes related to the DepthAI library are to be carefully tested, since the SDK is still in alpha and changes very often. The current version of this repository supports version 1.10 of DepthAI SDK
