from Controller import ButtonType, Controller
import Light as light

controller = Controller()

controller.set_button_press_action(ButtonType.A, lambda: light.cameraLight(True))
controller.set_button_press_action(ButtonType.B, lambda: light.warningLight(True))

# Set button release actions to stop motors
controller.set_button_release_action(ButtonType.A, lambda: light.cameraLight(False))
controller.set_button_release_action(ButtonType.B, lambda: light.warningLight(False))

# Set button release actions to stop motors
controller.set_button_release_action(ButtonType.START, lambda: light.startBlink())
controller.set_button_release_action(ButtonType.SELECT, lambda: light.stopBlink())

print("Testing light!")

# Main loop
try:
    while True:
        controller.loop()
        light.loop()

finally:
    controller.exit()
