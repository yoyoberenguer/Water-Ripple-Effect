import pygame
import sys
import numpy
import random
from RippleEffect import new_, new__

if __name__ == '__main__':

    numpy.set_printoptions(threshold=sys.maxsize)

    height = 600
    width = 600
    w2 = width // 2
    h2 = height // 2
    SCREENRECT = pygame.Rect(0, 0, width, height)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size, 32)
    SCREEN.set_alpha(None)
    pygame.init()

    texture = pygame.image.load('Assets\\background.jpg').convert()
    texture = pygame.transform.smoothscale(texture, (width, height))
    texture.set_colorkey((0, 0, 0, 0), pygame.RLEACCEL)
    texture.set_alpha(None)

    clock = pygame.time.Clock()
    All = pygame.sprite.Group()
    FRAME = 0
    recording = False
    VIDEO = []
    STOP_GAME = False
    PAUSE = False

    background = texture.copy()

    current = numpy.zeros((width, height), dtype=numpy.float32)
    previous = numpy.zeros((width, height), dtype=numpy.float32)

    texture_array = pygame.surfarray.array3d(texture)
    back_array = pygame.surfarray.array3d(background)
    WaterSplash = pygame.mixer.Sound("SplashSound.wav")
    WaterSplash1 = pygame.mixer.Sound("SplashSound1.wav")
    WaterSplash2 = pygame.mixer.Sound("SplashSound2.wav")
    Splashes = [WaterSplash1, WaterSplash2]
    old_mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    ch = pygame.mixer.Channel(1)

    while not STOP_GAME:

        pygame.event.pump()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

                if (old_mouse_pos - mouse_pos).length() > 35.0:
                    if not ch.get_busy():
                        s = WaterSplash
                        ch.play(s, fade_ms=100)
                        s.set_volume(1.0)
                    else:

                        pygame.mixer.stop()
                        s = WaterSplash
                        ch.play(s, fade_ms=300)
                        s.set_volume(0.7)
                else:
                    if not ch.get_busy():
                        s = Splashes[random.randint(0, 1)]
                        ch.play(s, fade_ms=200)
                        s.set_volume(0.5)

                previous[int(mouse_pos.x % width), int(mouse_pos.y % height)] = 8192
                old_mouse_pos = mouse_pos

        if keys[pygame.K_ESCAPE]:
            STOP_GAME = True

        if keys[pygame.K_F8]:
            pygame.image.save(SCREEN, 'Screendump' + str(FRAME) + '.png')

        if keys[pygame.K_PAUSE]:
            PAUSE = True

        rnd = random.randint(0, 1000)
        if rnd > 880:
            previous[random.randint(0, width - 2), random.randint(0, height - 2)] = 8192

        previous, current, back_array =\
                   new_(height, width, previous, current, texture_array, back_array)

        # previous, current, back_array = \
        #            new__(height, width, previous, current, texture_array, back_array)

        SCREEN.blit(pygame.surfarray.make_surface(back_array).convert(), (0, 0))
        # surf=pygame.image.frombuffer(numpy.ascontiguousarray(back_array.transpose(1, 0, 2)), (width, height), 'RGB')
        # surf.set_colorkey((0, 0, 0, 0), pygame.RLEACCEL)
        # SCREEN.blit(surf, (0, 0))
        pygame.display.flip()
        FRAME += 1
        TIME_PASSED_SECONDS = clock.tick(500)
        # print(clock.get_fps())
    pygame.quit()
