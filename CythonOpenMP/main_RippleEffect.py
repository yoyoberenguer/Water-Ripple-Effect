
# SOUND EFFECT FROM
# https://www.epidemicsound.com/track/gj8m0PURbn/

# COMPILATION
# python setup_RippleEffect.py build_ext --inplace

# INSTALLER
# pyinstaller --onefile main_rippleEffect.spec


try:
    import pygame
except ImportError:
    raise ImportError("\npygame library is missing on your system."
                      "\nTry: \n   C:\\pip inatall pygame on a window command prompt.")

from pygame.math import Vector2
from pygame.display import set_caption

import sys

try:
    import numpy
except ImportError:
    raise ImportError("\nnumpy library is missing on your system."
                      "\nTry: \n   C:\\pip install numpy on a window command prompt.")

from random import uniform, randint

try:
    from RippleEffect import new_, new__
except ImportError:
    raise ImportError("\n<RippleEffect> library is missing on your system or RippleEffect.pyx is not cynthonized."\
                      "\nTry: \n   C:\\python setup_RippleEffect.py build_ext --inplace")

if __name__ == '__main__':

    numpy.set_printoptions(threshold=sys.maxsize)

    height = 600
    width  = 600
    w2     = width // 2
    h2     = height // 2
    SCREENRECT = pygame.Rect(0, 0, width, height)
    pygame.display.init()
    SCREEN = pygame.display.set_mode(SCREENRECT.size)
    SCREEN.set_alpha(None)
    pygame.init()

    texture = pygame.image.load('background2.jpg').convert()
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
    # WaterDrop1   = pygame.mixer.Sound("ES_WaterDrip1.wav")
    WaterDrop2   = pygame.mixer.Sound("ES_WaterDrip2.wav")
    WaterDrop3   = pygame.mixer.Sound("ES_WaterDrip3.wav")
    WaterDrops   = [WaterDrop2, WaterDrop3]

    WaterSplash  = pygame.mixer.Sound("SplashSound.wav")
    WaterSplash1 = pygame.mixer.Sound("SplashSound1.wav")
    WaterSplash2 = pygame.mixer.Sound("SplashSound2.wav")
    Splashes = [WaterSplash1, WaterSplash2]
    old_mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

    ch = pygame.mixer.Channel(1)

    # TWEAKS
    screen_blit = SCREEN.blit
    clock_tick  = clock.tick
    cget_fps    = clock.get_fps
    event_pump  = pygame.event.pump
    event_get   = pygame.event.get
    get_key     = pygame.key.get_pressed
    get_pos     = pygame.mouse.get_pos
    flip        = pygame.display.flip

    while not STOP_GAME:

        set_caption("FPS %s " % round(cget_fps(), 2))

        event_pump()

        keys = get_key()

        for event in event_get():

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = Vector2(get_pos())

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
                        s = Splashes[randint(0, 1)]
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

        rnd = randint(0, 1000)

        if rnd > 995:
            drip_sound = WaterDrops[randint(0, 1)]
            drip_sound.set_volume(uniform(0.1, 0.8))
            drip_sound.play()
            previous[randint(0, width - 2), randint(0, height - 2)] = 8192

        previous, current, back_array = new_(height, width, previous, current, texture_array, back_array)

        screen_blit(pygame.surfarray.make_surface(back_array).convert(), (0, 0))

        flip()
        FRAME += 1
        TIME_PASSED_SECONDS = clock_tick(500)
        # print(clock.get_fps())
    pygame.quit()
