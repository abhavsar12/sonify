"""Generate sample data."""

import matplotlib.pyplot as plt
import numpy as np
import json


def gen_line(plot=False):
    m = 1
    x = np.arange(0, 10, 0.1)
    y = m * x

    data = {'x': x.tolist(), 'y': y.tolist()}
    if plot:
        plot_func(data)

    return data


def gen_parabola(plot=False):
    a = 1
    x = np.arange(0, 10, 0.1)
    y = a * x ** 2

    data = {'x': x.tolist(), 'y': y.tolist()}
    if plot:
        plot_func(data)

    return data


def gen_sine(plot=False):
    w = 1
    x = np.arange(0, 10, 0.1)
    y = np.sin(w * x)

    data = {'x': x.tolist(), 'y': y.tolist()}
    if plot:
        plot_func(data)

    return data


def plot_func(data):
    plt.plot(data['x'], data['y'])
    plt.show()


def write_func(data, fn):
    with open(fn + '.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


def main():
    write_func(gen_line(), 'sample_line')
    write_func(gen_parabola(), 'sample_parabola')
    write_func(gen_sine(), 'sample_sine')


if __name__ == "__main__":
    main()
