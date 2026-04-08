# pygame.draw.line(surface, color, start_pos, end_pos, width=1)
import pygame

lines = list()

scale = 10

def render(screen):
    turned = False
    width, height = screen.get_size()
    for i in range(scale):
        for j in range(1, scale):
            if turned:
                pygame.draw.line(screen, "black", ((width/scale)*j, 0), ((width/scale)*j, 1000), width=1)
            else:
                pygame.draw.line(screen, "black", (0, (height/scale)*j), (1000, (height/scale)*j), width=1)
        if i > 2:
            turned = True