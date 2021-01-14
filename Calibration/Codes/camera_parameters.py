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
Rotation_L = np.array(camera_model['rotation_vec_L'])
Rotation_R = np.array(camera_model['rotation_vec_R'])


np.save("SmartCar/Calibration/matrices/Camera_L_Matrix.npy", Camera_L_Matrix)
np.save("SmartCar/Calibration/matrices/Camera_R_Matrix.npy", Camera_R_Matrix)
np.save("SmartCar/Calibration/matrices/distorsionL.npy", distorsionL)
np.save("SmartCar/Calibration/matrices/distorsionR.npy", distorsionR)
np.save("SmartCar/Calibration/matrices/R.npy", R)
np.save("SmartCar/Calibration/matrices/T.npy", T)
np.save("SmartCar/Calibration/matrices/Proj_L.npy", Proj_L)
np.save("SmartCar/Calibration/matrices/Proj_R.npy", Proj_R)
np.save("SmartCar/Calibration/matrices/Rotation_L.npy", Rotation_L)
np.save("SmartCar/Calibration/matrices/Rotation_R.npy", Rotation_R)


