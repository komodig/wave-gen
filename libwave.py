import numpy as np
from plot import single_plot


POS_MAX = int(2 ** 15 - 1)
NEG_MAX = int(2 ** 15) * -1

RATE = 44100  # 44100 samples per second

def play_file():
    filename = 'myfile.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

def sinus_sample(freq, microseconds, rate, plot=False):
    x = np.linspace(0, 2*np.pi, int(rate/freq))
    wave = np.sin(x)
    wave = wave * POS_MAX
    if plot:
        single_plot(x, wave)
    audio = wave # 1st wave
    wave_duration = int(1 / freq * 1000000) # microseconds per wave
    assert microseconds > wave_duration
    for i in range(int(microseconds / wave_duration) - 1):  # -1st wave already added before
        audio = np.concatenate((audio, wave[1:]))  # skip 1st element in wave for clean zero point

    return audio

def triangular_sample(freq, microseconds, rate, plot=False):
    slope_rise = np.linspace(NEG_MAX, POS_MAX, int(rate/freq/2))
    slope_fall = np.linspace(POS_MAX, NEG_MAX, int(rate/freq/2))
    wave = np.concatenate((slope_rise, slope_fall))
    if plot:
        single_plot(range(int(rate/freq)), wave)
    audio = wave # start autio with something to concatenate on
    wave_duration = int(1 / freq * 1000000) # microseconds per wave

    # 1 second of noise would be x in range(freq)
    for x in range(int(microseconds / wave_duration) - 1):  # -1st wave already added before
        audio = np.concatenate((audio, wave))

    return audio

def square_sample(freq, microseconds, rate):
    # a single wave consists of 4 parts with half of it is silence
    first_half = np.full((int(rate/freq/4),), int(POS_MAX/4))   # use POS_MAX/2 because square is very dominant
    second_half = np.full((int(rate/freq/4),), int(NEG_MAX/4))  # use NEG_MAX/2 because square is very dominant
    wave = np.concatenate((first_half, second_half))
    wave = np.concatenate((wave, np.zeros(int(rate/freq/2))))
    audio = wave # start autio with something to concatenate on
    wave_duration = int(1 / freq * 1000000) # microseconds per wave
    # 1 second of noise would be x in range(freq)
    for x in range(int(microseconds / wave_duration) - 1):  # -1st wave already added before
        audio = np.concatenate((audio, wave))

    return audio

