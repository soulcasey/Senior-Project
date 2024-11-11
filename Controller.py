import pygame
import Motor as motor

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick connected.")
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick '{joystick.get_name()}' initialized.")

BUTTON_1 = 0
BUTTON_2 = 1 

while True:
    pygame.event.pump()
    
    if joystick.get_button(BUTTON_1):
        motor.moveVMotor(True)
    elif joystick.get_button(BUTTON_2):
        motor.moveVMotor(False)
    else:
        motor.stopMotor()
