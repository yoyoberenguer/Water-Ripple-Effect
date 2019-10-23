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

dampening = 0.9


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


def new_alpha(cols_, rows_, previous, current):

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
                index = int(((a * rows_) + b) * 3)
                pixel = (texture_buffer[index],  # -> red
                         texture_buffer[index + 1],  # -> green
                         texture_buffer[index + 2])  # -> blue

                back_array[i, j] = pixel  # text_array[a, b,:3]

            ii += 1
    temp = previous
    previous = current
    current = temp
    return previous, current, back_array


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


def new__(previous, current):

    a = ax.copy()
    b = ay.copy()
    data = (shift_vert_pos(previous, 1) + shift_vert_neg(previous, -1) +
            shift_horiz_pos(previous, 1) + shift_horiz_neg(previous, -1)) / 2

    data -= current
    data *= dampening
    current = data
    data = 1 - data / 1024

    a = (a * data + w2) / width
    b = (b * data + h2) / height

    """
    def vectors(i, j):
        for i in range(0, height - 1):
            for j in range(0, width - 1):
                if data[i, j] != 1:
                    background.set_at((i, j), texture.get_at(c[i, j]))
    """
    c = numpy.dstack((a, b)).astype(numpy.int)
    numpy.putmask(c, c > width - 1, width - 1)

    # vectorize = numpy.vectorize(vectors)
    # vectorize(i, j)

    for i in range(0, height - 1):
        for j in range(0, width - 1):
            if data[i, j] != 1:
                background.set_at((i, j), texture.get_at(c[i, j]))


    temp = previous
    previous = current
    current = temp
    return previous, current, background


def new__alpha(previous, current):

    a = ax.copy()
    b = ay.copy()
    data = (shift_vert_pos(previous, 1) + shift_vert_neg(previous, -1) +
            shift_horiz_pos(previous, 1) + shift_horiz_neg(previous, -1)) / 2

    data -= current
    data *= dampening
    current = data
    data = 1 - data / 1024

    a = (a * data + w2) / width
    b = (b * data + h2) / height

    c = numpy.dstack((a, b)).astype(numpy.int)
    numpy.putmask(c, c > width - 1, width - 1)

    for i in range(0, height - 1):
        for j in range(0, width - 1):
            if data[i, j] != 1:
                ii, jj = c[i, j]
                # index = ((ii * width) + jj) * 3
                # back_array[i, j] = (texture_buffer[index], texture_buffer[index + 1], texture_buffer[index + 2])
                back_array[i, j] = texture_array[ii, jj]


    temp = previous
    previous = current
    current = temp
    return previous, current, back_array


if __name__ == '__main__':

    numpy.set_printoptions(threshold=sys.maxsize)
    MAXFPS = 80
    height = 250
    width = 250
    w2 = width // 2
    h2 = height // 2
    SCREENRECT = pygame.Rect(0, 0, height, width)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, 32)
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
    for i in range(width):
        for j in range(height):
            ax[i, j] = ii - w2
            ii += 1

    ay = numpy.rot90(ax)

    clock = pygame.time.Clock()
    TIME_PASSED_SECONDS = clock.tick(MAXFPS)
    All = pygame.sprite.Group()
    FRAME = 0
    recording = False
    VIDEO = []
    STOP_GAME = False
    PAUSE = False

    background = texture.copy()

    current = numpy.zeros((width, height), dtype=numpy.float)
    previous = current.copy()

    texture_buffer = memoryview(texture.get_view('3')).tobytes()
    texture_array = pygame.surfarray.array3d(texture)
    back_array = pygame.surfarray.array3d(background)

    while not STOP_GAME:

        pygame.event.pump()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

                previous[int(mouse_pos.x % width), int(mouse_pos.y % height)] = 1024

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        if keys[pygame.K_F8]:
            pygame.image.save(SCREEN, 'Screendump' + str(FRAME) + '.png')

        if keys[pygame.K_PAUSE]:
            PAUSE = True

        rnd = random.randint(0, 1000)
        if rnd > 100:

            previous[random.randint(0, width - 2), random.randint(0, height - 2)] = 1024  # random.randint(512, 1024)
            # previous[width//2, height//2] = 1024

        # previous, current, background = new__(previous, current)
        # SCREEN.blit(background, (0, 0))

        # previous, current, array = new_alpha(width, height, previous, current)
        # pygame.surfarray.blit_array(SCREEN, array)

        previous, current, background = new__alpha(previous, current)
        SCREEN.blit(pygame.surfarray.make_surface(background), (0, 0))

        pygame.display.flip()

        FRAME += 1

    pygame.quit()