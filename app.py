import pygame
import rendering
from nodes import Grid, TerrainType, StructureType, Structure
from UIManager import UIManager
from input import Input
import pygame_gui
from enum import Enum

class Tool(Enum):
    TERRAIN = 1
    STRUCTURE = 2
    REMOVE_STRUCTURE = 3

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Linc Up")
        
        self.input: Input = Input()
        self.inputDirection = pygame.Vector2(0, 0)
        self.scrollStatus = None

        self.camSpeed = 200
        self.scrollFactor = 50

        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.ui: UIManager = UIManager((1280, 720))

        self.running: bool = True

        self.renderer: rendering.renderer = rendering.renderer(self.screen)

        self.boundSet: bool = False
        self.primaryGrid: Grid

        self.selectedTool: Tool = Tool.TERRAIN
        self.selectedTerrain: TerrainType = TerrainType.EMPTY
        self.selectedStructure: StructureType = StructureType.HOUSE

        self.firstStructurePoint: tuple[int, int] | None = None
        self.secondStructurePoint: tuple[int, int] | None = None

        self.brushSize = 1

    def HandleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.ui.process_event(event)

            scroll = self.input.ReadScroll(event)
            if scroll is not None:
                self.scrollStatus = scroll
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.firstStructurePoint = None
                    self.secondStructurePoint = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos()

                    if not self.ui.guiPanel.collidepoint(mousePos):
                        pos = self.renderer.NodePosFromScreen(mousePos)

                        if self.selectedTool == Tool.STRUCTURE and self.boundSet:
                            if pos in self.primaryGrid.terrain:
                                if not self.firstStructurePoint:
                                    self.firstStructurePoint = pos
                                else:
                                    self.secondStructurePoint = pos

                                    self.primaryGrid.CreateStructure(
                                        self.firstStructurePoint,
                                        self.secondStructurePoint,
                                        self.selectedStructure
                                    )

                                    self.firstStructurePoint = None
                                    self.secondStructurePoint = None

                        if self.selectedTool == Tool.REMOVE_STRUCTURE and self.boundSet:
                            node = self.primaryGrid.GetTopNode(pos)

                            if isinstance(node, Structure):
                                self.primaryGrid.structures = {
                                    k: v for k, v in self.primaryGrid.structures.items()
                                    if v.origin != node.origin
                                }
                                self.primaryGrid.lifeQualitySet = False
                                
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.ui.brushSizeBar:
                    self.brushSize = round(event.value)
                    self.ui.brushSizeDisplay.set_text(str(self.brushSize))
            
            if event.type == pygame.MOUSEBUTTONUP:
                snapped = round(self.ui.brushSizeBar.get_current_value())
                self.ui.brushSizeBar.set_current_value(snapped)
                self.brushSize = snapped
            
            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == self.ui.terrainTypeDropdown:
                    name = event.text
                    self.selectedTerrain = TerrainType[name]

                if event.ui_element == self.ui.structureTypeDropdown:
                    name = event.text
                    self.selectedStructure = StructureType[name]
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.ui.applyBoundsButton:
                    try:
                        w = int(self.ui.widthInput.get_text())
                        h = int(self.ui.heightInput.get_text())

                        self.primaryGrid = Grid(w, h, self.selectedTerrain)
                        self.renderer.SetGrid(self.primaryGrid)
                        self.boundSet = True
                    except:
                        print("Invalid input")

                if event.ui_element == self.ui.submitButton:
                    if self.boundSet:
                        self.primaryGrid.InitializeLivingQuality()
                        
                if event.ui_element == self.ui.terrainButton:
                    self.selectedTool = Tool.TERRAIN
                    self.ui.terrainButton.set_text("[X]")
                    self.ui.structureButton.set_text("[  ]")
                    self.ui.removeStructureButton.set_text("[  ]")
                    
                    self.firstStructurePoint = None
                    self.secondStructurePoint = None

                if event.ui_element == self.ui.structureButton:
                    self.selectedTool = Tool.STRUCTURE
                    self.ui.structureButton.set_text("[X]")
                    self.ui.terrainButton.set_text("[  ]")
                    self.ui.removeStructureButton.set_text("[  ]")
                    
                if event.ui_element == self.ui.removeStructureButton:
                    self.selectedTool = Tool.REMOVE_STRUCTURE
                    self.ui.removeStructureButton.set_text("[X]")
                    self.ui.terrainButton.set_text("[  ]")
                    self.ui.structureButton.set_text("[  ]")
                    self.firstStructurePoint = None
                    self.secondStructurePoint = None

    def Render(self):
        self.renderer.Render()
        self.ui.draw(self.screen)
        pygame.display.flip()

    def Run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            self.HandleEvents()
            self.ui.update(dt)
            
            self.inputDirection = self.input.ReadDirection()
            
            mousePos = pygame.mouse.get_pos()
            if not self.ui.guiPanel.collidepoint(mousePos):
                if self.scrollStatus:
                    self.renderer.ZoomCamera(self.scrollStatus * self.scrollFactor * dt)
                self.renderer.MoveCamera(
                    self.renderer.camOffset + (self.inputDirection * self.camSpeed * dt)
                )
                self.scrollStatus = None
                
                self.ui.manager.set_focus_set(None)
                
                clickedLMB = pygame.mouse.get_pressed()[0]
                if clickedLMB:
                    if self.boundSet and self.selectedTool == Tool.TERRAIN:
                        self.renderer.Draw(
                            self.selectedTerrain,
                            self.brushSize
                        )
                
                if self.firstStructurePoint and self.selectedTool == Tool.STRUCTURE:
                    mouseX, mouseY = self.renderer.NodePosFromScreen(mousePos)
                    selX, selY = self.firstStructurePoint

                    xSelPos = selX * self.renderer.camZoom + self.renderer.camOffset.x
                    ySelPos = selY * self.renderer.camZoom + self.renderer.camOffset.y

                    selWidth = (mouseX - selX) * self.renderer.camZoom
                    selHeight = (mouseY - selY) * self.renderer.camZoom

                    if selWidth < 0:
                        selWidth = -selWidth + self.renderer.camZoom
                        xSelPos -= selWidth
                        xSelPos += self.renderer.camZoom
                    else:
                        selWidth += self.renderer.camZoom

                    if selHeight < 0:
                        selHeight = -selHeight + self.renderer.camZoom
                        ySelPos -= selHeight
                        ySelPos += self.renderer.camZoom
                    else:
                        selHeight += self.renderer.camZoom

                    self.renderer.AddUIElement(
                        lambda: pygame.draw.rect(
                            self.screen,
                            self.renderer.GetColFromType(self.selectedStructure),
                            (xSelPos, ySelPos, selWidth, selHeight),
                            2
                        )
                    )
                    
                if self.boundSet and self.primaryGrid.lifeQualitySet:
                    x, y = self.renderer.NodePosFromScreen(mousePos)
                    if ((x, y) in self.primaryGrid.terrain):
                        topNode = self.primaryGrid.GetTopNode((x, y))
                        if isinstance(topNode, Structure):
                            if topNode.structureType in (StructureType.HOUSE, StructureType.APARTMENT):
                                for origin in self.primaryGrid.homes.keys():
                                    origin = topNode.origin
                                    quality = self.primaryGrid.lifeQualities.get(origin)

                                    if quality:
                                        self.renderer.ShowTooltip(
                                            self.primaryGrid.HomeQualityToString(quality)
                                        )
            
            self.Render()

        pygame.quit()