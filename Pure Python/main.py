import random

import pygame
import numpy
import timeit
import RippleEffect
from RippleEffect import *


if __name__ == '__main__':

    MAXFPS = 80
    cols = 300
    rows = 300
    SCREENRECT = pygame.Rect(0, 0, cols, rows)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, pygame.HWSURFACE, 32)
    SCREEN.set_alpha(None)
    pygame.init()

    background = pygame.image.load('Assets\\background.jpg').convert()
    background = pygame.transform.smoothscale(background, (cols, rows))
    background.set_alpha(None)

    clock = pygame.time.Clock()
    TIME_PASSED_SECONDS = clock.tick(MAXFPS)
    All = pygame.sprite.Group()
    FRAME = 0
    recording = False
    VIDEO = []
    STOP_GAME = False
    PAUSE = False

    current = numpy.zeros((cols, rows), dtype=numpy.uint8)
    previous = current.copy()

    bck_array = pygame.surfarray.array3d(background)
    bck_array_copy = bck_array.copy()

    # print(timeit.timeit('ripple_1(cols, rows, previous, current)',
    #                    'from __main__ import ripple_1, cols, rows, previous, current', number=10))
    # print(timeit.timeit('ripple_2(previous, current)',
    #                    'from __main__ import ripple_2, previous, current', number=10))
    # print(timeit.timeit('ripple_3(previous, current)',
    #                    'from __main__ import ripple_3, previous, current', number=1000))
    # print(timeit.timeit('ripple_4(previous, current)',
    #                    'from __main__ import ripple_4, previous, current', number=1000))

    while not STOP_GAME:

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:  # pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
                # current[int(mouse_pos.x), int(mouse_pos.y)] = 5000
                previous[int(mouse_pos.x), int(mouse_pos.y)] = 5000

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        if keys[pygame.K_F8]:
            pygame.image.save(SCREEN, 'Screendump' + str(FRAME) + '.png')

        if keys[pygame.K_PAUSE]:
            PAUSE = True

        rnd = random.randint(0, 1000)
        if rnd > 500:
            previous[random.randint(0, rows - 1), random.randint(0, cols - 1)] = random.randint(1000, 5000)

        previous, current = ripple_4(previous, current)

        # SCREEN.fill((0, 0, 0))

        array = numpy.full((cols, rows, 3), 0)

        # Red Ripple
        # array[:, :, 0:1] = current.reshape((cols, rows, 1))

        # Green Ripple
        # array[:, :, 1:2] = current.reshape((cols, rows, 1))

        # Blue Ripple
        # array[:, :, 2:3] = current.reshape((cols, rows, 1))

        # White
        array[:, :, :] = current.reshape((cols, rows, 1))

        # numpy.putmask(array, array > 255, 255)
        numpy.putmask(array, array < 0, 0)

        pygame.surfarray.blit_array(SCREEN, array)

        # pixelated wave
        # pygame.surfarray.blit_array(SCREEN, array.astype(dtype=numpy.uint8))

        # distortion
        # surface = Surface(current, cols, rows, bck_array)
        # pygame.surfarray.blit_array(SCREEN, surface)

        SCREEN.blit(background, (0, 0), special_flags=pygame.BLEND_RGB_ADD)

        # Cap the speed at 60 FPS
        TIME_PASSED_SECONDS = clock.tick(MAXFPS)
        # print(clock.get_fps())

        pygame.display.flip()

        FRAME += 1


    pygame.quit()
