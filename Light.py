import platform
import time

# Define GPIO pins for the lights
camera_light = 35
warning_light = 37

is_camera_light_on = False
is_warning_light_on = False

# Variable to track the last time the warning light was toggled
last_toggle_time = 0
blink_interval = 0.5  # 500 ms interval for blinking

# Flag to control blinking state
is_blinking = False

# Check if the code is running on a Raspberry Pi or Windows
is_raspberry_pi = platform.system() == "Linux" and "raspberrypi" in platform.node().lower()

if is_raspberry_pi:
    import RPi.GPIO as GPIO

    # Initialize GPIO in BOARD mode
    if GPIO.getmode() != GPIO.BOARD:
        GPIO.setmode(GPIO.BOARD)

    # Setup GPIO pins as output
    GPIO.setup(camera_light, GPIO.OUT)
    GPIO.setup(warning_light, GPIO.OUT)

    GPIO.output(camera_light, False)
    GPIO.output(warning_light, False)

# Control functions for individual lights
def cameraLight(isOn: bool):
    global is_camera_light_on

    if is_camera_light_on == isOn:
        return

    is_camera_light_on = isOn

    if is_raspberry_pi:
        GPIO.output(camera_light, isOn)

def warningLight(isOn: bool):
    global is_warning_light_on

    if is_warning_light_on == isOn:
        return
    
    is_warning_light_on = isOn

    if is_raspberry_pi:
        GPIO.output(warning_light, isOn)

# Blinking function for the warning light
def blinkWarningLight():
    global last_toggle_time

    current_time = time.time()
    if current_time - last_toggle_time >= blink_interval:
        # Toggle the warning light
        if is_warning_light_on:
            warningLight(False)
        else:
            warningLight(True)

        # Update the last toggle time
        last_toggle_time = current_time

# Start blinking the warning light
def startBlink():
    global is_blinking
    if not is_blinking:
        is_blinking = True

# Stop blinking the warning light
def stopBlink():
    global is_blinking
    if is_blinking:
        is_blinking = False

    warningLight(False)  # Ensure the light is turned off when stopping the blink

# Main loop that checks the blinking state and controls the light
def loop():
    if is_blinking:
        blinkWarningLight()

def exit():
    # Turn off the lights when exiting
    cameraLight(False)
    warningLight(False)
