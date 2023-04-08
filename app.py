#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np

app = Flask(__name__)

#defines route for homepage to render html file
@app.route('/')
def index():
    return render_template('index.html')

#helper function called by video_feed(). Opens webcam and records user.
def gen_frames():
    mp_drawing = mp.solutions.drawing_utils #drawing utilities
    mp_pose = mp.solutions.pose 

    #video feed
    cap = cv2.VideoCapture(0)

    #setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            
            #recolor image to rgb
            # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # #saves memory
            # image.flags.writeable = False
            
            #make detection
            results = pose.process(frame)
            
            #recolor back to bgr
            # image.flags.writeable = True
            # image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
            #Extract Landmarks
            try:
                landmarks = results.pose_landmarks.landmark
                print(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
                print(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
            except:
                pass

            #render detections
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, 
                                    mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))
            
            cv2.imshow('Mediapipe Feed', frame)
        
            #neee
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
            #grege

            if cv2.waitKey(10) & 0xFF == ord('q'): #break loop if screen is closed or q key is pressed
                break
        
        cap.release()
        cv2.destroyAllWindows()

#video_feed() function is ran when requests /video_feed url
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__': #checks if current file is ran as main script
    app.run(debug=True) #starts flask dev server 