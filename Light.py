import RPi.GPIO as GPIO

camera_light = 35
warning_light = 37

if (GPIO.getmode() != GPIO.BOARD):
    GPIO.setmode(GPIO.BOARD)

GPIO.setup(camera_light ,GPIO.OUT)
GPIO.setup(warning_light ,GPIO.OUT)

def cameraLight(isOn: bool):
    GPIO.output(camera_light, isOn)

def warningLight(isOn: bool):
    GPIO.output(warning_light, isOn)
