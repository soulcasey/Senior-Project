import platform
import time
import threading
from enum import Enum
from typing import List

class MotorState(Enum):
    STOP = 1
    FORWARD = 2
    BACKWARD = 3

# Check if the code is running on a Raspberry Pi or Windows
is_raspberry_pi = platform.system() == "Linux" and "raspberrypi" in platform.node().lower()

if is_raspberry_pi:
    import RPi.GPIO as GPIO # type: ignore

    if GPIO.getmode() != GPIO.BOARD:
        GPIO.setmode(GPIO.BOARD)

motorCount = 0
speed = 100

class Motor:
    def __init__(self, pwm_pin, dir_pin1, dir_pin2, multiplier):
        self.pwm_pin = pwm_pin
        self.dir_pin1 = dir_pin1
        self.dir_pin2 = dir_pin2

        self.multiplier = multiplier  # Degrees per second
        self.angle = 0
        self.motor_state: MotorState = MotorState.STOP
        self.last_time = time.time()

        if is_raspberry_pi:
            GPIO.setup(self.pwm_pin, GPIO.OUT)
            GPIO.setup(self.dir_pin1, GPIO.OUT)
            GPIO.setup(self.dir_pin2, GPIO.OUT)
            self.motor = GPIO.PWM(self.pwm_pin, 1000)
            self.motor.start(0)

        global motorCount
        motorCount += 1
        print("Motor " + str(motorCount) + " setup complete")

    def move(self, forward: bool):
        motor_state = MotorState.FORWARD if forward else MotorState.BACKWARD
        if self.motor_state == motor_state:
            return

        self.motor_state = motor_state
        self.last_time = time.time()

        if is_raspberry_pi:
            GPIO.output(self.dir_pin1, forward)
            GPIO.output(self.dir_pin2, not forward)
            self.motor.ChangeDutyCycle(speed)

    def stop(self):
        if self.motor_state == MotorState.STOP:
            return

        self.motor_state = MotorState.STOP
        self.last_time = time.time()

        if is_raspberry_pi:
            GPIO.output(self.dir_pin1, False)
            GPIO.output(self.dir_pin2, False)
            self.motor.ChangeDutyCycle(0)


motor1 = Motor(11, 13, 15, 90 / 1.5) # Motor 1
motor2 = Motor(22, 16, 18, 45) # Motor 2
motors: List[Motor] = [motor1, motor2]

def loop():
    for motor in motors:
        if motor.motor_state == MotorState.STOP:
            continue

        current_time = time.time()

        adjusted_angle = (current_time - motor.last_time) * motor.multiplier

        if motor.motor_state == MotorState.FORWARD:
            motor.angle += adjusted_angle
        else:
            motor.angle -= adjusted_angle

        motor.last_time = current_time

        print(motor.angle)

def moveMotor1(forward: bool):
    print("Motor 1 Forward") if forward else print("Motor 1 Backward")
    motors[0].move(forward)

def stopMotor1():
    print("Motor 1 Stop")
    motors[0].stop()

def moveMotor2(forward: bool):
    print("Motor 2 Forward") if forward else print("Motor 2 Backward")
    motors[1].move(forward)

def stopMotor2():
    print("Motor 2 Stop")
    motors[1].stop()

def stopAllMotors():
    for motor in motors:
        motor.stop()

def exit():
    if is_raspberry_pi:
        GPIO.cleanup()
    print("Exiting program. Cleaned up resources if applicable.")
