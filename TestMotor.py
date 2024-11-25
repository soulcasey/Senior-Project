from Controller import ButtonType, Controller
import Motor as motor

# Function to toggle auto_mode on or off when START or SELECT is pressed
def toggle_auto_mode():
    global auto_mode
    auto_mode = not auto_mode
    motor.stopMotor1()
    motor.stopMotor2()
    print(f"AUTO_MODE is now {'ON' if auto_mode else 'OFF'}")

# Initialize the auto mode to be off by default
auto_mode = False

controller = Controller()

# Set button press actions for motor control with auto_mode checks
controller.set_button_press_action(ButtonType.LEFT, lambda: motor.moveMotor1(True) if not auto_mode else None)
controller.set_button_press_action(ButtonType.RIGHT, lambda: motor.moveMotor1(False) if not auto_mode else None)

controller.set_button_press_action(ButtonType.UP, lambda: motor.moveMotor2(True) if not auto_mode else None)
controller.set_button_press_action(ButtonType.DOWN, lambda: motor.moveMotor2(False) if not auto_mode else None)

# Set button press actions for toggling auto mode
controller.set_button_press_action(ButtonType.SELECT, toggle_auto_mode)

# Set button release actions to stop motors
controller.set_button_release_action(ButtonType.LEFT, lambda: motor.stopMotor1() if not auto_mode else None)
controller.set_button_release_action(ButtonType.RIGHT, lambda: motor.stopMotor1() if not auto_mode else None)

controller.set_button_release_action(ButtonType.UP, lambda: motor.stopMotor2() if not auto_mode else None)
controller.set_button_release_action(ButtonType.DOWN, lambda: motor.stopMotor2() if not auto_mode else None)

# Main loop
try:
    while True:
        controller.loop()

except Exception as e:
    motor.stopAllMotors()

finally:
    controller.exit()
    motor.exit()
