import simpleaudio as sa
import numpy as np
from libwave import *

if __name__ == '__main__':
    duration = 31075
    a1 = a2 = np.zeros(1)
    x = 50

    b1, b2 = awesome_bomb(duration)
    for freq in (6 * x, 5 * x, 4 * x, 3 * x, 4 * x, 5 * x):
        a1 = np.concatenate((a1, triangular_sample(freq, duration*4, rate)))
    for freq in (6 * x, 5 * x, 4 * x, 3 * x, 4 * x, 5 * x):
        a1 = np.concatenate((a1, triangular_sample(freq*2, duration*4, rate)))
    print('initial len %d' % len(a1))
    if len(a1) < len(a2):
        diff = len(a2) - len(a1)
        print(diff)
        a1 = np.concatenate((a1, np.zeros(diff)))
    elif len(a2) < len(a1):
        diff = len(a1) - len(a2)
        print(diff)
        a2 = np.concatenate((a2, np.zeros(diff)))

    try:
        if len(b1) < len(a1):
            diff = len(a1) - len(b1)
            print(diff)
            b1 = np.concatenate((np.zeros(diff), b1))
        if len(b2) < len(a2):
            diff = len(a2) - len(b2)
            print(diff)
            b2 = np.concatenate((np.zeros(diff), b2))

        a1 = np.concatenate((a1, b1))
        a2 = np.concatenate((a2, b2))
        print('a1: {} a2: {} b1: {} b2: {}'.format(len(a1), len(a2), len(b1), len(b2)))
    except NameError:
        print('a1: {} a2: {}'.format(len(a1), len(a2)))
        pass


    a1 = a1.astype(np.int16)
    a2 = a2.astype(np.int16)
    audio = np.vstack((a1, a2))
    audio = audio.transpose()
    audio = audio.copy(order='C')
    play_obj = sa.play_buffer(audio, 2, 2, rate)
    play_obj.wait_done()



