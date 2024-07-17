import cv2
import mediapipe as mp
import numpy as np

def gen_frames():
    mp_drawing = mp.solutions.drawing_utils #drawing utilities
    mp_pose = mp.solutions.pose 

    #video feed
    cap = cv2.VideoCapture(0)

    #setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        counter = 0
        stage = "up"
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
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y,landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].z]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].z]
                right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].z]
                
                if right_hip[1] < right_knee[1] and stage == 'down' and calculate_angle(right_hip, right_knee,right_heel) > 170:
                    stage = "up"
                    counter += 1
                    print(counter)
                if right_knee[1] <= right_hip[1] and stage == 'up':
                    stage = "down"
                    print("down")

                #print(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
                #print(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
            except:
                pass

            cv2.putText(frame, str(counter), tuple([600,600]), cv2.FONT_HERSHEY_PLAIN, 10, (255,255,255), 2, cv2.LINE_AA)
            #render detections
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, 
                                    mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2))
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        
            if cv2.waitKey(10) & 0xFF == ord('q'): #break loop if screen is closed or q key is pressed
                break
        
        cap.release()
        cv2.destroyAllWindows()

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360-angle

    return angle