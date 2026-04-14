import pygame

class Input:
    def __init__(self):
        self.direction = pygame.Vector2(0, 0)
        self.scroll = 0

    def ReadDirection(self):
        keys = pygame.key.get_pressed()

        self.direction.x = (keys[pygame.K_a] or keys[pygame.K_LEFT]) - (keys[pygame.K_d] or keys[pygame.K_RIGHT])
        self.direction.y = (keys[pygame.K_w] or keys[pygame.K_UP]) - (keys[pygame.K_s] or keys[pygame.K_DOWN])

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        return self.direction

    def ReadScroll(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll = event.y
            return self.scroll
        return None