import unittest

from SpinLockVar import SpinLockVar
from CameraSettings import CameraSettings, CameraSetting, CameraSettingsMisconfigurationException, SettingType
from OakHandler import OakHandler
from RealSenseHandler import RealSenseHandler

class DummyClass():
    def __init__(self):
        ...

class TestSpinLockVar(unittest.TestCase):

    def test_eq(self):
        lock1 = SpinLockVar[bool](False)
        lock2 = SpinLockVar[bool](True)

        self.assertNotEqual(lock1.read(), lock2.read())
        self.assertFalse(lock1 == lock2)

        lock2.set(False)

        self.assertEqual(lock1.read(), lock2.read())
        self.assertTrue(lock1 == lock2)


    def test_generic_type(self):
        lock = SpinLockVar[DummyClass](DummyClass())

        self.assertTrue(isinstance(lock.read(), DummyClass))


    def test_no_init_val(self):
        caught_ex = False

        try:
            lock = SpinLockVar[DummyClass]()
        except:
            caught_ex = True

        self.assertTrue(caught_ex)



    def test_intrinsic_eq(self):
        lock = SpinLockVar[bool](False)

        if lock:
            self.fail()

        lock.set(True)
        if not lock:
            self.fail()


class TestCameraSettings(unittest.TestCase):

    def test_creating_settings(self):
        try:
            settings = CameraSettings(CameraSetting.STEREO_720, CameraSetting.COLOR_1080, CameraSetting.FPS_30)
        except:
            self.fail()


    def test_matching_settings(self):
        settings = CameraSettings(CameraSetting.STEREO_1080, CameraSetting.COLOR_1080, CameraSetting.FPS_60)

        self.assertTrue(settings.has(CameraSetting.COLOR_1080))
        self.assertTrue(settings.has(CameraSetting.STEREO_1080))
        self.assertTrue(settings.has(CameraSetting.FPS_60))

        self.assertFalse(settings.has(CameraSetting.FPS_24))
        self.assertFalse(settings.has(CameraSetting.STEREO_480))
        self.assertFalse(settings.has(CameraSetting.COLOR_480))
        self.assertFalse(settings.has(CameraSetting.COLOR_720))


    def test_vals(self):
        self.assertEqual(CameraSetting.to_val(CameraSetting.COLOR_1080), (1920, 1080))
        self.assertEqual(CameraSetting.to_val(CameraSetting.STEREO_480), (720, 480))
        self.assertEqual(CameraSetting.to_val(CameraSetting.FPS_60), 60)


    def test_dict_representation(self):
        settings = CameraSettings(CameraSetting.STEREO_480, CameraSetting.COLOR_720, CameraSetting.FPS_24)

        d = settings.as_dict()

        self.assertEqual(d[SettingType.FPS], 24)
        self.assertEqual(d[SettingType.COLOR], (1280, 720))
        self.assertEqual(d[SettingType.STEREO], (720, 480))


    def test_exception(self):
        try:
            raise CameraSettingsMisconfigurationException()
        except CameraSettingsMisconfigurationException as e:
            self.assertEqual(str(e), "Misconfigured camera settings")

        try:
            raise CameraSettingsMisconfigurationException("My custom message")
        except CameraSettingsMisconfigurationException as e:
            self.assertEqual(str(e), "My custom message")


class TestOakHandler(unittest.TestCase):

    def test_settings_extraction(self):
        stereo, color, fps = OakHandler._extract_camera_settings(CameraSettings(CameraSetting.STEREO_720, CameraSetting.COLOR_1080, CameraSetting.FPS_30))

        self.assertEqual(stereo, '800p')
        self.assertEqual(color, '1080p')
        self.assertEqual(fps, 30)


class TestRealSenseHandler(unittest.TestCase):

    def test_settings_extraction(self):
        stereo, color, fps = RealSenseHandler._extract_camera_settings(CameraSettings(CameraSetting.STEREO_720, CameraSetting.COLOR_1080, CameraSetting.FPS_60))

        self.assertEqual(stereo, (1280, 720))
        self.assertEqual(color, (1920, 1080))
        self.assertEqual(fps, 60)


if __name__ == '__main__':
    unittest.main()