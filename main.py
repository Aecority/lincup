import pygame
import rendering
import input

windowDimensions = (1280, 720)

pygame.init()
pygame.display.set_caption("Linc Up")
running = True

screen = pygame.display.set_mode(windowDimensions, pygame.RESIZABLE)
clock = pygame.time.Clock()

renderer = rendering.renderer(screen)

camSpeed = 0.2
inputDirection = pygame.Vector2(0, 0)

# Main app loop
while running:
    deltaTime = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        inputDirection = input.ReadDirection(event)
    
    renderer.MoveCamera(renderer.camOffset + (inputDirection * camSpeed * deltaTime))
    
    pygame.display.flip()
    
pygame.quit()