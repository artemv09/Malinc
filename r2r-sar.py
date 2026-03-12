import RPi.GPIO as GPIO
import time
import adc_plot 

class R2R_ADC:

    def __init__(self, dynamic_range, compare_time = 0.0001, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        a = [int(i) for i in bin(number)[2:].zfill(8)]
        for i in range(len(a)):
            GPIO.output(self.bits_gpio[i], a[i])

    def sequential_counting_adc(self):
        self.left = 1
        self.right = 255
        self.copy = 0

        self.flag = False
        while(self.right - self.left > 1):
            self.copy = (self.left + self.right) // 2
            self.number_to_dac(self.copy)
            time.sleep(0.0001)
            comparator_output = GPIO.input(self.comp_gpio)


            if comparator_output == 0:
                self.left = self.copy
        

            else :
                self.right = self.copy


        return self.copy

    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        voltage = (digital_value / 255) * self.dynamic_range
        return voltage
 


if __name__ == "__main__":

    dac = R2R_ADC(3.16, 0.0001, False)
    voltage_values = []
    time_values = []
    duration = 3.0

    try:

        start_time = time.time()

        while (time.time() - start_time < duration):
            voltage_values.append(dac.get_sc_voltage())
            time_values.append(time.time() - start_time)


        adc_plot.plot_voltage_vs_time(time_values, voltage_values, 3.3)
        adc_plot.plot_sampling_period_hist(time_values)

            

    finally:
        GPIO.output([26, 20, 19, 16, 13, 12, 25, 11], 0)
        GPIO.cleanup()
