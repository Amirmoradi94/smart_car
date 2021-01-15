# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:48:41 2020

@author: Amir Moradi
"""



import cv2
import numpy as np


def undistortion(img_1, img_2):
    
    h, w = img_1.shape[:2]
    
    Camera_L_Matrix = np.load("SmartCar/Calibration/matrices/matrix/Camera_L_Matrix.npy")
    Camera_R_Matrix = np.load("SmartCar/Calibration/matrices/Camera_R_Matrix.npy")
    distorsionL = np.load("SmartCar/Calibration/matrices/distorsionL.npy")
    distorsionR = np.load("SmartCar/Calibration/matrices/distorsionR.npy")
    
    #Get optimal camera matrix for better undistortion 
    new_cameraL_matrix, roi_l = cv2.getOptimalNewCameraMatrix(Camera_L_Matrix, distorsionL, (w,h), 1, (w,h))
    new_cameraR_matrix, roi_r = cv2.getOptimalNewCameraMatrix(Camera_R_Matrix, distorsionR, (w,h), 1, (w,h))
    
    img_1_undistorted = cv2.undistort(img_1, Camera_L_Matrix, distorsionL, None, new_cameraL_matrix)
    img_2_undistorted = cv2.undistort(img_2, Camera_R_Matrix, distorsionR, None, new_cameraR_matrix)
    
    roi_x, roi_y, roi_w, roi_h = roi_l    
    img_1_undistorted = img_1_undistorted[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
    
    roi_x_r, roi_y_r, roi_w_r, roi_h_r = roi_r
    img_2_undistorted = img_2_undistorted[roi_y_r : roi_y_r + roi_h_r, roi_x_r : roi_x_r + roi_w_r]
    
    return img_1_undistorted, img_2_undistorted


