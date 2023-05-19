from pathlib import Path


from rosbags.highlevel import AnyReader

if __name__ == '__main__':
    with AnyReader([Path('C:/Users/CdRV-SigMo/Documents/cameraAI/oakd-record/23-18443010912E9A0F00/recording.bag')]) as reader:
        connections = [x for x in reader.connections if x.topic == '/left/raw']
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            msg = reader.deserialize(rawdata, connection.msgtype)
            print(msg.header.frame_id)