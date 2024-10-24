import cv2
import mediapipe as mp

# Initialize MediaPipe's holistic model
# Will be using the most basic model for prototype
mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.9, min_tracking_confidence=0.9)

# Camera setup
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
cap.set(cv2.CAP_PROP_FPS, 30)

# Set target points
# The left taget point is placed on the right as the driver's face is inverted in camera's perspective
frame_width, frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
target_point_left = (frame_width // 2 + 25, frame_height // 2)
target_point_right = (frame_width // 2 - 25, frame_height // 2)

def draw_point(img, color, position):
    cv2.circle(img, position, 5, color, -1)

while True:
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_holistic.process(frame_rgb)

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
        draw_point(frame, (0, 0, 255), left_eye)
        draw_point(frame, (0, 255, 0), target_point_left)
        draw_point(frame, (0, 0, 255), right_eye)
        draw_point(frame, (0, 255, 0), target_point_right)
        
        # Calculate movement to align the reference point to the target point
        # Only to basic distance calculation for now
        x_movement_left = target_point_left[0] - left_eye[0]
        y_movement_left = target_point_left[1] - left_eye[1]
        x_movement_right = target_point_right[0] - right_eye[0]
        y_movement_right = target_point_right[1] - right_eye[1]
        
        # Display coordinate and calculation informations on screen for prototype
        cv2.putText(frame, f"RightEyePos: {right_eye}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"MovTo: ({x_movement_right}, {y_movement_right})", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.putText(frame, f"LeftEyePos: {left_eye}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(frame, f"MovTo: ({x_movement_left}, {y_movement_left})", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Adjustment process will go here once motor is complete

        # Check if the points are overlapped
        if abs(x_movement_left) <= 3 and abs(y_movement_left) <= 3 and abs(x_movement_right) <= 3 and abs(y_movement_right) <= 3:
            cv2.putText(frame, "GOOD!", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
