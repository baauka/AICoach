import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import pickle
import streamlit as st
import time
from datetime import datetime
from database import *


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

landmarks = ['class']
for val in range(1, 33+1):
    landmarks += ['x{}'.format(val), 'y{}'.format(val), 'z{}'.format(val), 'v{}'.format(val)]


@st.cache_resource
def load_model(model_path):
    with open(model_path, 'rb') as f:
        return pickle.load(f)


st.markdown("<h1 style='text-align: center;'>Welcome to your <span style='color: #7F00FF;'>AI Coach!</span></h1>", unsafe_allow_html=True)


simpleWorkout, forMaxWeight = st.tabs(['Simple Workout', 'PR workout'])


def deadlift_run(weight,sets_choice=1, reps_choice=1):

    deadlift_model = load_model('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\deadlift.pkl')
    position_model = load_model('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\position.pkl')
    leaning_model = load_model('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\leaning.pkl')

    cap = cv2.VideoCapture(0)

    counter = 0 
    set_counter = 1
    mistakes_counter = 0
    mistakes_all = 0
    stage = None
    mistake_detected = False
    success_of_workout = 100

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while set_counter <= sets_choice:
            while cap.isOpened() and counter < reps_choice:
                ret, frame = cap.read()

                frame = cv2.resize(frame, (1240, 780))

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                try:
                    row = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten().tolist()
                    X = pd.DataFrame([row], columns=landmarks[1:])
                    body_language_class_up_down = deadlift_model.predict(X)[0]
                    body_language_prob_up_down = deadlift_model.predict_proba(X)[0]

                    body_language_class_position = position_model.predict(X)[0]
                    body_language_prob_position = position_model.predict_proba(X)[0]

                    body_language_class_leaning = leaning_model.predict(X)[0]
                    body_language_prob_leaning = leaning_model.predict_proba(X)[0]

                    if success_of_workout < 70:
                        return

                    if body_language_class_up_down == 'down' and body_language_prob_up_down[body_language_prob_up_down.argmax()] >= 0.7:
                        stage = 'down'
                    elif stage == 'down' and body_language_class_up_down == 'up' and body_language_prob_up_down[body_language_prob_up_down.argmax()] >= 0.7:
                        stage = 'up'
                        counter += 1
                        mistake_detected = False  # Reset mistake detection for new rep

                    if stage == 'down' and not mistake_detected:
                        if body_language_class_position in ['wide', 'narrow']:
                            mistakes_counter += 1
                            success_of_workout-=5
                            mistake_detected = True 
                        

                    # Render curl counter
                    # Setup status box
                    #--------------------------------------------------------------------------------------
                    cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)
                    cv2.rectangle(image, (990, 0), (1240, 60), (245, 117, 16), -1)
                    cv2.rectangle(image, (990, 60), (1240, 120), (23, 23, 226), -1)  # BGR
                    cv2.rectangle(image, (0,60), (250, 120), (23, 23, 226), -1)
                    # Rep data
                    cv2.putText(image, 'CLASS', (95, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_up_down.split(' ')[0], (90, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    

                    cv2.putText(image, 'SET', (18, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    cv2.putText(image, str(set_counter), (25, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'MISTAKES', (105, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    cv2.putText(image, str(mistakes_counter), (135, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)

                    # Stage data
                    cv2.putText(image, 'PROB', (15, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_up_down[np.argmax(body_language_prob_up_down)], 2)),
                                (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    cv2.putText(image, 'COUNT', (180, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(counter),
                                (175, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    # -----------------------------------POSITION----------------------------------

                    cv2.putText(image, 'POSITION', (1000, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_position.split(' ')[0], (1000, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    cv2.putText(image, 'PROB', (1120, 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_position[np.argmax(body_language_prob_position)], 2)),
                                (1120, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                    # ----------------------------------------------------------------------------------

                    cv2.putText(image, 'LEANING', (1000, 72),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_leaning.split(' ')[0], (1000, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                    cv2.putText(image, 'PROB', (1120, 72),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_leaning[np.argmax(body_language_prob_leaning)], 2)),
                                (1120, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                except Exception as e:
                    pass

                cv2.imshow('Deadlift', image)

                if cv2.waitKey(1) & 0xFF == ord('i'):
                    counter+=1
                elif cv2.waitKey(1) & 0xFF == ord('r'):
                    counter=0
                    mistakes_counter=0
                    success_of_workout=100
                elif cv2.waitKey(1) & 0xFF == ord('f'):
                    counter=0
                    set_counter+=1
                    mistakes_counter=0
                    success_of_workout-=5
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            # Reset the rep counter for the next set
            counter = 0
            set_counter += 1
            mistakes_all += mistakes_counter

        cap.release()
        cv2.destroyAllWindows()

        date = datetime.now().strftime('%Y-%m-%d')
        username = get_username(st.session_state.global_email)

        if int(sets_choice) == 1 and int(reps_choice) == 1 and mistakes_all == 0:
            insert_patient_max_weight_info('Deadlift', username, float(weight), str(st.session_state.global_email), date)
        else:
            insert_patient_exercise(str(st.session_state.global_email), 'Deadlift', int(reps_choice), int(sets_choice), int(success_of_workout), float(weight), username, int(mistakes_all), date)


def biceps_curl_run(weight, sets_choice=1, reps_choice=1):
    
    biceps_up = load_model('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\biceps_curl.pkl')
    biceps_back_model = load_model('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\biceps_curl_back.pkl')

    cap = cv2.VideoCapture(0)

    counter = 0 
    set_counter = 1
    mistakes_counter = 0
    stage = None
    mistake_detected = False
    mistakes_all = 0

    #if complete pressed -5, for mistake -5, 

    success_of_workout = 100

    stage = None
    posture = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while set_counter <= sets_choice:
            while cap.isOpened() and counter < reps_choice:
                ret, frame = cap.read()

                frame = cv2.resize(frame, (1240,780))
                
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
            
                # Make detection
                results = pose.process(image)
            
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )   
                
                try:
                    row = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten().tolist()
                    X = pd.DataFrame([row], columns=landmarks[1:])

                    body_language_class_up_down = biceps_up.predict(X)[0]
                    body_language_prob_up_down = biceps_up.predict_proba(X)[0]


                    body_language_class_back = biceps_back_model.predict(X)[0]
                    body_language_prob_back = biceps_back_model.predict_proba(X)[0]


                    if success_of_workout < 70:
                        return
                    
                    if body_language_class_up_down == 'down' and body_language_prob_up_down[body_language_prob_up_down.argmax()] >= 0.7:
                        stage = 'down'
                    elif stage == 'down' and body_language_class_up_down == 'up' and body_language_prob_up_down[body_language_prob_up_down.argmax()] >= 0.7:
                        stage = 'up'
                        counter += 1
                        mistake_detected = False  # Reset mistake detection for new rep

                    if stage == 'down' and not mistake_detected:
                        if body_language_class_back == 'critical':
                            mistakes_counter += 1
                            success_of_workout-=5
                            mistake_detected = True 

                # Render curl counter
                # Setup status box
                    cv2.rectangle(image, (0,0), (250,60), (245,117,16), -1)
                    cv2.rectangle(image, (990, 0), (1240, 60), (245,117,16), -1)
                    cv2.rectangle(image, (0,60), (250, 120), (23, 23, 226), -1)

                    
                    # Rep data 
                    cv2.putText(image, 'CLASS', (95,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_up_down.split(' ')[0], (90,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    

                    cv2.putText(image, 'SET', (18, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    cv2.putText(image, str(set_counter), (25, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'MISTAKES', (105, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    cv2.putText(image, str(mistakes_counter), (135, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    # Stage data
                    cv2.putText(image, 'PROB', (15,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_up_down[np.argmax(body_language_prob_up_down)],2)), 
                                (10,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'COUNT', (180,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(counter), 
                                (175,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    # -------------------------------------------------------------------------------

                    cv2.putText(image, 'BACK_POSTURE', (1000,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_back.split(' ')[0], (1000,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'PROB', (1130,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_back[np.argmax(body_language_prob_back)],2)), 
                                (1130,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    
                    

                except Exception as e:
                    pass
                
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(1) & 0xFF == ord('i'):
                    counter+=1
                elif cv2.waitKey(1) & 0xFF == ord('r'):
                    counter=0
                    mistakes_counter=0
                    success_of_workout=100
                elif cv2.waitKey(1) & 0xFF == ord('f'):
                    counter=0
                    set_counter+=1
                    mistakes_counter=0
                    success_of_workout-=5
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            counter = 0
            set_counter += 1
            mistakes_all+=mistakes_counter

        cap.release()
        cv2.destroyAllWindows()

        date = datetime.now().strftime('%Y-%m-%d')
        username = get_username(st.session_state.global_email)
        if int(sets_choice) == 1 and int(reps_choice) == 1 and mistakes_all == 0:
            insert_patient_max_weight_info('Biceps Curl', username, float(weight), str(st.session_state.global_email), date)
        else:
            insert_patient_exercise(str(st.session_state.global_email), 'Biceps Curl', int(reps_choice), int(sets_choice), int(success_of_workout), float(weight), username, int(mistakes_all), date)





def squat_run(weight, sets_choice=1, reps_choice=1):
    with open('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\squat_up_down.pkl', 'rb') as f:
        squat_up_down_model = pickle.load(f)

    
    with open('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\squat_feet.pkl', 'rb') as f:
        squat_feet_model = pickle.load(f)

    with open('C:\\Users\\Admin\\Desktop\\Outpeer\\Project\\models\\squat_knee.pkl', 'rb') as f:
        squat_knee_model = pickle.load(f)

    cap = cv2.VideoCapture(0)

    counter = 0 
    set_counter = 1
    mistakes_counter = 0
    stage = None
    mistake_detected = False
    mistakes_all = 0
    success_of_workout = 100

    stage = None
    posture = None


    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while set_counter <= sets_choice:
            while cap.isOpened() and counter < reps_choice:
                ret, frame = cap.read()

                frame = cv2.resize(frame, (1240,780))
                
                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
            
                # Make detection
                results = pose.process(image)
            
                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )   
                
                try:
                    row = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten().tolist()
                    X = pd.DataFrame([row], columns=landmarks[1:])

                    body_language_class_up_down = squat_up_down_model.predict(X)[0]
                    body_language_prob_up_down = squat_up_down_model.predict_proba(X)[0]


                    body_language_class_feet = squat_feet_model.predict(X)[0]
                    body_language_prob_feet = squat_feet_model.predict_proba(X)[0]


                    body_language_class_knee = squat_knee_model.predict(X)[0]
                    body_language_prob_knee = squat_knee_model.predict_proba(X)[0]

                    if success_of_workout < 70:
                        return
                    
                    if stage == 'up' and not mistake_detected:
                        if body_language_class_knee == 'too_tight' or body_language_class_feet == 'too_tight':
                            mistakes_counter += 1
                            success_of_workout-=5
                            mistake_detected = True  


                    if body_language_class_up_down == 'down' and body_language_prob_up_down[body_language_prob_up_down.argmax()] >= 0.7:
                        stage = 'down'
                    elif stage == 'down' and body_language_class_up_down == 'up' and body_language_prob_up_down[body_language_prob_up_down.argmax()] >= 0.7:
                        stage = 'up'
                        counter += 1
                        mistake_detected = False  # Reset mistake detection for new rep

                    
                    
            
                # Render curl counter
                # Setup status box
                    cv2.rectangle(image, (0,0), (250,60), (245,117,16), -1)
                    cv2.rectangle(image, (990, 0), (1240, 60), (245,117,16), -1)
                    cv2.rectangle(image, (990,60), (1240,120),(23,23,226),-1)
                    cv2.rectangle(image, (0,60), (250, 120), (23, 23, 226), -1)

                    
                    # Rep data 
                    cv2.putText(image, 'CLASS', (95,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_up_down.split(' ')[0], (90,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    

                    cv2.putText(image, 'SET', (18, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    cv2.putText(image, str(set_counter), (25, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'MISTAKES', (105, 80), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
                    
                    cv2.putText(image, str(mistakes_counter), (135, 110), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2, cv2.LINE_AA)
                    
                    # Stage data
                    cv2.putText(image, 'PROB', (15,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_up_down[np.argmax(body_language_prob_up_down)],2)), 
                                (10,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'COUNT', (180,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(counter), 
                                (175,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    # -------------------------------------------------------------------------------

                    cv2.putText(image, 'FEET', (1000,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_feet.split(' ')[0], (1000,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255,255,255), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'PROB', (1120,12), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_feet[np.argmax(body_language_prob_feet)],2)), 
                                (1120,40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    #----------------------------------------------------------------------------------


                    cv2.putText(image, 'KNEE', (1000,72), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, body_language_class_knee.split(' ')[0], (1000,100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.85, (255,255,255), 2, cv2.LINE_AA)
                    
                    cv2.putText(image, 'PROB', (1120,72), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
                    cv2.putText(image, str(round(body_language_prob_knee[np.argmax(body_language_prob_knee)],2)), 
                                (1120,100), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
                    
                    

                except Exception as e:
                    pass
                
                cv2.imshow('Mediapipe Feed', image)

                if cv2.waitKey(1) & 0xFF == ord('i'):
                    counter+=1
                elif cv2.waitKey(1) & 0xFF == ord('r'):
                    counter=0
                    mistakes_counter=0
                    success_of_workout=100
                elif cv2.waitKey(1) & 0xFF == ord('f'):
                    counter=0
                    set_counter+=1
                    mistakes_counter=0
                    success_of_workout-=5
                elif cv2.waitKey(1) & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    return

            counter = 0
            set_counter += 1
            mistakes_all+=mistakes_counter

        cap.release()
        cv2.destroyAllWindows()

        date = datetime.now().strftime('%Y-%m-%d')
        username = get_username(st.session_state.global_email)
        if int(sets_choice) == 1 and int(reps_choice) == 1 and mistakes_all == 0:
            insert_patient_max_weight_info('Squat', username, float(weight), str(st.session_state.global_email), date)
        else:
            insert_patient_exercise(str(st.session_state.global_email), 'Squat', int(reps_choice), int(sets_choice), int(success_of_workout), float(weight), username, int(mistakes_all), date)



with simpleWorkout:

    exercises_choice = st.selectbox(
        '**Exercise**', ['Deadlifts', 'Biceps Curls', 'Squats'],
        index=None,
        placeholder='Choose exercise type'
        )
    set_choice = st.selectbox(
        '**Sets**', ['3', '4', '5'],
        index=None,
        placeholder='Choose how many sets you want to do'
        )
    reps_choice = st.selectbox(
        '**Reps**', ['6', '8', '12'],
        index=None,
        placeholder='Choose how many reps you want to do per set'
        )
    
    
    weight_selection_simple = st.text_input('Weight', placeholder='Select the weight for workout', value=None)
    
    button = st.button('Start')
    
    all_selected_coach = (exercises_choice is not None) and (set_choice is not None) and (reps_choice is not None) and (weight_selection_simple is not None)

    if button and all_selected_coach and exercises_choice=='Deadlifts':
        deadlift_run(weight_selection_simple,int(set_choice[0]), int(reps_choice))     
    elif button and all_selected_coach and exercises_choice=='Biceps Curls':
        biceps_curl_run(weight_selection_simple,int(set_choice[0]), int(reps_choice))
    elif button and all_selected_coach and exercises_choice=='Squats':
        squat_run(weight_selection_simple,int(set_choice[0]), int(reps_choice))
        
with forMaxWeight:

    exercises_choice_max = st.selectbox(
        '**Exercise**', ['Deadlift', 'Biceps Curl', 'Squat'],
        index=None,
        placeholder='Choose exercise type'
    )

    weight_selection = st.text_input('Weight', placeholder='Select the weight for your PR', value=None)
    
    button = st.button("Let's go")

    all_selected_max = (exercises_choice_max is not None) and (weight_selection is not None)

    if button and all_selected_max and exercises_choice_max == 'Deadlift':
        deadlift_run(weight_selection)
    elif button and all_selected_max and exercises_choice_max == 'Biceps Curl':
        biceps_curl_run(weight_selection)
    elif button and all_selected_max and exercises_choice_max == 'Squat':
        squat_run(weight_selection)
