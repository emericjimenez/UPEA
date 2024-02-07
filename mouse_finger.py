#pip install -q mediapipe==0.9.0.1
import cv2
import math
import numpy as np
import mediapipe as mp
import pyautogui
import sys
import  time

from win32api import GetSystemMetrics
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pyautogui.FAILSAFE= False

# Flags for click detection
_oneClick = False
_twoClick = False
bMove = True
bClick = True

# Previous mouse position
posXtemp = 0
posYtemp = 0

# Timer variables
time_ = 0
ini_of_time = time.time()


# Capture video from webcam
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def segundos():
    """
    Tracks elapsed time and resets click flag every 2 seconds.
    """
    global time_
    global ini_of_time
    global bClick
    time_final = time.time() 
    time_elapsed = int(time_final - ini_of_time)
    if time_elapsed % 2 == 0:
        if(time!=time_elapsed):
            #print ("%d segundos.", (time_elapsed))
            time_ = time_elapsed
            bClick = True
            if(time_>1):
                time_ = 0
                ini_of_time = time.time()

def move_mouse(PercentX,PercentY):
    """
    Moves the mouse to a specified percentage of the screen based on hand position.
    Handles clicking based on finger gestures.

    Args:
        PercentX (float): Percentage of screen width for X coordinate.
        PercentY (float): Percentage of screen height for Y coordinate.
    """
    global posXtemp
    global posYtemp    
    global bClick
    global ini_of_time
    global time_
    global _oneClick
    global _twoClick
    global bMove

    # Get screen dimensions
    width_screen = GetSystemMetrics(0)
    height_screen = GetSystemMetrics(1)

    # Convert percentages to pixels
    width_units = width_screen/100
    height_units = height_screen/100

    # Calculate pixel coordinates
    poxXCompu = int(width_units*PercentX)
    poxYCompu = int(height_units*PercentY)

    # Move mouse if position changed and movement is enabled
    if(posXtemp != poxXCompu or posYtemp != poxYCompu):        
        if(bMove==True):
            
            pyautogui.moveTo(poxXCompu, poxYCompu)            

        # Handle single click based on middle finger gesture
        if(_oneClick==True):
            #print(_oneClick)
            pyautogui.click(poxXCompu, poxYCompu)     
        # Handle double click based on ring finger gesture
        if(_twoClick==True):
            pyautogui.click(poxXCompu, poxYCompu)
            pyautogui.doubleClick()         
        
        # Reset click flag and timer
        bClick = False
        ini_of_time = time.time()
        time_ = 0      
        posXtemp = poxXCompu
        posYtemp = poxYCompu

def distance(x0,x1,y0,y1):
    """
    Calculates the Euclidean distance between two points.

    Args:
        x0 (int): X coordinate of point 1.
        x1 (int): X coordinate of point 2.
        y0 (int): Y coordinate of point 1.
        y1 (int): Y coordinate of point 2.

    Returns:
        float: Euclidean distance between the points.
    """
    xd0=x1-x0
    yd0=y1-y0
    xd0=pow(xd0, 2)
    yd0=pow(yd0, 2)
    dist =math.sqrt(xd0+yd0)
    return dist


with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,        
    min_detection_confidence=0.5) as hands:
    while True:
        ret, image = capture.read()
        if ret == False:
            break
        #Process image with OpenCV
        image = cv2.flip(image, 1)
        image_height, image_width, _ = image.shape                    
        image_rgb =cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        # Detect points
        if results.multi_hand_landmarks is not None:                
            
            for hand_landmarks in results.multi_hand_landmarks:               
                # Location of just 3 fingers for calculate distance
                x0 = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * image_width)
                y0 = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y * image_height)  
                z0 = float(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z)

                # Finfer index
                x6 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].x * image_width)
                y6 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y * image_height)  
                z6 = float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].z)


                x8 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
                y8 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)  
                z8 = float(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z)

                x10 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].x * image_width)
                y10 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y * image_height)  
                z10 = float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].z)
                
                x12 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image_width)
                y12 = int(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height)  
                z12 = float(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z)

                x14 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].x * image_width)
                y14 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y * image_height)

                x16  = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * image_width)
                y16 = int(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height)

                # locate index finger
                cv2.circle(image, (x8, y8), 3,(255,0,0),3)
                indice_0_8 = distance(x0,x8,y0,y8)          
                medio_0_10 = distance(x0,x10,y0,y10)
                medio_0_12 = distance(x0,x12,y0,y12)
                    
                porcX = x6/(image_width/100)
                porcY = y6/(image_height/100)                
                porcX = 100-porcX

                indice_0_6 = distance(x0,x6,y0,y6)
                indice_0_8 = distance(x0,x8,y0,y8)
                medio_0_10 = distance(x0,x10,y0,y10)
                medio_0_12 = distance(x0,x12,y0,y12)
                anular_0_14 = distance(x0,x14,y0,y14)
                anular_0_16 = distance(x0,x16,y0,y16)

                # Detect bend or stretched
                if(indice_0_6>indice_0_8):
                    print("Ind bend")
                    bMove = False
                else:
                    print("Ind stretched")
                    bMove = True
                if(medio_0_10>medio_0_12):
                    print("Med bend")
                    _oneClick = False
                else:
                    print("Med stretched")
                    _oneClick = True
                if(anular_0_14>anular_0_16):
                    print("CAnu bend")
                    _twoClick = False
                else:
                    print("Anu stretched")
                    _twoClick = True

                # Move mouse
                move_mouse(porcX,porcY)

                # time for released
                segundos()
        # Paint the result
        cv2.imshow('MediaPipe Hand', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
                break
capture.release()
