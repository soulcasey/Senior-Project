import pygame
from enum import Enum

# Constants for joystick button and axis mappings
X_AXIS = 0
Y_AXIS = 1
BUTTON_A = 1
BUTTON_B = 2
BUTTON_SELECT = 8
BUTTON_START = 9

class ButtonType(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"
    A = "A"
    B = "B"
    SELECT = "SELECT"
    START = "START"

class Button:
    def __init__(self, button_type):
        self.button_type = button_type
        self.pressed = False
        self.press_action = None
        self.release_action = None

    def set_press_action(self, action):
        self.press_action = action

    def set_release_action(self, action):
        self.release_action = action

    def update_state(self, is_pressed):
        if is_pressed and not self.pressed:
            self.pressed = True
            if self.press_action:
                self.press_action()
        elif not is_pressed and self.pressed:
            self.pressed = False
            if self.release_action:
                self.release_action()

class Controller:
    def __init__(self):
        # Initialize button states for each button type
        self.button_states = {button_type: Button(button_type) for button_type in ButtonType}
        
        # Initialize pygame and joystick
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("No joystick connected.")
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick '{self.joystick.get_name()}' initialized.")

    def is_button_pressed(self, button_type):
        if button_type in self.button_states:
            return self.button_states[button_type].pressed
        return False

    # Set custom actions for button press and release
    def set_button_press_action(self, button_type, action):
        if button_type in self.button_states:
            self.button_states[button_type].press_action = action

    def set_button_release_action(self, button_type, action):
        if button_type in self.button_states:
            self.button_states[button_type].release_action = action

    def loop(self):
        pygame.event.pump()

        # Update button states based on joystick input
        self.button_states[ButtonType.LEFT].update_state(self.joystick.get_axis(X_AXIS) < -0.5)
        self.button_states[ButtonType.RIGHT].update_state(self.joystick.get_axis(X_AXIS) > 0.5)
        self.button_states[ButtonType.UP].update_state(self.joystick.get_axis(Y_AXIS) < -0.5)
        self.button_states[ButtonType.DOWN].update_state(self.joystick.get_axis(Y_AXIS) > 0.5)
        self.button_states[ButtonType.A].update_state(self.joystick.get_button(BUTTON_A))
        self.button_states[ButtonType.B].update_state(self.joystick.get_button(BUTTON_B))
        self.button_states[ButtonType.SELECT].update_state(self.joystick.get_button(BUTTON_SELECT))
        self.button_states[ButtonType.START].update_state(self.joystick.get_button(BUTTON_START))

    # Cleanup and quit pygame
    def exit(self):
        pygame.quit()
