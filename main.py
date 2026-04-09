import pygame
import rendering
import input
import pygame_gui

windowDimensions = (1280, 720)

pygame.init()
pygame.display.set_caption("Linc Up")
running = True

screen = pygame.display.set_mode(windowDimensions, pygame.RESIZABLE)
clock = pygame.time.Clock()

# GUI
guimanager = pygame_gui.UIManager(windowDimensions)

renderer = rendering.renderer(screen)

camSpeed = 0.2
scrollFactor = 0.05
inputDirection = pygame.Vector2(0, 0)

# GUI elements
panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(0, 0, 220, (screen.get_size()[1])),
    manager=guimanager
)

widthInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 10, 200, 30),
    placeholder_text="width...",
    manager=guimanager
)

heightInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 50, 200, 30),
    placeholder_text="height...",
    manager=guimanager
)

submitButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 90, 200, 30),
    text="Apply",
    manager=guimanager
)

# Main app loop
while running:
    deltaTime = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        guimanager.process_events(event)
        inputDirection = input.ReadDirection(event)
        scrollStatus = input.ReadScroll(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == submitButton:
                try:
                    width, height = int(widthInput.get_text()), int(heightInput.get_text())
                    renderer.SetGrid(width, height)
                except:
                    print("bro.")
    
    if scrollStatus:
        renderer.ZoomCamera(scrollStatus * scrollFactor * deltaTime)
    renderer.MoveCamera(renderer.camOffset + (inputDirection * camSpeed * deltaTime))    
    
    guimanager.update(deltaTime/1000)
    guimanager.draw_ui(screen)

    scrollStatus = None
    
    pygame.display.flip()
    
pygame.quit()