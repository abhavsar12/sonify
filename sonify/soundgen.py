"""Generate sonified sound from data."""

import numpy as np
from scipy.io.wavfile import write

fs = 44100


def arrange_harmonies(freqs, track_len):
    track = np.zeros((track_len * fs, len(freqs)))
    t = np.arange(track_len * fs)
    for i, freq in enumerate(freqs):
        track[:, i] = np.sin(2 * np.pi * freq * t / fs)
    
    return track


def sonify_data(track, data):
    track_len = track.shape[0]
    data_len = data.shape[0]
    data_time = int(np.ceil(track_len / data_len))
    for i in range(data_len):
        j = i * data_time
        if j + data_time > track_len:
            track[j:, :] *= data[i, 1:]
        else:
            track[j:j+data_time, :] *= data[i, 1:]
    
    return track


def render_track(track):
    summed_track = np.sum(track, axis=1)
    norm_track = np.int16(summed_track / np.max(np.abs(summed_track)) * 32767)
    return norm_track


def play_track(track):
    write('test.wav', fs, track)
