# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:34:42 2020

@author: Amir Moradi
"""

import numpy as np
import cv2, glob

def StereoCalibration(chess_size, square_size):
    
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    
    chess_height = chess_size[0]  # (8, 6)
    chess_width = chess_size[1]
    
    objp = np.zeros((chess_height*chess_width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:chess_height, 0:chess_width].T.reshape(-1, 2) * square_size
    obj_pointsL = []  # 3d point in real world space
    obj_pointsR = []

    img_points_l = []  # 2d points in image plane.
    img_points_r = []  # 2d points in image plane.
    
    images_right = glob.glob('SmartCar/calibration/Images/Right/*.png')
    images_left = glob.glob('SmartCar/calibration/Images/Left/*.png')
    
    images_left.sort()
    images_right.sort()

    for i, fname in enumerate(images_right):
        img_l = cv2.imread(images_left[i])
        img_r = cv2.imread(images_right[i])

        gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
        gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret_l, corners_l = cv2.findChessboardCorners(gray_l, (chess_height, chess_width), None)
        ret_r, corners_r = cv2.findChessboardCorners(gray_r, (chess_height, chess_width), None)

        # If found, add object points, image points (after refining them)
        if ret_l is True and ret_r is True:
            cv2.cornerSubPix(gray_l, corners_l, (11,11), (-1,-1), criteria)
            img_points_l.append(corners_l)
            obj_pointsL.append(objp)
            
            #ret_l = cv2.drawChessboardCorners(img_l, (chess_height, chess_width), corners_l, ret_l)
            #cv2.imshow(images_left[i], img_l)
            #cv2.waitKey(500)    

            cv2.cornerSubPix(gray_r, corners_r, (11,11), (-1,-1), criteria)
            img_points_r.append(corners_r)
            obj_pointsR.append(objp)
            
            #ret_r = cv2.drawChessboardCorners(img_r, (chess_height, chess_width), corners_r, ret_r)
            #cv2.imshow(images_right[i], img_r)
            #cv2.waitKey(500)
            
    
    img_l = cv2.imread(images_left[0])
    gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
    h_l, w_l = gray_l.shape
    
    img_r = cv2.imread(images_right[0])
    gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
    h_r, w_r = gray_r.shape
    

    
    rt, M_L, distorsionL, rotationL, translationL = cv2.calibrateCamera(obj_pointsL, img_points_l, (w_l, h_l), None, None)
    rt, M_R, distorsionR, rotationR, translationR = cv2.calibrateCamera(obj_pointsR, img_points_r, (w_r, h_r), None, None)

    stereocalib_flags = 0
    stereocalib_flags |= cv2.CALIB_FIX_INTRINSIC
    #stereocalib_flags |= cv2.CALIB_FIX_PRINCIPAL_POINT
    #stereocalib_flags |= cv2.CALIB_USE_INTRINSIC_GUESS
    stereocalib_flags |= cv2.CALIB_FIX_FOCAL_LENGTH
    #stereocalib_flags |= cv2.CALIB_FIX_ASPECT_RATIO
    stereocalib_flags |= cv2.CALIB_ZERO_TANGENT_DIST
    #stereocalib_flags |= cv2.CALIB_RATIONAL_MODEL
    #stereocalib_flags |= cv2.CALIB_SAME_FOCAL_LENGTH
    #stereocalib_flags |= cv2.CALIB_FIX_K3
    #stereocalib_flags |= cv2.CALIB_FIX_K4
    #stereocalib_flags |= cv2.CALIB_FIX_K5

    stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 100, 0.001)
    #stereocalib_flags = cv2.CALIB_FIX_ASPECT_RATIO | cv2.CALIB_RATIONAL_MODEL | cv2.CALIB_FIX_K3 | cv2.CALIB_FIX_K4 | cv2.CALIB_FIX_K5

    ret, Camera_L_Matrix, distorsionL, Camera_R_Matrix, distorsionR, R, T, E, F = cv2.stereoCalibrate(obj_pointsR, img_points_l, img_points_r, M_L, distorsionL, M_R, distorsionR, (w_l, h_l), criteria = stereocalib_criteria, flags = stereocalib_flags)
    
    Ret_L, Ret_R, Proj_L, Proj_R, disp_to_depth_mat, roi_left, roi_right = cv2.stereoRectify(Camera_L_Matrix, distorsionL, Camera_R_Matrix, distorsionR, (w_l, h_l), R, T, alpha = 0)
   
    total_errorL = 0
    total_errorR = 0
    for i in range(len(obj_pointsL)):
        img_points2L, _ = cv2.projectPoints(obj_pointsL[i], rotationL[i], translationL[i], Camera_L_Matrix, distorsionL)
        img_points2R, _ = cv2.projectPoints(obj_pointsR[i], rotationR[i], translationR[i], Camera_R_Matrix, distorsionR)
        errorL = cv2.norm(img_points_l[i],img_points2L, cv2.NORM_L2)/len(img_points2L)
        errorR = cv2.norm(img_points_r[i],img_points2R, cv2.NORM_L2)/len(img_points2R)
        total_errorL += errorL
        total_errorR += errorR

    print("mean error for Left Camera: ", total_errorL/len(obj_pointsL))
    print("mean error for Right Camera: ", total_errorR/len(obj_pointsR))
    
    #### SAVE MATRIX AS NUMPY ARRAY
    
    calib_params = dict([('M_L', Camera_L_Matrix), ('M_R', Camera_R_Matrix), ('distL', distorsionL), ('distR', distorsionR), ('rotation_vec_L', rotationL),('rotation_vec_R', rotationR), ('R', R), ('T', T),('E', E), ('F', F), ('Proj_L', Proj_L), ('Proj_R', Proj_R)])
    return calib_params
