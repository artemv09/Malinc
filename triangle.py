import RPi.GPIO as GPIO
import numpy
import time
import math

global_var = 10

def get_sin_wave_amplitude(freq, time):
    global global_var
    x = 1 / freq
    y = x / 2

    z = int(time / y)

    if(z % 2 == 0):
        return (time - z * y) / y

    else:
        w = y * (z + 1) - time

        return w / y




def wait_for_sampling_period(sampling_frequency):
    time_slep = 1 / sampling_frequency
    time.sleep(time_slep)

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)

    def deinit(self):
        GPIO.putput(self.gpio_bits, 0)
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()

    def set_number(self, number):
        a = [int(i) for i in bin(number)[2:].zfill(8)]
        print(a)
        for i in range(len(a)):
            GPIO.output(self.gpio_bits[i], a[i])

    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            return 0
        number = int(voltage / self.dynamic_range * 255)
        self.set_number(number) 

amplitude = 3.2
signal_frequency = 10
sampling_frequency = 1000

try:
    dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
    start_time = time.time()
    while True:
        current_time = time.time() - start_time
        signal = amplitude*get_sin_wave_amplitude(signal_frequency, current_time)
        dac.set_voltage(signal)
        wait_for_sampling_period(sampling_frequency)
finally:
    dac.deinit()