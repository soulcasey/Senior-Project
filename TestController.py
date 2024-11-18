from Controller import ButtonType, Controller

def toggle_auto_mode():
    global auto_mode
    auto_mode = not auto_mode
    print(f"AUTO_MODE is now {'ON' if auto_mode else 'OFF'}")

auto_mode = False

controller = Controller()


controller.set_button_press_action(ButtonType.LEFT, lambda: print("LEFT") if not auto_mode else None)
controller.set_button_press_action(ButtonType.RIGHT, lambda: print("RIGHT") if not auto_mode else None)

controller.set_button_press_action(ButtonType.UP, lambda: print("UP") if not auto_mode else None)
controller.set_button_press_action(ButtonType.DOWN, lambda: print("DOWN") if not auto_mode else None)

controller.set_button_press_action(ButtonType.A, lambda: print("A") if not auto_mode else None)
controller.set_button_press_action(ButtonType.B, lambda: print("B") if not auto_mode else None)

controller.set_button_press_action(ButtonType.SELECT, toggle_auto_mode)
controller.set_button_press_action(ButtonType.START, lambda: print("START") if not auto_mode else None)

toggle_auto_mode()

# Main loop
try:
    while True:
        controller.loop()

finally:
    controller.exit()
