import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

# defining the coordinates
width = 1280
height = 720
# Webcam
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand detector
# detectionCon is the detection confidence. It is to make sure that it is really a hand that we are sending to unity
detector = HandDetector(maxHands=1, detectionCon=0.8)

# communication
# we use using UDP protocol for connecting pycharm with Unity. SOCK_DGRAM is used in case of UDP and SOCK_STREAM for TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ('127.0.0.1', 5053)

while True:
    # Get frame from Webcam
    success, img = cap.read()
    # get Hands
    hands, img = detector.findHands(img)
    # data should be defined on every iteration
    data = []
    # hand-landmark is the 21 hand-knuckle coordinates within the detected hand regions
    # each landmark consists of 3 values (x, y, z). total = (x, y, z)*21
    if hands:
        # get the first hand detected
        hand = hands[0]
        # Get the landMark List... returns a 2D array.
        lmList = hand['lmList']
        # converting the 2D array into a 1D array.
        # in opencv, y=0 is at top left and it extends downwards
        # in unity, y=0 is at bottom right and it extends upwards. So, y value should be reversed below
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])
        # sending our data to port 5052
        print(data)
        sock.sendto(str.encode(str(data)), serverAddressPort)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        quit()

