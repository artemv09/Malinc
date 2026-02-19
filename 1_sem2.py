import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = [16, 20, 21, 25, 26, 17, 27, 22]

dynamic_range = 3.3



GPIO.setup(led, GPIO.OUT)


def voltage_to_number(voltage):

    global dynamic_range
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавлниваем 0.0 В")
        return 0

    return int(voltage / dynamic_range * 255)



def number_to_dac(number):
    a = [int(i) for i in bin(number)[2:].zfill(8)]
    print(a)
    for i in range(len(a)):
        GPIO.output(led[i], a[i])



try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)

        except ValueError:
            print("Вы ввели не число. Попробуйте ещё раз\n")

finally:
    GPIO.output(led, 0)
    GPIO.cleanup()

