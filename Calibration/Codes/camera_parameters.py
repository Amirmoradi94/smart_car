# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 19:37:53 2020

@author: Amir Moradi
"""

import numpy as np
from stereo_calibration import StereoCalibration

chess_size = (8,6)
square_size = 2.5   # cm

camera_model = StereoCalibration(chess_size, square_size)

Camera_L_Matrix = np.array(camera_model['M_L'])
Camera_R_Matrix = np.array(camera_model['M_R'])
distorsionL = np.array(camera_model['distL'])
distorsionR = np.array(camera_model['distR'])
R = np.array(camera_model['R'])
T = np.array(camera_model['T'])
Proj_L = np.array(camera_model['Proj_L'])
Proj_R = np.array(camera_model['Proj_R'])

np.save("E:/In Use/Projects/SmartCar/calibration/matrix/Camera_L_Matrix.npy", Camera_L_Matrix)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/Camera_R_Matrix.npy", Camera_R_Matrix)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/distorsionL.npy", distorsionL)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/distorsionR.npy", distorsionR)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/R.npy", R)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/T.npy", T)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/Proj_L.npy", Proj_L)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/Proj_R.npy", Proj_R)
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/Rotation_L.npy", np.array(camera_model['rotation_vec_L']))
np.save("E:/In Use/Projects/SmartCar/calibration/matrix/Rotation_R.npy", np.array(camera_model['rotation_vec_R']))




