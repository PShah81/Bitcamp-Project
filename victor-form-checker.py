#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 23:08:48 2023

@author: victorsu
"""

import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils #drawing utilities
mp_pose = mp.solutions.pose 

#video feed
cap = cv2.VideoCapture(0)

#setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        
        #recolor image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        #make detection
        results = pose.process(image)
        
        #recolor back to bgr
        image.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        #render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, 
                                  mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))
        
        cv2.imshow('Mediapipe Feed', image)
    
        if cv2.waitKey(10) & 0xFF == ord('q'): #break loop if screen is closed or q key is pressed
            break
    
    cap.release()
    cv2.destroyAllWindows()