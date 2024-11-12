import pygame
import Motor as motor
import time

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick connected.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick '{joystick.get_name()}' initialized.")

X_AXIS = 0
Y_AXIS = 1
BUTTON_A = 1
BUTTON_B = 2 
BUTTON_SELECT = 8
BUTTON_START = 9

try:
    while True:
        pygame.event.pump()
        x_axis = joystick.get_axis(X_AXIS)
        y_axis = joystick.get_axis(Y_AXIS)

        if joystick.get_axis(X_AXIS) < -0.5:
            print("LEFT pressed")
            motor.moveVMotor(True)
        elif joystick.get_axis(X_AXIS) > 0.5:
            print("RIGHT pressed")
            motor.moveVMotor(False)
        if joystick.get_axis(Y_AXIS) < -0.5:
            print("UP pressed")
            motor.moveHMotor(True)
        elif joystick.get_axis(Y_AXIS) > 0.5:
            print("DOWN pressed")
            motor.moveHMotor(False)
        if joystick.get_button(BUTTON_A):
            print("A pressed")
            #motor.moveVMotor(True)
        if joystick.get_button(BUTTON_B):
            print("B pressed")
            #motor.moveVMotor(False)
        if joystick.get_button(BUTTON_SELECT):
            print("SELECT pressed")
        if joystick.get_button(BUTTON_START):
            print("START pressed")
            #motor.moveVMotor(True)
        else:
            motor.stopMotor()

        time.sleep(0.1)  # Reduce CPU usage

except KeyboardInterrupt:
    print("Exiting program.")
finally:
    pygame.quit()
