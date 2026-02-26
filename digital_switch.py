import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)с

led = 26

GPIO.setup(led, GPIO.OUT)
GPIO.output(led, 0)  

button = 13 
GPIO.setup(button, GPIO.IN)

state = False 

while True:
    if GPIO.input(button):
        state = not state
        GPIO.output(led, state)
        time.sleep(0.2)