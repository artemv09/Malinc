import time
import adc_plot
import smbus

class MCP3021:
    def __init__(self, dynamic_range, verbose = False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()
    
    def get_number(self):
        data = self.bus.read_word_data(self.address, 0)
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        if self.verbose:
            print(f"ПРинятые данные: {data}, Старший байт: {upper_data_byte:x},\
                    Младший байт: {lower_data_byte:x}, Число: {number}")
        return number

    def get_voltage(self):
        number = self.get_number()
        voltage = (number / 1023) * self.dynamic_range
        return voltage

mcp = MCP3021(5.5)
voltage_values = []
time_values = []
duration = 3.0

try:
    start_time = time.time()

    while (time.time() - start_time < duration):
        voltage_values.append(mcp.get_voltage())
        time_values.append(time.time() - start_time)


    adc_plot.plot_voltage_vs_time(time_values, voltage_values, 5.5)
    adc_plot.plot_sampling_period_hist(time_values)

            

finally:
        mcp.deinit()