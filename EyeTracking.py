from enum import Enum
import cv2
import mediapipe as mp
import time
import numpy as np
import math

DISTANCE_RANGE = 5
ANGLE_RANGE = 10
DARKNESS_THRESHOLD = 60
AXIS_X = 400
AXIS_Y = 400
TARGET_OFFSET = 25

class Direction(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    # UP = "UP"
    # DOWN = "DOWN"
    CW = "CLOCKWISE"
    CCW = "COUNTERCLOCKWISE"

def calcualte_angle(left, right):
    dx = right[0] - left[0]
    dy = right[1] - left[1]

    # Calculate the angle in radians
    angle_radians = math.atan2(dy, dx)

    # Convert to degrees
    return math.degrees(angle_radians) * -1 # Muliply -1 due to frame's y axis being fliped

class EyeTracking:
    def __init__(self, headless: bool):
        # Initialize face mesh model instead of holistic for more precise eye detection
        self.mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8)
        
        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, AXIS_X)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, AXIS_Y)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        # Set target points
        self.frame_width, self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.target_point_right = (142, 168)
        self.target_point_left = (199, 144)

        # Convert to degrees
        self.target_angle = calcualte_angle(self.target_point_left, self.target_point_right)

        self.instruction_sequence = []
        self.prev_time = time.time()  # Initialize previous time for FPS calculation
        self.headless = headless
        self.is_dark = False

    def draw_point(self, img, color, position):
        cv2.circle(img, position, 5, color, -1)

    def calculate_fps(self):
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time
        return fps

    def loop(self, testMode = False):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("No camera")

        # Calculate brightness by converting to grayscale and taking the mean
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray_frame)
        
        if brightness < DARKNESS_THRESHOLD:  # Check if the room is too dark
            self.is_dark = brightness < DARKNESS_THRESHOLD

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_holistic.process(frame_rgb)


        self.instruction_sequence.clear()
    
        # FPS calculation
        fps = self.calculate_fps()

        # If face landmarks have been detected
        if results.pose_landmarks:
            left_eye = (
            int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_EYE].x * self.frame_width),
            int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.LEFT_EYE].y * self.frame_height)
            )

            right_eye = (
                int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.RIGHT_EYE].x * self.frame_width),
                int(results.pose_landmarks.landmark[mp.solutions.holistic.PoseLandmark.RIGHT_EYE].y * self.frame_height)
            )

            # Calculate movement to align the reference point to the target point
            x_movement_left = self.target_point_left[0] - left_eye[0]
            y_movement_left = self.target_point_left[1] - left_eye[1]
            x_movement_right = self.target_point_right[0] - right_eye[0]
            y_movement_right = self.target_point_right[1] - right_eye[1]

            # Check if the points are angled
            
            self.instruction_sequence.clear()

            current_angle = calcualte_angle(left_eye, right_eye)
            angle_difference = self.target_angle - current_angle
            if angle_difference < -180:
                angle_difference += 360

            if abs(angle_difference) > ANGLE_RANGE:
                if angle_difference < 0:
                    self.instruction_sequence.append(Direction.CW)
                else:
                    self.instruction_sequence.append(Direction.CCW)

            # Check if the points are overlapped
            x_average = (x_movement_left + x_movement_right) / 2
            y_average = (y_movement_left + y_movement_right) / 2

            if abs(x_average) > DISTANCE_RANGE:
                if x_average < 0:
                    self.instruction_sequence.append(Direction.LEFT)
                else:
                    self.instruction_sequence.append(Direction.RIGHT)

            # if abs(y_average) > RANGE_TARGET:
            #     if y_average < 0:
            #         self.move_direction.append(Direction.UP)
            #     else:
            #         self.move_direction.append(Direction.DOWN)
            
            if self.headless is False:

                # Display FPS on frame
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Draw the left and right eye reference points along with their target points
                self.draw_point(frame, (0, 255, 0), left_eye)
                self.draw_point(frame, (0, 0, 255), self.target_point_left)
                self.draw_point(frame, (0, 255, 0), right_eye)
                self.draw_point(frame, (0, 0, 255), self.target_point_right)

                # Display coordinate and calculation information on screen for prototype
                cv2.putText(frame, f"{right_eye}, {left_eye}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(frame, f"({x_average}, {y_average})", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

                if self.is_dark:
                    cv2.putText(frame, "ROOM TOO DARK", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                move_direction_text = ', '.join([direction.value for direction in self.instruction_sequence]) if len(self.instruction_sequence) > 0 else "GOOD"
                cv2.putText(frame, move_direction_text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    

        # if testMode:
        #     self.test(frame)

        if self.headless:
            # if len(self.move_direction) > 0:
            #     print(', '.join([direction.value for direction in self.move_direction]))
            None
        else:
            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
    
    def test(self, frame):
        offset = 80
        self.draw_point(frame, (160, 32, 240), (offset, self.frame_height // 2))
        self.draw_point(frame, (0, 165, 255), (self.frame_width - offset, self.frame_height // 2))
        self.draw_point(frame, (255, 255, 255), (self.frame_width // 2, offset))
        self.draw_point(frame, (0, 0, 0), (self.frame_width // 2, self.frame_height - offset))

    def exit(self):
        self.cap.release()
        cv2.destroyAllWindows()