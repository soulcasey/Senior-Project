import pygame
from enum import Enum

# Constants for joystick button and axis mappings
X_AXIS = 0
Y_AXIS = 4
BUTTON_A = 1
BUTTON_B = 2 
BUTTON_SELECT = 8
BUTTON_START = 9

class Button(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP = "UP"
    DOWN = "DOWN"
    A = "A"
    B = "B"
    SELECT = "SELECT"
    START = "START"

class Controller:
    def __init__(self):
        # Button states and actions combined (Inside Main class)
        self.button_info = {button: {"state": False, "press": None, "release": None} for button in Button}
        
        self.joystick = None

        # Initialize pygame and joystick
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("No joystick connected.")
        else:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            print(f"Joystick '{self.joystick.get_name()}' initialized.")

    # Update the button state and execute actions for press and release
    def update_button_state(self, button, is_pressed):
        current_state = self.button_info[button]["state"]
        if is_pressed and not current_state:
            self.button_info[button]["state"] = True
            if self.button_info[button]["press"]:
                self.button_info[button]["press"]()
        elif not is_pressed and current_state:
            self.button_info[button]["state"] = False
            if self.button_info[button]["release"]:
                self.button_info[button]["release"]()

    # Set custom actions for button press and release
    def set_button_press_action(self, button, action):
        if button in self.button_info:
            self.button_info[button]["press"] = action

    def set_button_release_action(self, button, action):
        if button in self.button_info:
            self.button_info[button]["release"] = action

    # Handle joystick input in the loop
    def loop(self):
        pygame.event.pump()

        # Process joystick input and button state changes for every button
        self.update_button_state(Button.LEFT, self.joystick.get_axis(X_AXIS) < -0.5)
        self.update_button_state(Button.RIGHT, self.joystick.get_axis(X_AXIS) > 0.5)
        self.update_button_state(Button.UP, self.joystick.get_axis(Y_AXIS) < -0.5)
        self.update_button_state(Button.DOWN, self.joystick.get_axis(Y_AXIS) > 0.5)
        self.update_button_state(Button.A, self.joystick.get_button(BUTTON_A))
        self.update_button_state(Button.B, self.joystick.get_button(BUTTON_B))
        self.update_button_state(Button.SELECT, self.joystick.get_button(BUTTON_SELECT))
        self.update_button_state(Button.START, self.joystick.get_button(BUTTON_START))

    # Cleanup and quit pygame
    def exit(self):
        pygame.quit()