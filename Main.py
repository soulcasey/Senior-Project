from Controller import ButtonType, Controller
from EyeTracking import EyeTracking, Direction
import Motor as motor
import Light as light
import argparse
from enum import Enum

class SystemState(Enum):
    IDLE = 1
    AUTO = 2
    MANUAL = 3

parser = argparse.ArgumentParser(description="Automatic Rear View Mirror")

# Add arguments
parser.add_argument('--headless', action='store_true', help="Enable headless mode (no GUI)")
args = parser.parse_args()
headless = args.headless

def set_state(new_state: SystemState):
    global current_state
    current_state = new_state

    motor.stopAllMotors()

    if current_state == SystemState.AUTO:
        light.warningLight(False)
        light.startBlink()
    elif current_state == SystemState.MANUAL:
        light.stopBlink()
        light.warningLight(True)
    else:
        light.stopBlink()

    print(f"Current State: {current_state}")


current_state = SystemState.IDLE

# Initialize the eye tracking and controller objects
eye_tracking = EyeTracking(headless)
controller = Controller()

# Set button press actions for motor control with auto_mode checks
controller.set_button_press_action(ButtonType.LEFT, lambda: motor.moveMotor1(True) if current_state == SystemState.MANUAL else None)
controller.set_button_press_action(ButtonType.RIGHT, lambda: motor.moveMotor1(False) if current_state == SystemState.MANUAL else None)

controller.set_button_press_action(ButtonType.UP, lambda: motor.moveMotor2(True) if current_state == SystemState.MANUAL else None)
controller.set_button_press_action(ButtonType.DOWN, lambda: motor.moveMotor2(False) if current_state == SystemState.MANUAL else None)

controller.set_button_press_action(ButtonType.SELECT, lambda:set_state(SystemState.IDLE if current_state == SystemState.MANUAL else SystemState.MANUAL))
controller.set_button_press_action(ButtonType.START, lambda: set_state(SystemState.AUTO) if current_state == SystemState.IDLE else None)

# Set button release actions to stop motors
controller.set_button_release_action(ButtonType.LEFT, lambda: motor.stopMotor1() if current_state == SystemState.MANUAL else None)
controller.set_button_release_action(ButtonType.RIGHT, lambda: motor.stopMotor1() if current_state == SystemState.MANUAL else None)

controller.set_button_release_action(ButtonType.UP, lambda: motor.stopMotor2() if current_state == SystemState.MANUAL else None)
controller.set_button_release_action(ButtonType.DOWN, lambda: motor.stopMotor2() if current_state == SystemState.MANUAL else None)

# Main loop
try:
    while True:
        controller.loop()
        eye_tracking.loop()
        motor.loop()
        light.loop()

        if current_state == SystemState.AUTO:
            if len(eye_tracking.move_direction) > 0:
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
            else:
                set_state(SystemState.IDLE)
        
        if eye_tracking.is_dark and light.camera_light is not True:
            light.cameraLight(True)
        elif eye_tracking.is_dark is not True and light.camera_light:
            light.cameraLight(False)

except Exception as e:
    print(e)
    motor.stopAllMotors()
finally:
    light.exit()
    motor.exit()
    controller.exit()
    eye_tracking.exit()
