import numpy as np
from libwave import sinus_sample, square_sample, triangular_sample, RATE
from plot import dual_plot


def legacy_square_bass():
    x = 40
    nothing = np.zeros(1)
    a1 = nothing
    a2 = nothing

    for bass in np.linspace(100, 40, 20):
        a1 = np.concatenate((a1, square_sample(bass, 40000, RATE)))
        a2 = np.concatenate((a2, square_sample(bass, 40000, RATE)))

    silence = np.zeros(int(RATE/4))
    for i in range(8):
        a1 = np.concatenate((a1, square_sample(x, 300000, RATE)))
        a1 = np.concatenate((a1, silence))
        a2 = np.concatenate((a2, square_sample(x, 300000, RATE)))
        a2 = np.concatenate((a2, silence))

    return a1, a2

def awesome_bass(duration=30000):
    almost_nothing = np.zeros(1)
    a1 = almost_nothing
    a2 = almost_nothing

    while len(a1) < duration:
        for bass in np.linspace(100, 40, 10):
            freq = 2*bass
            a1 = np.concatenate((a1, sinus_sample(freq, duration, RATE)))
            a2 = np.concatenate((a2, sinus_sample(bass, duration, RATE)))

    return a1, a2

def legacy_sinus_figure_1():
    x = 60
    almost_nothing = np.zeros(1)
    a1 = almost_nothing
    a2 = almost_nothing

    chan1 = list(np.concatenate((np.linspace(60, 150, 30), np.linspace(150, 120, 20))))
    chan2 = list(np.concatenate((np.linspace(50, 150, 30), np.linspace(150, 120, 20))))
    chan1 += reversed(chan1)
    chan2 += reversed(chan2)

    for freq in chan1:
        a1 = np.concatenate((a1, sinus_sample(freq, 220000, RATE)))

    for freq in chan2:
        a2 = np.concatenate((a2, sinus_sample(freq, 220000, RATE)))

    return a1, a2

def legacy_sinus_figure_2():
    x = 60
    almost_nothing = np.zeros(1)
    a1 = almost_nothing
    a2 = almost_nothing

    for bass in (2.5*x, 3*x, 2.5*x):
        for freq in (3*x, 2*x, 3*x, 1*x, 2*x, 3*x):
            a1 = np.concatenate((a1, sinus_sample(freq, 120000, RATE)))
            a2 = np.concatenate((a2, sinus_sample(bass, 120000, RATE)))

    return a1, a2

def triangular_sequence_1(duration=120000):
    x = 60
    nothing = np.zeros(1)
    a1 = nothing
    a2 = nothing

    for bass in (1.5*x,):
        for freq in (6*x, 5*x, 4*x, 3*x, 4*x, 5*x, 6*x, 5*x, 4*x, 7*x, 6*x, 5*x):
            a1 = np.concatenate((a1, triangular_sample(freq, duration, RATE)))
            a2 = np.concatenate((a2, triangular_sample(bass, duration, RATE)))

    return a1, a2

def sinus_sequence_1():
    b1 = b2 = np.zeros(1)
    x = 50
    for var in (x*1, x*2, x*3, x*4, x*2, x*5, x*2):
        for amp in list(range(1,5)) + list(reversed(range(1,5))):
            a1 = sinus_sample(100 + var, 300000, RATE)
            a2 = sinus_sample(100, 300000, RATE)
            a2 /= amp

            x2 = sinus_sample(400, 400000, RATE)
            x2 = x2[:len(a2)]
            x2 /= 10
            a2 = a2 + x2
            a2 *= 0.7

            b1 = np.concatenate((b1, a1))
            b2 = np.concatenate((b2, a2))

    dual_plot(range(1000), a1[:1000], a2[:1000])

    return b1, b2

def sinus_sequence_2():
    b1 = b2 = np.zeros(1)
    x = 50
    for var in (x*1, x*2, x*3, x*4, x*2, x*5, x*2):
        for rav in (x*2, x*3, x*1, x*5, x*4, x*3, x*2):
            a1 = sinus_sample(100 + var, 300000, RATE)

            x1 = sinus_sample(300, 600000, RATE)
            x1 = x1[:len(a1)]
            x1 /= 10
            a1 += x1
            a1 *= 0.7

            a2 = sinus_sample(200 + rav, 300000, RATE)

            x2 = sinus_sample(400, 400000, RATE)
            x2 = x2[:len(a2)]
            x2 /= 10
            a2 += x2
            a2 *= 0.7

            b1 = np.concatenate((b1, a1))
            b2 = np.concatenate((b2, a2))

    dual_plot(range(1000), a1[:1000], a2[:1000])

    return b1, b2
