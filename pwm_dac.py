import RPi.GPIO as GPIO

led = [16, 20, 21, 25, 26, 17, 27, 22]

def number_to_dac(number):
    a = [int(i) for i in bin(number)[2:].zfill(8)]
    print(a)
    for i in range(len(a)):
        GPIO.output(led[i], a[i])



class PWM_DAC:
    def __init__(self, gpio_pin, pwm_frequency, dynamic_range, verbose = False):

        self.gpio_pin = gpio_pin
        self.freq = pwm_frequency
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT, initial = 0)

        self.pwm = GPIO.PWM(self.gpio_pin, self.freq) 
        self.pwm.start(0) 
       
    def deinit(self):

        self.pwm.stop()

        GPIO.output(self.gpio_pin, 0)

        GPIO.cleanup()


    def set_voltage(self, voltage):

        if (0.0 <= voltage <= self.dynamic_range):
            duty_cycle = (voltage / self.dynamic_range * 100)



        else:
            print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {self.dynamic_range:.2f} В)")
            print("Устанавливаем 0.0 В")
            duty_cycle = 0
            return 0

        number = int(voltage / self.dynamic_range * 255)
        number_to_dac(number)

        self.pwm.ChangeDutyCycle(duty_cycle)
        print(f"Коэффициент заполнения {duty_cycle:.2f} B")



if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.3, True) 
       
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")

    finally:
        dac.deinit()