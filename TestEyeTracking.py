from EyeTracking import EyeTracking, Direction
import argparse

parser = argparse.ArgumentParser(description="Automatic Rear View Mirror")

# Add arguments
parser.add_argument('--headless', action='store_true', help="Enable headless mode (no GUI)")
args = parser.parse_args()
headless = args.headless

# Initialize the eye tracking and controller objects
eye_tracking = EyeTracking(headless)

# Main loop
try:
    while True:
        eye_tracking.loop(True)
        

finally:
    eye_tracking.exit()
