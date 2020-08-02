import simpleaudio as sa
import numpy as np


POS_MAX = int(2 ** 16 / 2 - 1)
NEG_MAX = int(2 ** 16 / 2) * -1


def play_file():
    filename = 'myfile.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()  # Wait until sound has finished playing

def sinus_sample(freq, microseconds, rate):
    miliseconds = int(microseconds / 1000)
    # Generate array with seconds*sample_rate steps, ranging between 0 and seconds
    t = np.linspace(0, miliseconds, miliseconds * int(rate / 1000), False)
    # Generate sine wave
    note = np.sin(freq* t * 2 * np.pi)
    # Ensure that highest value is in 16-bit range
    audio = note * (2**15 - 1) / np.max(np.abs(note))
    for x in range(len(audio)):
        print(audio[x])

    return audio

def triangular_sample(freq, microseconds, rate):
    slope_rise = np.linspace(NEG_MAX, POS_MAX, int(rate/freq/2))
    slope_fall = np.linspace(POS_MAX, NEG_MAX, int(rate/freq/2))
    wave = np.concatenate((slope_rise, slope_fall))
    audio = wave # start autio with something to concatenate on
    wave_duration = int(1 / freq * 1000000) # microseconds per wave

    # 1 second of noise would be x in range(freq)
    for x in range(int(microseconds / wave_duration)):
        audio = np.concatenate((audio, wave))

    return audio

def square_sample(freq, microseconds, rate):
    # a single wave consists of 4 parts with half of it is silence
    first_half = np.full((int(rate/freq/4),), POS_MAX)
    second_half = np.full((int(rate/freq/4),), NEG_MAX)
    wave = np.concatenate((first_half, second_half))
    wave = np.concatenate((wave, np.zeros(int(rate/freq/2))))
    audio = wave # start autio with something to concatenate on
    wave_duration = int(1 / freq * 1000000) # microseconds per wave
    # 1 second of noise would be x in range(freq)
    for x in range(int(microseconds / wave_duration)):
        audio = np.concatenate((audio, wave))

    return audio

def play_sample():
    x = 60
    rate = 44100  # 44100 samples per second

    silence100ms = np.zeros(int(rate/10))
    audio = silence100ms # 100ms of silence

    for freq in (x, x*2, x, x*3, x, x*4, x*3, x*2):
        audio = np.concatenate((audio, triangular_sample(freq, 100000, rate)))
        audio = np.concatenate((audio, silence100ms))
        audio = np.concatenate((audio, triangular_sample(freq, 100000, rate)))
        audio = np.concatenate((audio, silence100ms))
        audio = np.concatenate((audio, square_sample(freq, 100000, rate)))
        audio = np.concatenate((audio, silence100ms))
        audio = np.concatenate((audio, square_sample(freq, 100000, rate)))
        audio = np.concatenate((audio, silence100ms))

    audio = audio.astype(np.int16)
    # sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    play_obj = sa.play_buffer(audio, 1, 2, rate)
    # Wait for playback to finish before exiting
    play_obj.wait_done()

def play_sample_2():
    x = 60
    rate = 44100  # 44100 samples per second

    silence100ms = np.zeros(int(rate/1000))
    a1 = silence100ms # 100ms of silence
    a2 = silence100ms # 100ms of silence

    for freq in (x, x*2, x, x*3, x, x*4, x*3, x*2):
        a1 = np.concatenate((a1, triangular_sample(freq, 100000, rate)))
        a1 = np.concatenate((a1, silence100ms))
        a1 = np.concatenate((a1, triangular_sample(freq, 100000, rate)))
        a1 = np.concatenate((a1, silence100ms))
        a2 = np.concatenate((a2, square_sample(freq, 100000, rate)))
        a2 = np.concatenate((a2, silence100ms))
        a2 = np.concatenate((a2, square_sample(freq, 100000, rate)))
        a2 = np.concatenate((a2, silence100ms))

    if len(a2) <  len(a1):
        diff = len(a1) - len(a2)
        a2 = np.concatenate((a2, np.zeros(diff)))

    a1 = a1.astype(np.int16)
    a2 = a2.astype(np.int16)

    audio = np.array((a1, a2))
    # sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    play_obj = sa.play_buffer(audio, 1, 2, rate)
    # Wait for playback to finish before exiting
    play_obj.wait_done()

def play_sample_stereo():
    x = 60
    rate = 44100  # 44100 samples per second

    silence100ms = np.zeros(int(rate / 1000))
    a1 = silence100ms  # 100ms of silence
    a2 = silence100ms  # 100ms of silence

    for freq in (x, x * 2, x, x * 3, x, x * 4, x * 3, x * 2):
        a1 = np.concatenate((a1, triangular_sample(freq, 100000, rate)))
        a1 = np.concatenate((a1, silence100ms))
        a1 = np.concatenate((a1, triangular_sample(freq, 100000, rate)))
        a1 = np.concatenate((a1, silence100ms))
        a2 = np.concatenate((a2, square_sample(freq, 100000, rate)))
        a2 = np.concatenate((a2, silence100ms))
        a2 = np.concatenate((a2, square_sample(freq, 100000, rate)))
        a2 = np.concatenate((a2, silence100ms))

    if len(a2) < len(a1):
        diff = len(a1) - len(a2)
        a2 = np.concatenate((a2, np.zeros(diff)))

    a1 = a1.astype(np.int16)
    a2 = a2.astype(np.int16)

    # A 2D array where the left and right tones are contained in their respective rows
    audio = np.vstack((a1, a2))

    # Reshape 2D array so that the left and right tones are contained in their respective columns
    audio = audio.transpose()
    audio = audio.copy(order='C')
    print(audio.flags)

    # sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    play_obj = sa.play_buffer(audio, 2, 2, rate)
    #wo = sa.WaveObject(audio, 2, 2, 44100)
    #play_obj = wo.play()
    # Wait for playback to finish before exiting
    play_obj.wait_done()
    return audio

def play_sample_stereo_2():
    x = 60
    rate = 44100  # 44100 samples per second

    silence100ms = np.zeros(int(rate / 1000))
    a1 = silence100ms  # 100ms of silence
    a2 = silence100ms  # 100ms of silence

    for freq in (x, x * 2, x, x * 3, x, x * 4, x * 3, x * 2):
        a1 = np.concatenate((a1, triangular_sample(freq, 100000, rate)))
        a1 = np.concatenate((a1, silence100ms))
        a1 = np.concatenate((a1, silence100ms))
        a1 = np.concatenate((a1, triangular_sample(freq, 100000, rate)))
        a1 = np.concatenate((a1, silence100ms))
        a1 = np.concatenate((a1, silence100ms))
        a2 = np.concatenate((a2, triangular_sample(freq, 100000, rate)))
        a2 = np.concatenate((a2, silence100ms))
        a2 = np.concatenate((a2, triangular_sample(freq, 100000, rate)))
        a2 = np.concatenate((a2, silence100ms))

    if len(a2) < len(a1):
        diff = len(a1) - len(a2)
        a2 = np.concatenate((a2, np.zeros(diff)))

    a1 = a1.astype(np.int16)
    a2 = a2.astype(np.int16)

    # A 2D array where the left and right tones are contained in their respective rows
    audio = np.vstack((a1, a2))

    # Reshape 2D array so that the left and right tones are contained in their respective columns
    audio = audio.transpose()
    audio = audio.copy(order='C')
    print(audio.flags)

    # sa.play_buffer(audio_data, num_channels, bytes_per_sample, sample_rate)
    play_obj = sa.play_buffer(audio, 2, 2, rate)
    #wo = sa.WaveObject(audio, 2, 2, 44100)
    #play_obj = wo.play()
    # Wait for playback to finish before exiting
    play_obj.wait_done()

    return audio

if __name__ == '__main__':
    play_sample_stereo_2()

