# pygame.draw.line(surface, color, start_pos, end_pos, width=1)
import pygame

lines = list()

def render(screen):
    turned = False
    for i in range(5):
        for j in range(5):
            if turned:
                pygame.draw.line(screen, "black", (0, 0), (0, 0), width=1)
            else:
                pygame.draw.line(screen, "black", (0, 0), (0, 0), width=1)
        if i > 2:
            turned = True