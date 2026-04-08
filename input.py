import pygame

direction = pygame.Vector2(0, 0)
def ReadDirection(event):
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_w):
            direction.y = 1
        elif (event.key == pygame.K_s):
            direction.y = -1
        if (event.key == pygame.K_a):
            direction.x = 1
        elif (event.key == pygame.K_d):
            direction.x = -1
            
    if (event.type == pygame.KEYUP):
        if (event.key == pygame.K_w):
            direction.y = 0
        elif (event.key == pygame.K_s):
            direction.y = 0
        if (event.key == pygame.K_a):
            direction.x = 0
        elif (event.key == pygame.K_d):
            direction.x = 0
    
    return direction