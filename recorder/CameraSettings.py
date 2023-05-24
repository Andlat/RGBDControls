class CameraSetting(int):
    STEREO_480  = 0x01
    STEREO_720  = 0x02
    STEREO_1080 = 0x04
    COLOR_480   = 0x08
    COLOR_720   = 0x10
    COLOR_1080  = 0x20
    FPS_24      = 0x40
    FPS_30      = 0x80
    FPS_60      = 0x100



    @staticmethod
    def to_val(setting: int) -> int | tuple[int] | None:
        match setting: # Breaking compatibility with Python < 3.10
            case CameraSetting.STEREO_480 | CameraSetting.COLOR_480:
                return 720, 480
            case CameraSetting.STEREO_720 | CameraSetting.COLOR_720:
                return 1280, 720
            case CameraSetting.STEREO_1080 | CameraSetting.COLOR_1080:
                return 1920, 1080
            case CameraSetting.FPS_24:
                return 24
            case CameraSetting.FPS_30:
                return 30
            case CameraSetting.FPS_60:
                return 60

        # default
        return None


class SettingType(str):
    FPS     = "fps"
    STEREO  = "stereo"
    COLOR   = "color"


class CameraSettings:
    """
    self.settings contains bit flags of different possible camera settings
    Any code that uses this bears the responsability to validate conflicting flags
    """
    def __init__(self, *flags: CameraSetting):
        self.settings = 0

        for flag in flags:
            self.settings |= flag


    def has(self, setting: CameraSetting):
        return self.settings & setting == setting


    @staticmethod
    def _bits(n): # https://stackoverflow.com/a/8898977
        while n:
            b = n & (~n+1)
            yield b
            n ^= b


    def as_dict(self) -> dict[str, int]:
        """
        Create a dictionnary with the camera settings.
        If multiple flags/settings target a same "module" (stereo, color, fps, ...),
        then the highest ordered bit/flag of that "module" is used
        """
        d : dict[str, int | tuple[int]] = {}

        for setting in CameraSettings._bits(self.settings):
            key = None

            if ( setting == CameraSetting.STEREO_480 or
                 setting == CameraSetting.STEREO_720 or
                 setting == CameraSetting.STEREO_1080
            ):
                key = SettingType.STEREO
            elif ( setting == CameraSetting.COLOR_480 or
                   setting == CameraSetting.COLOR_720 or
                   setting == CameraSetting.COLOR_1080
            ):
                key = SettingType.COLOR
            elif ( setting == CameraSetting.FPS_24 or
                   setting == CameraSetting.FPS_30 or
                   setting == CameraSetting.FPS_60
            ):
                key = SettingType.FPS

            if key:
                d[key] = CameraSetting.to_val(setting)

        return d


class CameraSettingsMisconfigurationException(BaseException):
    def __init__(self, msg: str | None = None):
        super().__init__(msg or "Misconfigured camera settings")