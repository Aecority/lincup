import pygame
from typing import List, Tuple
import rendering
import input
import pygame_gui
from nodes import TerrainType, StructureType, Structure

windowDimensions = (1280, 720)

pygame.init()
pygame.display.set_caption("Linc Up")
running = True

screen = pygame.display.set_mode(windowDimensions, pygame.RESIZABLE)
clock = pygame.time.Clock()

# GUI
guimanager = pygame_gui.UIManager(windowDimensions, "theme.json")
terrainList: List[str | Tuple[str, str]] = [t.name for t in TerrainType]
structureList: List[str | Tuple[str, str]] = [t.name for t in StructureType]
selectedTerrain: TerrainType = TerrainType.EMPTY
selectedStructure: StructureType = StructureType.HOUSE
brushSize: int = 1

structureSelected, terrainSelected, removeStructureSelected = False, False, False
# Structure placement
firstStructurePoint: tuple[int, int] | None = None
secondStructurePoint: tuple[int, int] | None = None

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
    container=panel,
    manager=guimanager
)

widthInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 50, 200, 30),
    placeholder_text="width...",
    container=panel,
    manager=guimanager
)

heightInput = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 90, 200, 30),
    placeholder_text="height...",
    container=panel,
    manager=guimanager
)

applyBoundsButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 120, 200, 30),
    text="Apply",
    container=panel,
    manager=guimanager
)

terrainButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 170, 30, 30),
    text='[  ]',
    manager=guimanager
)

brushHeading = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 170, 180, 30),
    text='Brush',
    container=panel,
    manager=guimanager
)

brushSizeBar = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect(10, 200, 160, 30),
    start_value=1,
    value_range=(1, 10),
    container=panel,
    manager=guimanager
)

brushSizeDisplay = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(170, 200, 35, 30),
    text='1',
    container=panel,
    manager=guimanager
)

structureButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 290, 30, 30),
    text='[  ]',
    manager=guimanager
)

structureHeading = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 290, 180, 30),
    text='Structures',
    container=panel,
    manager=guimanager
)

terrainTypeDropdown = pygame_gui.elements.UIDropDownMenu(
    relative_rect=pygame.Rect(10, 240, 180, 30),
    options_list=terrainList,
    container=panel,
    starting_option=terrainList[0]
)

structureTypeDropdown = pygame_gui.elements.UIDropDownMenu(
    relative_rect=pygame.Rect(10, 320, 180, 30),
    options_list=structureList,
    container=panel,
    starting_option=structureList[0]
)

removeStructureButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 370, 30, 30),
    text='[  ]',
    container=panel,
    manager=guimanager
)

removeStructureText = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(40, 370, 140, 30),
    text='Remove Structure',
    container=panel,
    manager=guimanager
)

enableGridRendering = pygame_gui.elements.UICheckBox(
    relative_rect=pygame.Rect(10, 420, 30, 30),
    text="Enable Grid Rendering",
    container=panel,
    manager=guimanager
)
enableGridRendering.set_state(True)

submitButton = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 460, 200, 30),
    text="Submit",
    container=panel,
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
        
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.ui_element == terrainTypeDropdown:
                selectedTerrain = TerrainType[event.text]
            if event.ui_element == structureTypeDropdown:
                selectedStructure = StructureType[event.text]
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not guiPanel.collidepoint(pygame.mouse.get_pos()):
                pos = renderer.NodePosFromScreen(pygame.mouse.get_pos())
                if structureSelected and boundSet:
                    if pos in renderer.grid.terrain:
                        if not firstStructurePoint:
                            firstStructurePoint = pos
                        elif not secondStructurePoint:
                            secondStructurePoint = pos
                            
                if removeStructureSelected and boundSet:
                    node = renderer.grid.GetTopNode(pos)
                    if type(node) == Structure:
                        renderer.grid.structures = {
                            k: v for k, v in renderer.grid.structures.items()
                            if v.origin != node.origin
                        }
        
        if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == enableGridRendering:
                renderer.enableBgRendering = True
        if event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == enableGridRendering:
                renderer.enableBgRendering = False
            
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
                    renderer.SetGrid(width, height, selectedTerrain)
                    boundSet = True
                except ValueError:
                    print("Invalid Input")
                    
            if event.ui_element == terrainButton:
                structureButton.set_text("[  ]")
                terrainButton.set_text("[X]")
                removeStructureButton.set_text("[  ]")
                terrainSelected = True
                structureSelected = False
                removeStructureSelected = False
                firstStructurePoint = None
                secondStructurePoint = None
            if event.ui_element == structureButton:
                structureButton.set_text("[X]")
                terrainButton.set_text("[  ]")
                removeStructureButton.set_text("[  ]")
                structureSelected = True
                terrainSelected = False
                removeStructureSelected = False
            if event.ui_element == removeStructureButton:
                structureButton.set_text("[  ]")
                terrainButton.set_text("[  ]")
                removeStructureButton.set_text("[X]")
                structureSelected = False
                terrainSelected = False
                removeStructureSelected = True
                firstStructurePoint = None
                secondStructurePoint = None
    
    if not guiPanel.collidepoint(pygame.mouse.get_pos()):
        guimanager.set_focus_set(None)
        if pygame.mouse.get_pressed()[0]:
            if boundSet and terrainSelected:
                    renderer.Draw(selectedTerrain, brushSize)
        if firstStructurePoint:
            if secondStructurePoint:
                renderer.grid.CreateStructure(firstStructurePoint, secondStructurePoint, selectedStructure)
                firstStructurePoint = None
                secondStructurePoint = None
            else:
                mouseX, mouseY = renderer.NodePosFromScreen(pygame.mouse.get_pos())
                selX, selY = firstStructurePoint
                xSelPos, ySelPos = selX*renderer.camZoom+renderer.camOffset.x, selY*renderer.camZoom+renderer.camOffset.y
                selWidth, selHeight = (mouseX - selX)*renderer.camZoom, (mouseY - selY)*renderer.camZoom
                if selWidth<0:
                    selWidth = -selWidth
                    xSelPos -= selWidth
                if selHeight<0:
                    selHeight = -selHeight
                    ySelPos -= selHeight
                    
                renderer.AddUIElement(lambda: pygame.draw.rect(screen, renderer.GetColFromType(selectedStructure), (xSelPos, ySelPos, selWidth, selHeight), 2))
                
    if scrollStatus:
        renderer.ZoomCamera(scrollStatus * scrollFactor * deltaTime)
    renderer.MoveCamera(renderer.camOffset + (inputDirection * camSpeed * deltaTime))
    
    renderer.Render()
    
    guimanager.update(deltaTime/1000)
    guimanager.draw_ui(screen)

    scrollStatus = None
    
    pygame.display.flip()
    
pygame.quit()