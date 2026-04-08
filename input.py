import pygame

direction = pygame.Vector2(0, 0)
def ReadDirection(event):
    if (event.type == pygame.KEYDOWN):
        if (event.key == pygame.K_w or event.key == pygame.K_UP):
            direction.y = 1
        elif (event.key == pygame.K_s or event.key == pygame.K_DOWN):
            direction.y = -1
        if (event.key == pygame.K_a or event.key == pygame.K_LEFT):
            direction.x = 1
        elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
            direction.x = -1
            
    if (event.type == pygame.KEYUP):
        if (event.key == pygame.K_w or event.key == pygame.K_UP):
            direction.y = 0
        elif (event.key == pygame.K_s or event.key == pygame.K_DOWN):
            direction.y = 0
        if (event.key == pygame.K_a or event.key == pygame.K_LEFT):
            direction.x = 0
        elif (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
            direction.x = 0
    
    return direction