import simpleaudio as sa
import numpy as np


POS_MAX = int(2 ** 15 - 1)
NEG_MAX = int(2 ** 15) * -1

rate = 44100  # 44100 samples per second

def play_file():
    filename = 'myfile.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

def sinus_sample(freq, microseconds, rate):
    x = np.linspace(0, 2*np.pi, int(rate/freq))
    wave = np.sin(x)
    wave = wave * POS_MAX
    audio = wave # 1st wave
    wave_duration = int(1 / freq * 1000000) # microseconds per wave
    assert microseconds > wave_duration
    for x in range(int(microseconds / wave_duration) - 1):  # -1st wave already added before
        audio = np.concatenate((audio, wave))

    return audio

def triangular_sample(freq, microseconds, rate):
    slope_rise = np.linspace(NEG_MAX, POS_MAX, int(rate/freq/2))
    slope_fall = np.linspace(POS_MAX, NEG_MAX, int(rate/freq/2))
    wave = np.concatenate((slope_rise, slope_fall))
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

def triangular_square():
    x = 60
    silence100ms = np.zeros(int(rate / 1000))
    a1 = silence100ms
    a2 = silence100ms

    for bass in (x, 2.5*x, 1.5*x):
        for freq in (4*x, 2*x, 3*x, 4*x, 2*x, 3*x, ):
            a1 = np.concatenate((a1, triangular_sample(freq, 120000, rate)))
            a2 = np.concatenate((a2, square_sample(bass, 120000, rate)))

    return a1, a2

def legacy_square_bass():
    x = 40
    nothing = np.zeros(1)
    a1 = nothing
    a2 = nothing

    for bass in np.linspace(100, 40, 20):
        a1 = np.concatenate((a1, square_sample(bass, 40000, rate)))
        a2 = np.concatenate((a2, square_sample(bass, 40000, rate)))

    silence = np.zeros(int(rate/4))
    for i in range(8):
        a1 = np.concatenate((a1, square_sample(x, 300000, rate)))
        a1 = np.concatenate((a1, silence))
        a2 = np.concatenate((a2, square_sample(x, 300000, rate)))
        a2 = np.concatenate((a2, silence))

    return a1, a2

def awesome_bomb(duration):
    almost_nothing = np.zeros(1)
    a1 = almost_nothing
    a2 = almost_nothing

    while len(a1) < duration:
        for bass in np.linspace(100, 40, 10):
            freq = 2*bass
            a1 = np.concatenate((a1, sinus_sample(freq, duration, rate)))
            a2 = np.concatenate((a2, sinus_sample(bass, duration, rate)))

    return a1, a2

def sinus_figure_1():
    x = 60
    almost_nothing = np.zeros(1)
    a1 = almost_nothing
    a2 = almost_nothing

    for bass in np.linspace(100, 40, 10):
        freq = 2*bass
        a1 = np.concatenate((a1, sinus_sample(freq, 40000, rate)))
        a2 = np.concatenate((a2, sinus_sample(bass, 40000, rate)))

    for bass in (x, 2.5*x, 1.5*x):
        for freq in (2*x, 1*x, 1.5*x, 2*x, 1*x, 1.5*x):
            a1 = np.concatenate((a1, sinus_sample(freq, 120000, rate)))
            a2 = np.concatenate((a2, sinus_sample(bass, 120000, rate)))

    return a1, a2

def sinus_figure_2():
    x = 60
    almost_nothing = np.zeros(1)
    a1 = almost_nothing
    a2 = almost_nothing

    for bass in (2.5*x, 3*x, 2.5*x):
        for freq in (4*x, 2*x, 3*x, 4*x, 2*x, 3*x):
            a1 = np.concatenate((a1, sinus_sample(freq, 120000, rate)))
            a2 = np.concatenate((a2, sinus_sample(bass, 120000, rate)))

    return a1, a2

def triangular_sequence_1():
    x = 60
    nothing = np.zeros(1)
    a1 = nothing
    a2 = nothing

    for bass in (1.5*x,):
        for freq in (6*x, 5*x, 4*x, 3*x, 4*x, 5*x, 6*x):
            a1 = np.concatenate((a1, triangular_sample(freq, 120000, rate)))
            a2 = np.concatenate((a2, triangular_sample(bass, 120000, rate)))

    return a1, a2

def sinus_sequence_1():
    a1a, a2a = sinus_figure_1()
    a1b, a2b = sinus_figure_2()
    a1 = np.concatenate((a1a, a1b))
    a2 = np.concatenate((a2a, a2b))
    a1c, a2c = triangular_sequence_1()
    a1 = np.concatenate((a1, a1c))
    a2 = np.concatenate((a2, a2c))

    return a1, a2

if __name__ == '__main__':
    #b1 = a1; b2 = a2
    a1, a2 = sinus_sequence_1()
    print(len(a1))
    b1, b2 = awesome_bomb(len(a1))
    #a1, a2 = triangular_square()

    a1 = np.concatenate((a1, a1))
    if len(a1) < len(a2):
        diff = len(a2) - len(a1)
        print(diff)
        a1 = np.concatenate((a1, np.zeros(diff)))
    elif len(a2) < len(a1):
        diff = len(a1) - len(a2)
        print(diff)
        a2 = np.concatenate((a2, np.zeros(diff)))

    if len(b1) < len(a1):
        diff = len(a1) - len(b1)
        print(diff)
        b1 = np.concatenate((np.zeros(diff), b1))
    if len(b2) < len(a2):
        diff = len(a2) - len(b2)
        print(diff)
        b2 = np.concatenate((np.zeros(diff), b2))
    a1 = np.concatenate((a1, (a1 + b1)))
    a2 = np.concatenate((a2, (a2 + b2)))
    print('a1: {} a2: {} b1: {} b2: {}'.format(len(a1), len(a2), len(b1), len(b2)))

    a1 = a1.astype(np.int16)
    a2 = a2.astype(np.int16)
    audio = np.vstack((a1, a2))
    audio = audio.transpose()
    audio = audio.copy(order='C')
    play_obj = sa.play_buffer(audio, 2, 2, rate)
    play_obj.wait_done()



