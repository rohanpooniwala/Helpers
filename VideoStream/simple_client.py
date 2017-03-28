import cv2
import socket
from videostreamer import sendframe

cap = cv2.VideoCapture(0)
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.43.167'
port = 8089
clientsocket.connect((host, port))

ret = True

while ret:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (320, 240))
    ret = sendframe(clientsocket, frame)

clientsocket.close()
cap.release()
cv2.destroyAllWindows()
