import RPi.GPIO as GPIO

camera_light = 29
warning_light = 37

if (GPIO.getmode() != GPIO.BOARD):
    GPIO.setmode(GPIO.BOARD)

GPIO.setup(camera_light ,GPIO.OUT)
GPIO.setup(warning_light ,GPIO.OUT)

def cameraLight(isOn: bool):
    if (isOn == True):
        print("Camera Light On")
        GPIO.setup(camera_light, GPIO.HIGH)
    else:
        print("Camera Light Off")
        GPIO.setup(camera_light, GPIO.LOW)

def warningLight(isOn: bool):
    if (isOn == True):
        print("Warning Light On")
        GPIO.setup(warning_light, GPIO.HIGH)
    else:
        print("Warning Light Off")
        GPIO.setup(warning_light, GPIO.LOW)