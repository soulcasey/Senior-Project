import cv2
import mediapipe as mp
import time
import numpy as np

RANGE_TARGET = 5
DARKNESS_THRESHOLD = 50

# Initialize MediaPipe's holistic model
mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FPS, 30)

# Set target points
frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
target_point_left = (frame_width // 2 + 25, frame_height // 2)
target_point_right = (frame_width // 2 - 25, frame_height // 2)

def draw_point(img, color, position):
    cv2.circle(img, position, 5, color, -1)

prev_time = time.time()  # Initialize previous time for FPS calculation

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate brightness by converting to grayscale and taking the mean
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray_frame)

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_holistic.process(frame_rgb)

    # FPS calculation
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display FPS on frame
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # If face has been detected
    if results.pose_landmarks:
        # Extract left and right eye keypoints
        left_eye = (
            int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_EYE].x * frame_width),
            int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_EYE].y * frame_height)
        )

        right_eye = (
            int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.RIGHT_EYE].x * frame_width),
            int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.RIGHT_EYE].y * frame_height)
        )

        # Draw the left and right eye reference points along with their target points
        draw_point(frame, (0, 255, 0), left_eye)
        draw_point(frame, (0, 0, 255), target_point_left)
        draw_point(frame, (0, 255, 0), right_eye)
        draw_point(frame, (0, 0, 255), target_point_right)
        
        # Calculate movement to align the reference point to the target point
        x_movement_left = target_point_left[0] - left_eye[0]
        y_movement_left = target_point_left[1] - left_eye[1]
        x_movement_right = target_point_right[0] - right_eye[0]
        y_movement_right = target_point_right[1] - right_eye[1]

        # Display coordinate and calculation information on screen for prototype
        cv2.putText(frame, f"EYE POSITION: {right_eye}, {left_eye}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"MOVE BY: ({x_movement_right}, {y_movement_right}), ({x_movement_left}, {y_movement_left})", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Check if the points are overlapped
        x_average = (x_movement_left + x_movement_right) / 2
        y_average = (y_movement_left + y_movement_right) / 2

        text = ""
        if abs(x_average) > RANGE_TARGET:
            if x_average < 0:
                text += "Left "
            else:
                text += "Right "

        if abs(y_average) > RANGE_TARGET:
            if y_average < 0:
                text += "Up "
            else:
                text += "Down "
        
        if text == "":
            text = "GOOD!"

        cv2.putText(frame, text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    elif brightness < DARKNESS_THRESHOLD: # Check if the room is too dark
        cv2.putText(frame, "ROOM TOO DARK", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
