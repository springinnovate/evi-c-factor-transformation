import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
ax.set(xlabel='evi', ylabel='C factor')
ax.grid()


import numpy
import scipy.optimize

evi_vs_c = [
    (0.02874, 0.95),
    (0.18186, 0.25),
    (0.25782, 0.13575),
    (0.33039, 0.07075),
    (0.54826, 0.035425),
    (0.65346, 0.0001),
    ]


def make_c_factor(lin_start, lin_end):
    def c_factor(evi, a, b, c):
        return numpy.clip(
            (1-1/(1+numpy.exp(-(evi-lin_end))**10))*(1-a*numpy.exp(-evi**b)**c) +
            0.07075*(lin_start-evi)/(lin_start-lin_end),
            0.0001, 1.0)
    return c_factor

raw_evi_list = [x[0] for x in evi_vs_c]
raw_c_list = [x[1] for x in evi_vs_c]

lin_start = raw_evi_list[-1]
lin_end = raw_evi_list[-3]


c_factor = make_c_factor(lin_start, lin_end)
p0, variant = scipy.optimize.curve_fit(
    c_factor,
    raw_evi_list,
    raw_c_list,
    p0=[3, -0.3, 1],
    method='lm')

print(p0)
print(variant)
error_sum = 0.0
for evi_val, expected in evi_vs_c:
    error_sum += (expected-c_factor(evi_val, *p0))**2
print(f'r^2={error_sum}')

ax.plot(raw_evi_list, raw_c_list, 'x')
evi_vals = numpy.arange(0.01, 0.7, 0.01)
c_vals = c_factor(evi_vals, *p0)
ax.plot(evi_vals, c_vals)
a, b, c = p0
print(f'(1-1/(1+numpy.exp(-(evi-{lin_end}))**10))*(1-{a}*numpy.exp(-evi**{b})**{c}) +.07075*({lin_start}-evi)/({lin_start}-{lin_end})')

plt.show()