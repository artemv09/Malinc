import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 26

GPIO.setup(led, GPIO.OUT)

state = 0
period = 0.3 

while True:
    GPIO.output(led, state)
    time.sleep(period / 2)  
    state = not state       
