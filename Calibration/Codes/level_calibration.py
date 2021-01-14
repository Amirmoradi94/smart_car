# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:32:13 2020

@author: Amir Moradi
"""

import cv2

camL = cv2.VideoCapture(1)
camR = cv2.VideoCapture(2)


while True:
    retL, frameL = camL.read()
    retR, frameR = camR.read()
    if not retR  and not retL:
        print("failed to grab frame")
        break
    height_L = frameL.shape[0]
    width_L = frameL.shape[1]
    
    height_R = frameR.shape[0]
    width_R = frameR.shape[1]
    
    cv2.line(frameL, (0, int(height_L/2)), (width_L, int(height_L/2)), color = (255, 0, 0), thickness = 3)
    cv2.line(frameR, (0, int(height_R/2)), (width_R, int(height_R/2)), color = (255, 0, 0), thickness = 3)
    cv2.imshow("frameL", frameL)
    cv2.imshow("frameR", frameR)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    

camL.release()
camR.release()

cv2.destroyAllWindows()
