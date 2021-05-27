import numpy
import scipy.optimize

evi_vs_c = [
    (0.02874, 0.95),
    (0.18186, 0.25),
    (0.3643000126, 0.13575),
    (0.33039, 0.07075),
    (0.54826, 0.035425),
    (0.65346, 0.0001),
    ]

def c_factor(evi, a, b, c):
    import numpy
import scipy.optimize

evi_vs_c = [
    (0.02874, 0.95),
    (0.18186, 0.25),
    (0.3643000126, 0.13575),
    (0.33039, 0.07075),
    (0.54826, 0.035425),
    (0.65346, 0.0001),
    ]

def make_c_factor(evi_lin_start, evi_lin_end):
    def c_factor(evi, a, b, c):
        return numpy.clip(
            1-a*numpy.exp(-evi**b)**c +
            0.07075*(evi_lin_end-evi)/(evi_lin_end-evi_lin_start),
            0.0001, 1.0)
    return c_factor

evi_lin_start = 0.65346
evi_lin_end = 0.33039

c_factor = make_c_factor(evi_lin_start, evi_lin_end)
p0, variant = scipy.optimize.curve_fit(
    c_factor,
    [x[0] for x in evi_vs_c],
    [x[1] for x in evi_vs_c],
    p0=[3, -0.3, 1],
    method='lm')

print(p0, variant)
error_sum = 0.0
for evi_val, expected in evi_vs_c:
    error_sum += (expected-c_factor(evi_val, *p0))**2

print(error_sum)
print(f'1-{p0[0]}*numpy.exp(-evi**{p0[1]})**{p0[2]} + 0.07075 * ({evi_lin_end}-evi)/({evi_lin_end}-{evi_lin_start})')
for p in p0:
    print(p)