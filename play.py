from sequence import *
from animation import play_wave, draw_wave
import simpleaudio as sa

if __name__ == '__main__':
    for (a1, a2) in ((sinus_sample(400, 1200000, RATE), sinus_sample(440, 1000000, RATE)),):
        if len(a1) < len(a2):
            diff = len(a2) - len(a1)
            print('a1 < a2: ' + str(diff))
            a1 = np.concatenate((a1, np.zeros(diff)))
        elif len(a2) < len(a1):
            diff = len(a1) - len(a2)
            print('a2 < a1: ' + str(diff))
            a2 = np.concatenate((a2, np.zeros(diff)))

        print('a1: {} a2: {}'.format(len(a1), len(a2)))

        a1 = a1.astype(np.int16)
        a2 = a2.astype(np.int16)
        audio = np.vstack((a1, a2))
        audio = audio.transpose()
        audio = audio.copy(order='C')

        #play_wave(audio)
        draw_wave(a1, a2)
        while True:
            play_obj = sa.play_buffer(audio, 2, 2, RATE)
            play_obj.wait_done()



