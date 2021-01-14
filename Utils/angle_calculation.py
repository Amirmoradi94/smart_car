# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 13:51:39 2020

@author: Amir Moradi
"""

from sympy import Point3D, Plane 
import math

def angle_calculation(driver_pt, mirror_pt):

    driver_plane = Plane(Point3D(0, 0, 0), Point3D(driver_pt[0], 0, driver_pt[2]), Point3D(driver_pt[0], driver_pt[1], driver_pt[2]))
    mirror_plane = Plane(Point3D(0, 0, 0), Point3D(mirror_pt[0], 0, mirror_pt[2]), Point3D(mirror_pt[0], mirror_pt[1], mirror_pt[2]))
    xy = Plane(Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 1, 0))
    xz = Plane(Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(0, 0, 1))
    
    alpha = driver_plane.angle_between(mirror_plane)
    betta = driver_plane.angle_between(xy)
    yaw = math.degrees(alpha/2 + betta)
    slope = math.tan(alpha/2 + betta)  # slope of bisector line of two planes
    #print(slope)

    bisector_pt1 = tuple(driver_plane.intersection(mirror_plane)[0].points[0])
    bisector_pt2 = tuple(driver_plane.intersection(mirror_plane)[0].points[1])
    bisector_pt3 = (1, 0, slope)
    
    bisector_plane = Plane(Point3D(bisector_pt1[0], bisector_pt1[1], bisector_pt1[2]), Point3D(bisector_pt2[0], bisector_pt2[1], bisector_pt2[2]), Point3D(bisector_pt3[0], bisector_pt3[1], bisector_pt3[2]))
    driver_mirror_plane = Plane(Point3D(0, 0, 0), Point3D(driver_pt[0], driver_pt[1], driver_pt[2]), Point3D(mirror_pt[0], mirror_pt[1], mirror_pt[2]))
    
    final_line = bisector_plane.intersection(driver_mirror_plane)
    final_pt = tuple(final_line[0].points[1])
    
    #print('Yaw Angle: ',math.degrees(math.atan2(final_pt[2], final_pt[0])))
    #print('Pitch Angle: ', math.degrees(driver_mirror_plane.angle_between(xz)))
    
    yaw = math.degrees(math.atan2(final_pt[2], final_pt[0]))
    pitch = math.degrees(driver_mirror_plane.angle_between(xz))
    
    return yaw, pitch
