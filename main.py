import pygame
import rendering

windowDimensions = (1280, 720)
backgroundColor = pygame.Color("#bebebe")

pygame.init()
pygame.display.set_caption("Linc Up")
running = True

screen = pygame.display.set_mode(windowDimensions, pygame.RESIZABLE)
clock = pygame.time.Clock()

# Main app loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    deltaTime = clock.tick(60)
    screen.fill(backgroundColor)
    
    rendering.render(screen, 10)
    
    pygame.display.flip()
    
pygame.quit()