import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
import numpy as np
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import IAudioEndpointVolume, AudioUtilities

#################################
wCam, HCam = 1280, 720
#################################

ctime = 0
ptime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, HCam)

detector = htm.handDetector(detectionCon=0.75)

# Setup Audio control
device = AudioUtilities.GetSpeakers()
interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# State variables
prev_length_left = None
prev_length_right = None
dead_zone = 10  # Minimum change in length to update

vol = 0.5
brightness = 50

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    hands = detector.findPosition(img, draw=False)

    for hand in hands:
        lmList = hand["lmList"]
        handedness = hand["handedness"]

        if len(lmList) != 0 and handedness == "Right":
            # Right hand → volume
            x1, y1 = lmList[4][1], lmList[4][2]  # thumb
            x2, y2 = lmList[8][1], lmList[8][2]  # index
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            if prev_length_right is None or abs(length - prev_length_right) > dead_zone:
                vol = np.interp(length, [50, 400], [0.0, 1.0])
                print('Volume: ', int(length), int(vol * 100))
                volume.SetMasterVolumeLevelScalar(vol, None)
                prev_length_right = length

        elif len(lmList) != 0 and handedness == "Left":
            # Left hand → brightness
            x1, y1 = lmList[4][1], lmList[4][2]  # thumb
            x2, y2 = lmList[8][1], lmList[8][2]  # index
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)

            if prev_length_left is None or abs(length - prev_length_left) > dead_zone:
                brightness = int(np.interp(length, [50, 400], [0, 100]))
                sbc.set_brightness(brightness)
                print('Brightness: ', int(length), int(brightness))
                prev_length_left = length

    # Volume bar
    vol_bar_len = np.interp(vol, [0.0, 1.0], [440, 180])
    cv2.rectangle(img, (1230, 180), (1195, 440), (0, 0, 0), 2)
    cv2.rectangle(img, (1230, int(vol_bar_len)), (1195, 440), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(vol * 100)} %', (1190, 470), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    # Brightness bar
    brightness_bar_len = np.interp(brightness, [0, 100], [440, 180])
    cv2.rectangle(img, (50, 180), (85, 440), (0, 0, 0), 2)
    cv2.rectangle(img, (50, int(brightness_bar_len)), (85, 440), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'{int(brightness)} %', (80, 470), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    # FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

    cv2.imshow("Gesture_Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('Quitting')
        break

cap.release()
cv2.destroyAllWindows()
