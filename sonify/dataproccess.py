"""Module for converting 2D data to matrix data for sonification."""

import numpy as np


def norm_and_quantize_data(data, num_voices):
    y = np.array(data['y'])
    y = (y - min(y))/(max(y) - min(y))

    y *= num_voices
    y = y.astype(int)
    y[y > num_voices - 1] = num_voices - 1
    y += 1

    return np.array([data['x'], y.tolist()])


def gen_sonification_mat(data, num_voices, block_percent, overlap_percent):
    y = np.array(data[1, :])
    data_len = len(y)
    block_len = int(np.round(data_len * block_percent))
    if block_len == 0:
        raise ValueError("Block length is zero. Choose a larger block percentage.")
    block_iter = int(np.round(block_len * (1 - overlap_percent)))
    if block_iter == 0:
        raise ValueError("Overlap length is equal to the block length. Choose a smaller overlap percentage.")

    son_data_len = int(np.ceil(data_len / block_iter))
    son_data = np.zeros((son_data_len, num_voices + 1))

    for i in range(son_data_len):
        j = i * block_iter
        if j + block_len > data_len:
            arr = np.concatenate(((y[j:]), np.zeros(j + block_len - data_len)))
        else:
            arr = y[j:j+block_len]
        son_data[i, :] = _count_occurences(arr, num_voices)
        son_data[i, :] /= sum(son_data[i, :])

    return son_data


def _count_occurences(vals, num_voices):
    occurences = np.zeros(num_voices + 1)
    for val in vals:
        occurences[int(val)] += 1
    return occurences
