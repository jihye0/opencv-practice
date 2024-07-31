import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                      
    # Process the RGB frame to find hands
    result = hands.process(rgb_frame)

    # Draw the hand annotations on the frame
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get landmark coordinates
            landmarks = hand_landmarks.landmark

            # Check if the hand is open (simple logic using landmarks)
            if (landmarks[mp_hands.HandLandmark.THUMB_TIP].y <
                landmarks[mp_hands.HandLandmark.THUMB_IP].y and
                landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y <
                landmarks[mp_hands.HandLandmark.INDEX_FINGER_DIP].y and
                landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y <
                landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y and
                landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y <
                landmarks[mp_hands.HandLandmark.RING_FINGER_DIP].y and
                landmarks[mp_hands.HandLandmark.PINKY_TIP].y <
                landmarks[mp_hands.HandLandmark.PINKY_DIP].y):
                # Hand is open
                pyautogui.press('space')
                #print('!!!!!!!!!!!!!')

    # Display the resulting frame
    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()                