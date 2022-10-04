# Kyla Ramos
# CSC 355 - Homework 4 - Hand Raise
# Program that tracks the pose of the user as seen by your webcam, 
# and detects if the user’s left or right hand is raised or lowered. 
 
from unittest import result
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# flags for printing
left_lowered = False
left_raised = False
right_lowered = False
right_raised = False

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
        continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # wrist vars
    left_wrist = results.pose_landmarks.landmark[15].y
    right_wrist = results.pose_landmarks.landmark[16].y

    # shoulder vars
    left_shoulder = results.pose_landmarks.landmark[11].y
    right_shoulder = results.pose_landmarks.landmark[12].y  

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())     

    # compare left wrist to left shoulder to see if arm is raised or lowered       
    if left_wrist >= left_shoulder:
        if left_lowered == False:
            print("Left hand lowered.")
            left_lowered = True
            left_raised = False

    if left_wrist <= left_shoulder:
        if left_raised == False:
            print("Left hand raised.")
            left_raised = True
            left_lowered = False


    # compare right wrist to right shoulder to see if arm is raised or lowered       
    if right_wrist >= right_shoulder:
        if right_lowered == False:
            print("Right hand lowered.")
            right_lowered = True
            right_raised = False

    if right_wrist <= right_shoulder:
        if right_raised == False:
            print("Right hand raised.")
            right_raised = True
            right_lowered = False                  

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()