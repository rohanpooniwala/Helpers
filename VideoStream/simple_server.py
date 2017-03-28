import socket
import cv2
from videostreamer import InternetVideoStream

HOST = 'localhost'
PORT = 8089
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')
s.bind((HOST,PORT))
print ('Socket bind complete')
s.listen(10)
print ('Socket now listening')

conn, addr = s.accept()

vid = InternetVideoStream(conn)
vid.start()

while True:
    frame = vid.read()
    cv2.imshow('frame', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

    if vid.stopped:
        break

vid.stop()
cv2.destroyAllWindows()
