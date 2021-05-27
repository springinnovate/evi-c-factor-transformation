"""Fit an exponential curve to input data."""
import argparse
import matplotlib.pyplot as plt
import numpy as np



import numpy
import scipy.optimize

def exp_decay(val, a, b):
    return 1-a*numpy.exp(-val**b)

def exp_exp_decay(val, a, b, c):
    return 1-a*numpy.exp(-val**b)**c


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fit Exponential Decay')
    parser.add_argument(
        'exponential_csv_file',
        help='Path to exponential csv')
    args = parser.parse_args()
    x_list = []
    y_list = []
    with open(args.exponential_csv_file, 'r') as exponential_file:
        for line in exponential_file:
            x, y = line.rstrip().split(',')
            x_list.append(float(x))
            y_list.append(float(y))

    fig, ax = plt.subplots()
    ax.plot(x_list, y_list, 'x', label=f'points from {args.exponential_csv_file}')

    x_sample = numpy.linspace(min(x_list), max(x_list), 50)
    p0, variant = scipy.optimize.curve_fit(
        exp_decay,
        x_list,
        y_list,
        p0=[1, -0.1],
        method='lm')
    y_exp = exp_decay(x_sample, *p0)
    exp_decay_string = f'1-{p0[0]:.5f}*numpy.exp(-x**{p0[1]:.5f})'
    ax.plot(x_sample, y_exp, '-', label=exp_decay_string)

    p0, variant = scipy.optimize.curve_fit(
        exp_exp_decay,
        x_list,
        y_list,
        p0=[1, -0.1, 1],
        method='lm')
    y_exp_exp = exp_exp_decay(x_sample, *p0)
    exp_exp_decay_string = f'1-{p0[0]:.5f}*numpy.exp(-x**{p0[1]:.5f})**{p0[2]:.5f}'
    ax.plot(x_sample, y_exp_exp, '-', label=exp_exp_decay_string)

    ax.set(xlabel='x', ylabel='y')
    legend = ax.legend(loc='upper right')
    ax.grid()
    print('**** function fit ->')
    print(exp_decay_string)
    print(exp_exp_decay_string)
    plt.show()