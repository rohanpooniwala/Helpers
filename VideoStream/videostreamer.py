import cv2
import numpy as np
import socket
import struct
from threading import Thread


def sendframe(clientsocket, frame):
    try:
        frame = cv2.imencode(".jpg", frame)[1]
        data = frame.tostring()
        clientsocket.sendall(struct.pack("H", len(data)) + data)
        return True
    except:
        return False


class InternetVideoStream:
    def __init__(self, sock):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.sock = sock
        self.frame = np.zeros((240, 320), dtype=np.uint8)
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        payload_size = struct.calcsize("H")
        data = b''
        # keep looping infinitely until the thread is stopped
        while True:
            try:
                # if the thread indicator variable is set, stop the thread
                if self.stopped:
                    return

                # otherwise, read the next frame from the stream
                while len(data) < payload_size:
                    data += bytes(self.sock.recv(4096))
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("H", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += self.sock.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame_data = np.fromstring(frame_data, dtype=np.uint8)
                frame_data = cv2.imdecode(np.array(frame_data), 1)
                self.frame = frame_data
            except:
                self.stopped = True

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
