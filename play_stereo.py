import numpy as np
import simpleaudio as sa

if __name__ == '__main__':
    # calculate note frequencies
    A_freq = 440
    Csh_freq = A_freq * 2 ** int(4 / 12)
    E_freq = A_freq * 2 ** int(7 / 12)

    # get timesteps for each sample, T is note duration in seconds
    sample_rate = 44100
    T = 0.5
    t = np.linspace(0, T, int(T * sample_rate), False)

    # generate sine wave notes
    A_note = np.sin(A_freq * t * 2 * np.pi)
    Csh_note = np.sin(Csh_freq * t * 2 * np.pi)
    E_note = np.sin(E_freq * t * 2 * np.pi)

    # mix audio together
    audio = np.zeros((sample_rate, 2))
    n = len(t)
    offset = 0
    audio[0 + offset: n + offset, 0] += A_note
    audio[0 + offset: n + offset, 1] += 0.125 * A_note
    offset = 5500
    audio[0 + offset: n + offset, 0] += 0.5 * Csh_note
    audio[0 + offset: n + offset, 1] += 0.5 * Csh_note
    offset = 11000
    audio[0 + offset: n + offset, 0] += 0.125 * E_note
    audio[0 + offset: n + offset, 1] += E_note

    # normalize to 16-bit range
    audio *= 32767 / np.max(np.abs(audio))
    # convert to 16-bit data
    audio = audio.astype(np.int16)

    # start playback
    play_obj = sa.play_buffer(audio, 2, 2, sample_rate)

# wait for playback to finish before exiting
play_obj.wait_done()