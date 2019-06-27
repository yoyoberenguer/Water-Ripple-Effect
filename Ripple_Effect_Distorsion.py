# encoding: utf-8
"""
                   GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 """


from math import sin, exp, isnan
import math
import random
import pygame
import numpy
from numpy import *
import timeit
import sys


dampening = 0.8


def new_(cols_, rows_, previous, current):

    ii = 0
    cols2 = cols_ / 2
    rows2 = rows_ / 2
    
    for i in range(0, cols_ - 1):
    
        for j in range(0, rows_ - 1):

            data = (previous[i + 1][j] + previous[i - 1][j] + previous[i][j - 1] + previous[i][j + 1]) / 2
            data -= current[i, j]
            data -= data / 32
            current[i, j] = data
            data = (1024 - data) / 1024
            a = int(((i - rows2) * data) + rows2)
            b = int(((j - cols2) * data) + cols2)
            a %= rows_
            b %= cols_
            background.set_at((i, j), texture.get_at((a, b)))
            ii += 1
    temp = previous
    previous = current
    current = temp
    return previous, current



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
def new__(previous, current):

    # global previous, current
    a = ax.copy()
    b = ay.copy()
    data = (shift_vert_pos(previous, 1) + shift_vert_neg(previous, -1) +
           shift_horiz_pos(previous, 1) + shift_horiz_neg(previous, -1)) / 2

    data -= current
    # data *= dampening
    data -= data / 32

    current = data
    
    data = (1024 - data) / 1024
    
    a = a * data + rows2
    b = b * data + cols2
    # b = a.copy()
    # a = numpy.rot90(a, -1)
    # a = numpy.flip(a, axis=0)

    a /= (rows - 1)
    b /= (cols - 1)
    c = numpy.dstack((a % rows, b % cols)).astype(numpy.uint8)

    
    for i in range(cols - 1):
         for j in range(rows - 1):
            SCREEN.set_at((i, j), texture.get_at(c[i, j]))

    temp = previous
    previous = current
    current = temp
    return previous, current


if __name__ == '__main__':

    numpy.set_printoptions(threshold=sys.maxsize)
    MAXFPS = 80
    cols = 250
    rows = 250
    rows2 = rows // 2
    cols2 = cols // 2
    SCREENRECT = pygame.Rect(0, 0, cols, rows)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWSURFACE, 32)
    SCREEN.set_alpha(None)
    pygame.init()

    texture = pygame.image.load('Assets\\background.jpg').convert()
    # texture = pygame.image.load('writing.jpeg').convert()
    texture = pygame.transform.flip(texture, 0, 1)
    texture = pygame.transform.smoothscale(texture, (cols, rows))
    texture.set_alpha(None)

    ax = numpy.zeros((rows, cols))
    ii = 0
    for i in range(cols):
        for j in range(rows):
            # print(ii - rows2)
            ax[i, j] = (ii - rows2)
            ii += 1

    ay = numpy.zeros((rows, cols))
    ii = 0
    for i in range(cols):
        for j in range(rows):
            ay[j, i] = (ii - cols2)
            ii += 1

    clock = pygame.time.Clock()
    TIME_PASSED_SECONDS = clock.tick(MAXFPS)
    All = pygame.sprite.Group()
    FRAME = 0
    recording = False
    VIDEO = []
    STOP_GAME = False
    PAUSE = False

    background = texture.copy()

    current = numpy.zeros((cols, rows), dtype=numpy.float64)
    previous = current.copy()

    while not STOP_GAME:

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

                previous[int(mouse_pos.x), int(mouse_pos.y)] = 512

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        if keys[pygame.K_F8]:
            pygame.image.save(SCREEN, 'Screendump' + str(FRAME) + '.png')

        if keys[pygame.K_PAUSE]:
            PAUSE = True

        rnd = random.randint(0, 1000)
        if rnd > 800:
            previous[random.randint(0, rows - 1), random.randint(0, cols - 1)] = random.randint(512, 1024)
            # previous[rows2, cols2] = 1024

        previous, current = new__(previous, current)
        # previous, current = new_(cols, rows, previous, current)
        
        #SCREEN.blit(background, (0, 0))

        pygame.display.flip()

        FRAME += 1

    pygame.quit()
