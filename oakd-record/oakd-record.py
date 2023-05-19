"""
Record using an Oak-D camera
Source: https://docs.luxonis.com/projects/sdk/en/latest/features/recording/#rosbag
2023-05-12
"""

from depthai_sdk import OakCamera, RecordType

def record():
    with OakCamera() as oak:
        color = oak.create_camera('color', resolution='1080p', fps=30, encode=True)
        left = oak.create_camera('left', resolution='800p', fps=30, encode=True)
        right = oak.create_camera('right', resolution='800p', fps=30, encode=True)
        stereo = oak.create_stereo(resolution='800p', fps=30, left=left, right=right, encode=True)

        # Synchronize & save all (encoded) streams
        oak.record([color.out.encoded, left.out.encoded, right.out.encoded, stereo.out.encoded, stereo.out.depth], './', RecordType.ROSBAG)

        # Show color stream
        oak.visualize([color.out.encoded], scale=0.5, fps=True)

        oak.start(blocking=True)


if __name__ == '__main__':
    record()
