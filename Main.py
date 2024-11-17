from Controller import Button, Controller
from EyeTracking import EyeTracking
import time

# Function to print button press based on auto_mode
def on_button_press(button):
    if not auto_mode:
        print(f"Pressed {button.value}")

# Function to print button release based on auto_mode
def on_button_release(button):
    if not auto_mode:
        print(f"Released {button.value}")

# Function to toggle auto_mode on or off when START or SELECT is pressed
def toggle_auto_mode():
    global auto_mode
    auto_mode = not auto_mode
    print(f"AUTO_MODE is now {'ON' if auto_mode else 'OFF'}")

auto_mode = False

eye_tracking = EyeTracking()
controller = Controller()

# Set button actions
controller.set_button_press_action(Button.LEFT, lambda: on_button_press(Button.LEFT))
controller.set_button_press_action(Button.RIGHT, lambda: on_button_press(Button.RIGHT))
controller.set_button_press_action(Button.UP, lambda: on_button_press(Button.UP))
controller.set_button_press_action(Button.DOWN, lambda: on_button_press(Button.DOWN))
controller.set_button_press_action(Button.A, lambda: on_button_press(Button.A))
controller.set_button_press_action(Button.B, lambda: on_button_press(Button.B))
controller.set_button_press_action(Button.SELECT, lambda: toggle_auto_mode())
controller.set_button_press_action(Button.START, lambda: on_button_press(Button.START))

# Set button release actions, print only if auto_mode is off
controller.set_button_release_action(Button.LEFT, lambda: on_button_release(Button.LEFT))
controller.set_button_release_action(Button.RIGHT, lambda: on_button_release(Button.RIGHT))
controller.set_button_release_action(Button.UP, lambda: on_button_release(Button.UP))
controller.set_button_release_action(Button.DOWN, lambda: on_button_release(Button.DOWN))
controller.set_button_release_action(Button.A, lambda: on_button_release(Button.A))
controller.set_button_release_action(Button.B, lambda: on_button_release(Button.B))
controller.set_button_release_action(Button.SELECT, lambda: on_button_release(Button.SELECT))
controller.set_button_release_action(Button.START, lambda: on_button_release(Button.START))

while (True):
    controller.loop()
    eye_tracking.loop()

    if 0xFF == ord('q'):
        break

controller.exit()
