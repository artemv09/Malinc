import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 26  
button = 13
state = 0

GPIO.setup(led, GPIO.OUT)
GPIO.setup(state, GPIO.IN)  

while True:
    if GPIO.input(button):
        state = not state


    GPIO.output(led, state)