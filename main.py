import pygame
from typing import List, Tuple
import rendering
import input
import pygame_gui
from nodes import NodeType

windowDimensions = (1280, 720)

pygame.init()
pygame.display.set_caption("Linc Up")
running = True

screen = pygame.display.set_mode(windowDimensions, pygame.RESIZABLE)
clock = pygame.time.Clock()

# GUI
guimanager = pygame_gui.UIManager(windowDimensions, "theme.json")
typeList: List[str | Tuple[str, str]] = [t.name for t in NodeType]
selectedType: NodeType = NodeType.EMPTY
brushSize: int = 1

renderer = rendering.renderer(screen)
boundSet = False

camSpeed = 0.2
scrollFactor = 0.05
inputDirection = pygame.Vector2(0, 0)

# GUI elements
guiPanel = pygame.Rect(0, 0, 220, 500)
panel = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(0, 0, 220, 500),
    manager=guimanager
)

boundHeading = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 20, 200, 30),
    text='Create Bounds',
    manager=guimanager
)

widthInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 50, 200, 30),
    placeholder_text="width...",
    manager=guimanager
)

heightInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 90, 200, 30),
    placeholder_text="height...",
    manager=guimanager
)

applyBoundsButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 120, 200, 30),
    text="Apply",
    manager=guimanager
)

brushHeading = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 170, 200, 30),
    text='Set Brush',
    manager=guimanager
)

brushSizeBar = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 200, 160, 30),
    start_value=1,
    value_range=(1, 10),
    manager=guimanager
)

brushSizeDisplay = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(170, 200, 35, 30),
    text='1',
    manager=guimanager
)

nodeTypeDropdown = pygame_gui.elements.UIDropDownMenu(
    relative_rect=pygame.Rect(10, 240, 200, 30),
    options_list=typeList,
    starting_option=typeList[0]
)

enableGridRendering = pygame_gui.elements.UICheckBox(
    relative_rect=pygame.Rect(10, 420, 30, 30),
    text="Enable Grid Rendering",
    manager=guimanager
)
enableGridRendering.set_state(True)

submitButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 460, 200, 30),
    text="Submit",
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
        
        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == enableGridRendering:
                renderer.enableBgRendering = True
        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == enableGridRendering:
                renderer.enableBgRendering = False
                
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            selectedType = NodeType(typeList.index(event.text))
            
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == brushSizeBar:
                brushSize = round(event.value)
                brushSizeDisplay.set_text(str(brushSize))
        
        if event.type == pygame.MOUSEBUTTONUP:
            snappedVal = round(brushSizeBar.get_current_value())
            brushSizeBar.set_current_value(snappedVal)
            brushSize = snappedVal
                    
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == applyBoundsButton:
                try:
                    width, height = int(widthInput.get_text()), int(heightInput.get_text())
                    renderer.SetGrid(width, height)
                    boundSet = True
                except ValueError:
                    print("Invalid Input")
    
    if not guiPanel.collidepoint(pygame.mouse.get_pos()):
        if pygame.mouse.get_pressed()[0]:
            if boundSet:
                renderer.Draw(selectedType, brushSize)
        
        if scrollStatus:
            renderer.ZoomCamera(scrollStatus * scrollFactor * deltaTime)
        renderer.MoveCamera(renderer.camOffset + (inputDirection * camSpeed * deltaTime))    
    
    guimanager.update(deltaTime/1000)
    guimanager.draw_ui(screen)

    scrollStatus = None
    
    pygame.display.flip()
    
pygame.quit()