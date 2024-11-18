from Controller import ButtonType, Controller

controller = Controller()


controller.set_button_press_action(ButtonType.LEFT, lambda: print("LEFT"))
controller.set_button_press_action(ButtonType.RIGHT, lambda: print("RIGHT"))

controller.set_button_press_action(ButtonType.UP, lambda: print("UP"))
controller.set_button_press_action(ButtonType.DOWN, lambda: print("DOWN"))

controller.set_button_press_action(ButtonType.A, lambda: print("A"))
controller.set_button_press_action(ButtonType.B, lambda: print("B"))

controller.set_button_press_action(ButtonType.SELECT, lambda: print("SELECT"))
controller.set_button_press_action(ButtonType.START, lambda: print("START"))


# Main loop
try:
    while True:
        controller.loop()

finally:
    controller.exit()
