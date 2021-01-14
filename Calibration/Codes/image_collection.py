# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 19:17:57 2020

@author: Amir Moradi
"""

import cv2

camL = cv2.VideoCapture(1)
camR = cv2.VideoCapture(2)

cv2.namedWindow("test")

img_counter = 0

while True:
    retL, frameL = camL.read()
    retR, frameR = camR.read()
    if not retL or not retR:
        print("failed to grab frame")
        break
    cv2.imshow("testL", frameL)
    cv2.imshow("testR", frameR)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_nameL = "SmartCar/Calibration/images/Left/frameL_{}.png".format(img_counter)
        img_nameR = "SmartCar/Calibration/images/Right/frameR_{}.png".format(img_counter)
        cv2.imwrite(img_nameL, frameL)
        cv2.imwrite(img_nameR, frameR)
        print("{} written!".format(img_nameL))
        print("{} written!".format(img_nameR))
        img_counter += 1

camL.release()
camR.release()

cv2.destroyAllWindows()
