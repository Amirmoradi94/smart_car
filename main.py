# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:40:05 2020

@author: Amir Moradi
"""


import cv2
from utils.undistortion import undistortion
from utils.angle_calculation import angle_calculation
import numpy as np
import serial

video_StreamL = cv2.VideoCapture(2)  # index of left camera
video_StreamR = cv2.VideoCapture(1)  # index of right camera

face_cascade = cv2.CascadeClassifier('SmartCar/Cascades/haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('SmartCar/Cascades/haarcascade_eye_tree_eyeglasses.xml')

cen_eyesL = []
cen_eyesR = []

Proj_R = np.load("SmartCar/Calibration/matrices/Proj_R.npy")
Proj_L = np.load("SmartCar/Calibration/matrices/Proj_L.npy")

ser = serial.Serial("COM5", 9600)


mirror_pt = [-10, 10, 150]

while(True):
    
    retL, imgL = vidStreamL.read()
    retR, imgR = vidStreamR.read()

    imgL, imgR = undistortion(imgL, imgR)
    
    grayL = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)
    grayR = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
    
    try:
        facesL = face_cascade.detectMultiScale(grayL, 1.3, 5)
        facesR = face_cascade.detectMultiScale(grayR, 1.3, 5)
        
        for (x_l, y_l, w_l, h_l), (x_r, y_r, w_r, h_r) in zip(facesL, facesR):
            roi_grayL = grayL[y_l:y_l+h_l, x_l:x_l+w_l]
            roi_grayR = grayR[y_r:y_r + h_r, x_r:x_r + w_r]
            
            eyesL = eye_cascade.detectMultiScale(roi_grayL)
            eyesR = eye_cascade.detectMultiScale(roi_grayR)
            
            inter_l = []
            inter_r = []
            
            for (ex_l,ey_l,ew_l,eh_l), (ex_r,ey_r,ew_r,eh_r) in zip(eyesL, eyesR):
                cv2.rectangle(imgL, (ex_l + x_l, ey_l + y_l), (ex_l + ew_l + x_l, ey_l + eh_l + y_l), (0,255,0), 2)
                cv2.rectangle(imgR, (ex_r + x_r, ey_r + y_r), (ex_r + ew_r + x_r, ey_r + eh_r + y_r), (0,255,0), 2)
                
                inter_l.append(((2 * ex_l + ew_l)/2, (2 * ey_l + eh_l)/2))
                inter_r.append(((2 * ex_r + ew_r)/2, (2 * ey_r + eh_r)/2))
            
            eyeL_lو eyeR_l = inter_l[0], inter_l[1]
            
            eyeLx_l = eyeL_l[0]
            eyeLy_l = eyeL_l[1]
            eyeRx_l = eyeR_l[0]
            eyeRy_l = eyeR_l[1]
            
            eyeL_r = inter_r[0]
            eyeR_r = inter_r[1]
            
            eyeLx_r = eyeL_r[0]
            eyeLy_r = eyeL_r[1]
            eyeRx_r = eyeR_r[0]
            eyeRy_r = eyeR_r[1]
    
            cen_pos_l = (int((eyeLx_l + eyeRx_l)/2 + x_l), int((eyeLy_l + eyeRy_l)/2 + y_l))
            cen_pos_r = (int((eyeLx_r + eyeRx_r)/2 + x_r), int((eyeLy_r + eyeRy_r)/2 + y_r))
            
            cen_eyesL.append(cen_pos_l)
            cen_eyesR.append(cen_pos_r)
            
            ptL = np.array([[cen_pos_l[0]], [cen_pos_l[1]]], dtype=np.float)
            ptR = np.array([[cen_pos_r[0]], [cen_pos_r[1]]], dtype=np.float)
            
            cv2.circle(imgL, cen_pos_l, radius=1, color=(0, 0, 255), thickness=10)
            cv2.circle(imgR, cen_pos_r, radius=1, color=(0, 0, 255), thickness=10)
            
            xyz_points = cv2.triangulatePoints(Proj_L, Proj_R, ptL, ptR)
            xyz_points /= xyz_points[3]
            
            driver_pt = [int(xyz_points[0][0]), int(xyz_points[1][0]), int(xyz_points[2][0])]
            yaw, pitch = angle_calculation(driver_pt, mirror_pt)
            
            pitch_angle = f"S2={pitch}"
            yaw_angle = f"S1={yaw}"
            
            ser.write(pitch_angle.encode())
            ser.write(yaw_angle.encode())
            
            """
            text_z = "Z is: {} cm".format(int(xyz_points[2][0]))
            text_y = "Y is: {} cm".format(int(xyz_points[1][0]))
            text_x = "X is: {} cm".format(int(xyz_points[0][0]))
            cv2.putText(imgL, text_z, (int(w_l/2) + 20, int(h_l/2)), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 0, 0), 2) 
            cv2.putText(imgL, text_y, (int(w_l/2) + 20, int(h_l/2)+35), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 0, 0), 2) 
            cv2.putText(imgL, text_x, (int(w_l/2) + 20, int(h_l/2)+70), cv2.FONT_HERSHEY_SIMPLEX,  0.5, (255, 0, 0), 2) 
            """
            
            origin_R = np.dot(Proj_R[:3], xyz_points)
            origin_L = np.dot(Proj_L[:3], xyz_points)
            
            # Again, put in homogeneous form before using them
            origin_R /= origin_R[2]
            origin_L /= origin_L[2]
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        cv2.imshow('imgL', imgL)
        cv2.imshow('imgR', imgR)
        
    except:
        pass
ser.close()
cv2.destroyAllWindows()
