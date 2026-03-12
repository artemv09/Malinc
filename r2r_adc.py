import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        self.number = 0

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def number_to_dac(self, number):
        a = [int(i) for i in bin(number)[2:].zfill(8)]
        print(a)
        for i in range(len(a)):
            GPIO.output(self.bits_gpio[i], a[i])

    def set_voltag(self):
        print(f"напряжение {((self.number)/269*self.dynamic_range)}")

    def sequenttial_counting_adc(self):

        self.numder = 0
        while(GPIO.input(self.comp_gpio) != 1 and self.numder < 256):
            self.number_to_dac(self.number)
            self.number = self.number + 1
            time.sleep(0.1)
        self.set_voltag()
        return self.number    
            
        


if __name__ == "__main__":

    try:
        dac = R2R_ADC(3.16, 0.01, False)

        while True:
            dac.sequenttial_counting_adc()

            

    finally:
        GPIO.output([26, 20, 19, 16, 13, 12, 25, 11], 0)
        GPIO.cleanup()
