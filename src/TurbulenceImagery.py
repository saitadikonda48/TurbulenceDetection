import h5py
import numpy as np
from PIL import Image
from math import exp
from math import sqrt
import os


def calculate_gradient():
    t = h5py.File("isotropic4096_1_4000_4000_1.h5", "r")
    pressure = t['p00000']
    shape = pressure.shape

    gradient_file = h5py.File("gradient_1_4000_4000_1.h5", "w")
    gradient = gradient_file.create_dataset("gradient", pressure.shape, dtype='f')
    for t, x, y, z in np.ndindex(gradient.shape):
        gradient[t, x, y, z] = grad_mag(pressure, t, x, y, z, gradient.shape)


def pressure():
    t = h5py.File("isotropic4096_1_4000_4000_1.h5", "r")
    pressure = t['p00000'][0, :, :, 0]
    max_abs = max(abs(np.max(pressure)), abs(np.min(pressure)))
    arr = [[pressure_pixel_map(max_abs, x) for x in l] for l in pressure]
    pixels = np.asarray(arr, 'uint8')
    path = 'C:\\Users\\rwill\\Pictures\\Turbulence\\'
    img = Image.fromarray(pixels, 'RGB')
    img.save(path + 'test2.png')
    img.show()


def gradient():
    t = h5py.File("gradient_1_2000_2000_1.h5", "r")
    grad = t['gradient'][0, :, :, 0]
    max_abs = np.max(grad)
    arr = [[pixel_map_level2(max_abs * 0.0005, max_abs * 0.05, x) for x in l] for l in grad]
    pixels = np.asarray(arr, 'uint8')
    path = ''
    img = Image.fromarray(pixels, 'RGBA')
    img.save(path + 'turbulence.png')
    # img.show()


def grad_mag(v, t, x, y, z, shape):
    grad_x = 0 if shape[1] == 1 else (v[t, 1, y, z] - v[t, x, y, z] if x == 0 else (v[t, x, y, z] - v[t, shape[1] - 2, y, z] if x == shape[1] - 1 else v[t, x + 1, y, z] - v[t, x - 1, y, z]))
    grad_y = 0 if shape[2] == 1 else (v[t, x, 1, z] - v[t, x, y, z] if y == 0 else (v[t, x, y, z] - v[t, x, shape[2] - 2, z] if y == shape[1] - 1 else v[t, x, y + 1, z] - v[t, x, y - 1, z]))
    grad_z = 0 if shape[3] == 1 else (v[t, x, y, 1] - v[t, x, y, z] if z == 0 else (v[t, x, y, z] - v[t, x, y, shape[3] - 2] if z == shape[1] - 1 else v[t, x, y, z + 1] - v[t, x, y, z - 1]))
    return grad_x**2 + grad_y**2 + grad_z**2


def valid_index(t, x, y, z, shape):
    return t >= 0 and x >= 0 and y >= 0 and z >= 0 and t < shape[0] and x < shape[1] and y < shape[2] and z < shape[3]


def pressure_pixel_map(max_abs, val):
    if val >= 0:
        v = int(val * 255 / max_abs)
        return 0, v, 0
    else:
        v = int(val * -255 / max_abs)
        return v, 0, 0


def pixel_map_positive(max_abs, val):
    if val >= 0:
        v = int(val * 255 / max_abs)
        return v, 0, 0


def pixel_map_sqrt(max_abs, val):
    if val >= 0:
        v = int(sqrt(val / max_abs) * 255)
        return 255, 0, 0, v


def pixel_map_sqrt_sqrt(max_abs, val):
    if val >= 0:
        v = int(sqrt(sqrt(val / max_abs)) * 255)
        return 255, 0, 0, v


def pixel_map_quadratic(max_abs, val):
    a = -1
    if val >= 0:
        x = val / max_abs
        return 255, 0, 0, int((a*x**2 + (1-a)*x) * 255)


def pixel_map_level(cutoff, val):
    return 255, 0, 0, int(255 / (1 + exp(100*cutoff-100*val)))


def pixel_map_level2(lower, upper, val):
    if val < lower:
        return 0, 0, 0, 0
    elif val > upper:
        return 255, 0, 0, 255
    else:
        return 255, 0, 0, int(255 * (val - lower) / (upper - lower))


def pixel_map_cutoff(cutoff, val):
    return (255, 0, 0, 255) if val >= cutoff else (0, 0, 0, 0)


if __name__ == "__main__":
    gradient()
