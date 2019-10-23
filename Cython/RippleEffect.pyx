# encoding: utf-8


import numpy
from numpy import ndarray, asarray, empty_like, dstack, putmask, float32, roll
cimport cython
cimport numpy as np

cdef double dampening = 0.9


# CREATE A WATER RIPPLE EFFECT ON A PYGAME SURFACE.
# Returns 3 numpy arrays 'previous' and 'current' representing the surface water
# disturbances; returns the background_array representing the background image
# distorted by the water effect
# 
# This method loop over all the pixels.

def new_(cols_: int, rows_:int, previous: ndarray, current: ndarray,
         texture_array: ndarray, background_array: ndarray):
    """

    :param cols_: integer, representing the image height (surface height)
    :param rows_: integer, representing the image width (surface width)
    :param previous: numpy.ndarray type (w, h) of type float32 (previous water state)
    :param current: numpy.ndarray type(w, h) of type float32 (current water state)
    :param texture_array: numpy.ndarray type (w, h, 3) type uint8 (background texture
                          without deformation)
    :param background_array: numpy.ndarray type (w, h, 3) type uint8 background texture
    :return: Return 3 numpy arrays (current, previous, background_array)
    """
    
    return new_c(cols_, rows_, previous, current,
                 texture_array, background_array)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef new_c(int cols_, int rows_,
           float [:, :] previous,                       # type numpy.float32 (w, h)
           float [:, :] current,                        # type numpy.float32 (w, h)
           unsigned char [:, :, :] texture_array,       # type numpy.ndarray (w, h, 3)
           unsigned char [:, :, :] background_array,    # type numpy.ndarray (w, h, 3)
           ):

    cdef:
        float cols2 = cols_ >> 1
        float rows2 = rows_ >> 1
        int i, j, a, b
        int cols_1 = cols_ - 1
        int rows_1 = rows_ - 1
        float data
        float [:, :] temp
        float c1 = 1.0 / 1024.0
    
    # from 1 to w - 1 to avoid python wraparound error
    # same for j (1 to h - 1)

    for j in range(1, cols_1):
        for i in range(1, rows_1):
            
            data = (previous[i + 1, j] + previous[i - 1, j] +
                    previous[i, j - 1] + previous[i, j + 1]) * 0.5
            data -= current[i, j]
            data -= data * 0.03125
            current[i, j] = data
            data = 1 - data * c1
        
            a = max(<int>(((i - rows2) * data) + rows2) % rows_, 0)
            b = max(<int>(((j - cols2) * data) + cols2) % cols_, 0)
            background_array[i, j, 0], background_array[i, j, 1], background_array[i, j, 2] = \
                texture_array[a, b, 0], texture_array[a, b, 1], texture_array[a, b, 2]
            # if a + 1 < rows_ :
            #    background_array[i + 1, j, 0], background_array[i + 1, j, 1], background_array[i + 1, j, 2] = \
            #        texture_array[a + 1, b, 0], texture_array[a + 1, b, 1], texture_array[a + 1, b, 2]

    return current, previous, asarray(background_array)



@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef shift_vert_pos(float [:, :] arr, int num):
    cdef float fill_value=0.0
    cdef float [:, :] result = numpy.empty_like(arr, dtype=float32)
    result[:num, :] = fill_value  
    result[num:, :] = arr[:-num, :]
    return asarray(result)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef shift_vert_neg(float [:, :] arr, int num):
    cdef float fill_value=0.0
    cdef float [:, :] result = numpy.empty_like(arr, dtype=float32)
    result[num:, :] = fill_value
    result[:num, :] = arr[-num:, :]
    return asarray(result)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef shift_horiz_pos(float [:, :] arr, int num):
    cdef float fill_value=0.0
    cdef float [:, :] result = numpy.empty_like(arr, dtype=float32)
    result[:, :num] = fill_value
    result[:, num:] = arr[:, :-num]
    return asarray(result)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef shift_horiz_neg(float [:, :] arr, int num):
    cdef float fill_value=0.0
    cdef float [:, :] result = numpy.empty_like(arr, dtype=float32)
    result[:, num:] = fill_value
    result[:, :num] = arr[:, -num:]
    return asarray(result)



# CREATE A WATER RIPPLE EFFECT ON A PYGAME SURFACE.
# Returns 3 numpy arrays 'previous' and 'current' representing the surface water
# disturbances; returns the background_array representing the background image
# distorted by the water effect
# 
# This method apply first the blur to all pixels using numpy array and loop
# over all pixels to apply background deformation.

def new__(cols_: int, rows_: int, previous: ndarray, current: ndarray,
          texture_array: ndarray, background_array: ndarray):
    """

    :param cols_: integer, representing the image height (surface height)
    :param rows_: integer, representing the image width (surface width)
    :param previous: numpy.ndarray type (w, h) of type float32 (previous water state)
    :param current: numpy.ndarray type(w, h) of type float32 (current water state)
    :param texture_array: numpy.ndarray type (w, h, 3) type uint8 (background texture
                          without deformation)
    :param background_array: numpy.ndarray type (w, h, 3) type uint8 background texture
    :return: Return 3 numpy arrays (current, previous, background_array)
    """
    return new__c(cols_, rows_, previous, current, texture_array, background_array)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef new__c(int cols_, int rows_,
            np.ndarray[np.float32_t, ndim=2] previous,
            np.ndarray[np.float32_t, ndim=2] current,
            unsigned char [:, :, :] texture_array,
            unsigned char [:, :, :] background_array
            ):
    cdef np.ndarray[np.float32_t, ndim=2] data = \
            (shift_vert_pos(previous, 1) + shift_vert_neg(previous, -1) +
            shift_horiz_pos(previous, 1) + shift_horiz_neg(previous, -1)) * 0.5
    #cdef np.ndarray[np.float32_t, ndim=2] data = (roll(previous, -1, axis=1) + roll(previous, 1, axis=1)
    #    + roll(previous, 1, axis=0) + roll(previous, -1, axis=0)) * 0.5

    data -= current
    # data *= dampening
    data -= data * 0.03125
    current = data
    data = 1 - data / 1024

    cdef:
        int i, j, a, b
        int cols_1 = cols_ - 1
        int rows_1 = rows_ - 1
        int rows2 = rows_ >> 1
        int cols2 = cols_ >> 1

    for i in range(1, cols_1):
        for j in range(1, rows_1 ):
            a = max(<int>(((j - rows2) * data[j, i]) + rows2) % rows_, 0)
            b = max(<int>(((i - cols2) * data[j, i]) + cols2) % cols_, 0)
            background_array[j, i, 0], background_array[j, i, 1], background_array[j, i, 2] = \
                texture_array[a, b, 0], texture_array[a, b, 1], texture_array[a, b, 2]
            # if a + 1 < rows_ :
            #    background_array[i + 1, j, 0], background_array[i + 1, j, 1], background_array[i + 1, j, 2] = \
            #        texture_array[a + 1, b, 0], texture_array[a + 1, b, 1], texture_array[a + 1, b, 2]

    return current, previous, asarray(background_array)


