from Controller import ButtonType, Controller
from EyeTracking import EyeTracking, Direction
import Motor as motor
import Light as light
import argparse

parser = argparse.ArgumentParser(description="Automatic Rear View Mirror")

# Add arguments
parser.add_argument('--headless', action='store_true', help="Enable headless mode (no GUI)")
args = parser.parse_args()
headless = args.headless

# Function to toggle auto_mode on or off when START or SELECT is pressed
def toggle_auto_mode():
    global auto_mode
    auto_mode = not auto_mode
    motor.stopMotor1()
    motor.stopMotor2()
    print(f"AUTO_MODE is now {'ON' if auto_mode else 'OFF'}")
    if auto_mode:
        light.warningLight(False)
        light.startBlink()
    else:
        light.stopBlink()
        light.warningLight(True)


# Initialize the auto mode to be off by default
auto_mode = False

# Initialize the eye tracking and controller objects
eye_tracking = EyeTracking(headless)
controller = Controller()

# Set button press actions for motor control with auto_mode checks
controller.set_button_press_action(ButtonType.LEFT, lambda: motor.moveMotor1(True) if not auto_mode else None)
controller.set_button_press_action(ButtonType.RIGHT, lambda: motor.moveMotor1(False) if not auto_mode else None)

controller.set_button_press_action(ButtonType.UP, lambda: motor.moveMotor2(True) if not auto_mode else None)
controller.set_button_press_action(ButtonType.DOWN, lambda: motor.moveMotor2(False) if not auto_mode else None)

# Set button press actions for toggling auto mode
controller.set_button_press_action(ButtonType.SELECT, toggle_auto_mode)

controller.set_button_press_action(ButtonType.A, lambda: light.cameraLight(True))
controller.set_button_press_action(ButtonType.B, lambda: light.warningLight(True))

# Set button release actions to stop motors
controller.set_button_release_action(ButtonType.LEFT, lambda: motor.stopMotor1() if not auto_mode else None)
controller.set_button_release_action(ButtonType.RIGHT, lambda: motor.stopMotor1() if not auto_mode else None)

controller.set_button_release_action(ButtonType.UP, lambda: motor.stopMotor2() if not auto_mode else None)
controller.set_button_release_action(ButtonType.DOWN, lambda: motor.stopMotor2() if not auto_mode else None)

controller.set_button_release_action(ButtonType.A, lambda: light.cameraLight(False))
controller.set_button_release_action(ButtonType.B, lambda: light.warningLight(False))

# Main loop
try:
    while True:
        controller.loop()
        eye_tracking.loop()

        if auto_mode:
            if Direction.UP in eye_tracking.move_direction:
                motor.moveMotor1(True)
            elif Direction.DOWN in eye_tracking.move_direction:
                motor.moveMotor1(False)
            else:
                motor.stopMotor1()

            if Direction.LEFT in eye_tracking.move_direction:
                motor.moveMotor2(True)
            elif Direction.RIGHT in eye_tracking.move_direction:
                motor.moveMotor2(False)
            else:
                motor.stopMotor2()      
except Exception as e:
    motor.stopAllMotors()
finally:
    controller.exit()
    eye_tracking.exit()
    motor.exit()
