# python
import os
os.environ["SDL_VIDEODRIVER"] = "x11"
os.environ["SDL_RENDER_DRIVER"] = "software"
import pygame
pygame.init()
pygame.display.set_mode((640, 480))
pygame.time.wait(1000)
