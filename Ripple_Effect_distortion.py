# encoding: utf-8
"""
                   GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007
 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.
 """

import pygame
import numpy
from numpy import *
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
            data = 1 - data/1024

            oldata = lastmap[ii]
            lastmap[ii] = data
            if oldata != data:
                a = int(((i - rows2) * data) + rows2)
                b = int(((j - cols2) * data) + cols2)
                a %= rows_
                b %= cols_
                SCREEN.set_at((i, j), texture.get_at((a, b)))

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

    ii = 0
    a = ax.copy()
    b = ay.copy()
    data = (shift_vert_pos(previous, 1) + shift_vert_neg(previous, -1) +
            shift_horiz_pos(previous, 1) + shift_horiz_neg(previous, -1)) / 2

    data -= current
    # data *= dampening
    data -= data / 16
    current = data
    data = 1 - data/1024

    a = a * data + rows2
    # b = b * data + cols2
    a /= (width - 1)
    # b /= (height - 1)
    b = numpy.rot90(a.copy())   # only if width and height are equals else uncomment b lines
    c = numpy.dstack((a % width, b % height)).astype(numpy.uint8)

    # todo vectorised below
    for i in range(height - 1):
        for j in range(width - 1):
            if data[i, j] != 1:
                background.set_at((i, j), texture.get_at(c[i, j]))
    ii += 1

    temp = previous
    previous = current
    current = temp
    return previous, current


if __name__ == '__main__':

    numpy.set_printoptions(threshold=sys.maxsize)
    MAXFPS = 80
    height = 200
    width = 200
    rows2 = width // 2
    cols2 = height // 2
    SCREENRECT = pygame.Rect(0, 0, height, width)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWSURFACE, 32)
    SCREEN.set_alpha(None)
    pygame.init()

    texture = pygame.image.load('Assets\\hqdefault.jpg').convert()
    texture = pygame.transform.smoothscale(texture, (height, width))
    texture.set_alpha(None)

    lastmap = []
    for r in range(width * height):
        lastmap.append(0)

    ax = numpy.zeros((width, height))
    ii = 0
    for i in range(height):
        for j in range(width):
            # print(ii - rows2)
            ax[i, j] = (ii - rows2)
            ii += 1

    ay = numpy.zeros((width, height))
    ii = 0
    for i in range(height):
        for j in range(width):
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

    current = numpy.zeros((height, width), dtype=numpy.float64)
    previous = current.copy()

    while not STOP_GAME:

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

                previous[int(mouse_pos.x), int(mouse_pos.y)] = 1024

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        if keys[pygame.K_F8]:
            pygame.image.save(SCREEN, 'Screendump' + str(FRAME) + '.png')

        if keys[pygame.K_PAUSE]:
            PAUSE = True

        rnd = random.randint(0, 1000)
        if rnd > 800:
            previous[random.randint(0, width - 1), random.randint(0, height - 1)] = 1024  # random.randint(512, 1024)
            # previous[rows2, cols2] = 1024

        previous, current = new__(previous, current)
        # previous, current = new_(cols, rows, previous, current)

        SCREEN.blit(background, (0, 0))

        pygame.display.flip()

        FRAME += 1

    pygame.quit()