

from math import sin, exp, isnan

import numpy

import math

dampening = 0.97  # 0.97


# method 1

# Slow method with python, works fine with language C

# and Java.

def ripple_1(cols_, rows_):
    global previous, current

    for i in range(1, cols_ - 1):

        for j in range(1, rows_ - 1):
            val = ((previous[i + 1][j] + previous[i - 1][j] + previous[i][j - 1] + previous[i][j + 1]) / 2) \
 \
                  - current[i, j]

        current[i, j] = val * dampening


# method 2

def ripple_2():
    global previous, current

    val = (numpy.roll(previous, 1, axis=0) + numpy.roll(previous, -1, axis=0) +

           numpy.roll(previous, 1, axis=1) + numpy.roll(previous, -1, axis=1)) / 2 - current

    current = val * dampening

    temp = previous

    previous = current

    current = temp


def shift_vert(arr, num, fill_value=0):
    result = numpy.empty_like(arr)

    if num > 0:

        result[:num, :] = fill_value  # first row

        result[num:, :] = arr[:-num, :]

    elif num < 0:

        result[num:, :] = fill_value  # last row

        result[:num, :] = arr[-num:, :]

    else:

        result = arr

    return result


def shift_horiz(arr, num, fill_value=0):
    result = numpy.empty_like(arr)

    if num > 0:

        result[:, :num] = fill_value

        result[:, num:] = arr[:, :-num]

    elif num < 0:

        result[:, num:] = fill_value

        result[:, :num] = arr[:, -num:]

    else:

        result = arr

    return result


# method 3

def ripple_3():
    global previous, current

    val = (shift_vert(previous, 1) + shift_vert(previous, -1) +

           shift_horiz(previous, 1) + shift_horiz(previous, -1)) / 2 - current

    current = val * dampening

    temp = previous

    previous = current

    current = temp


def shift_vert_pos(arr, num, fill_value=0):
    result = numpy.empty_like(arr)

    result[:num, :] = fill_value  # first row

    result[num:, :] = arr[:-num, :]

    return result


def shift_vert_neg(arr, num, fill_value=0):
    result = numpy.empty_like(arr)

    result[num:, :] = fill_value  # last row

    result[:num, :] = arr[-num:, :]

    return result


def shift_horiz_pos(arr, num, fill_value=0):
    result = numpy.empty_like(arr)

    result[:, :num] = fill_value

    result[:, num:] = arr[:, :-num]

    return result


def shift_horiz_neg(arr, num, fill_value=0):
    result = numpy.empty_like(arr)

    result[:, num:] = fill_value

    result[:, :num] = arr[:, -num:]

    return result


# method 3

def ripple_4(previous, current):
    val = (shift_vert_pos(previous, 1) + shift_vert_neg(previous, -1) +

           shift_horiz_pos(previous, 1) + shift_horiz_neg(previous, -1)) / 2 - current

    # val -= val / 32

    current = val * dampening

    temp = previous

    previous = current

    current = temp

    return previous, current

