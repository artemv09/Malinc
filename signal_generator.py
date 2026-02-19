import numpy
import time 
import math

def get_sin_wave_amplitude(freq, time):
    artg = 2 * math.pi * freq * time

    return (math.sin(artg) + 1) / 2



def wait_for_sampling_period(sampling_frequency):
    time_slep = 1 / sampling_frequency
    time.sleep(time_slep)

