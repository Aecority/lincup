import pygame
from math import ceil
from nodes import Grid, TerrainType, StructureType, Structure
from collections.abc import Callable

BACKGROUND_COLOR = pygame.Color("#f4c2c2")
MIN_ZOOM, MAX_ZOOM = 5, 40
BG_RENDER_THRESHOLD: int = 10

# Node colors -
 # Terrain
EMPTY_NODE_COL = pygame.Color("#F5F5F5")
DIRT_NODE_COL = pygame.Color("#724419")
PAVEMENT_NODE_COL = pygame.Color("#A19E8E")
ROAD_NODE_COL = pygame.Color("#1D1F27")
 
 # Structures
HOUSE_NODE_COL = pygame.Color("#FF7300")
APARTMENT_NODE_COL = pygame.Color("#00ff00")
HOSPITAL_NODE_COL = pygame.Color("#0000ff")
SCHOOL_NODE_COL = pygame.Color("#fff000")
BUS_NODE_COL = pygame.Color("#ff0000")

class renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        self.enableBgRendering: bool = True # Don't change this directly either
        
        # Camera (do NOT directly change either of these values outside this class and use the respective functions instead)
        self.camOffset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.camZoom: float = 30
        
        self.__grid: Grid
        self.__gridSet: bool = False
        self.overlayedUI: list[Callable] = []
        self.font = pygame.font.SysFont(None, 25)
        
        self.Render()
    
    def SetBackgroundVisibility(self, state: bool):
        self.enableBgRendering = state
    
    def Render(self):
        self.screen.fill(BACKGROUND_COLOR)
        if self.__gridSet:
            self.__RenderGrid()
        
        if self.camZoom > BG_RENDER_THRESHOLD and self.enableBgRendering:
            self.__RenderBackground()
        
        for ui in self.overlayedUI:
            ui()
        self.overlayedUI.clear()
        
    def MoveCamera(self, pos: pygame.Vector2):
        self.camOffset = pos
        
    def ZoomCamera(self, dir: float):
        zoomLevel = self.camZoom + dir
        if zoomLevel > MAX_ZOOM:
            zoomLevel = MAX_ZOOM
        elif zoomLevel < MIN_ZOOM:
            zoomLevel = MIN_ZOOM
        
        self.camZoom = zoomLevel
        
    def NodePosFromScreen(self, pos: tuple[int, int]):
        x, y = pos
        nodePos = int((x-self.camOffset.x)//self.camZoom), int((y-self.camOffset.y)//self.camZoom)
        return nodePos
    
    def SetStructure(self, first: tuple[int, int], second: tuple[int, int], structureType: StructureType):
        self.__grid.CreateStructure(first, second, structureType)
    
    def Draw(self, selectedType: TerrainType, size: int):
        mouseX, mouseY = self.NodePosFromScreen(pygame.mouse.get_pos())
        if size<1:
            return ValueError("Invalid brush size")
        
        terrainNodes = self.__grid.terrain
        radius = size-1
        
        startX, endX = mouseX-radius, mouseX+radius
        startY, endY = mouseY-radius, mouseY+radius
        
        if radius==0:
            pos = (mouseX, mouseY)
            targetType = terrainNodes.get(pos, None)
            if pos and targetType != None and targetType != selectedType:
                terrainNodes[pos] = selectedType
        else:
            for x in range(startX, endX+1):
                for y in range(startY, endY+1):
                    pos = (x, y)
                    targetType = terrainNodes.get(pos, None)
                    if pos and targetType != None and targetType != selectedType:
                        terrainNodes[pos] = selectedType
        self.__grid.lifeQualitySet = False

    def SetGrid(self, grid: Grid):
        self.__grid = grid
        self.__gridSet = True
    
    def AddUIElement(self, elem: Callable):
        self.overlayedUI.append(elem)
    
    def __RenderGrid(self):
        sWidth, sHeight = self.screen.get_size()
        
        startX, startY = int(-self.camOffset.x // self.camZoom), int(-self.camOffset.y // self.camZoom)
        endX, endY = startX+ceil(sWidth / self.camZoom)+2, startY+ceil(sHeight / self.camZoom)+2

        for x in range(startX, endX):
            for y in range(startY, endY):
                if (x,y) not in self.__grid.terrain:
                    continue
            
                xPos = round(x*self.camZoom + self.camOffset.x)
                yPos = round(y*self.camZoom + self.camOffset.y)
                size = ceil(self.camZoom)
                rect = pygame.Rect(xPos, yPos, size, size)
                
                node = self.__grid.GetTopNode((x, y))
                
                if node != None:
                    nodeCol = self.GetColFromType(node)
                    
                pygame.draw.rect(self.screen, nodeCol, rect)
    
    def GetColFromType(self, ntype: Structure | TerrainType | StructureType):
                if type(ntype) == Structure:
                    ntype = ntype.structureType
                if type(ntype) == StructureType:
                    match ntype:
                        case StructureType.HOUSE:
                            nodeCol = HOUSE_NODE_COL
                        case StructureType.APARTMENT:
                            nodeCol = APARTMENT_NODE_COL
                        case StructureType.HOSPITAL:
                            nodeCol = HOSPITAL_NODE_COL
                        case StructureType.SCHOOL:
                            nodeCol = SCHOOL_NODE_COL
                        case StructureType.BUS:
                            nodeCol = BUS_NODE_COL
                    
                else:
                    match ntype:
                        case TerrainType.EMPTY:
                            nodeCol = EMPTY_NODE_COL
                        case TerrainType.DIRT:
                            nodeCol = DIRT_NODE_COL
                        case TerrainType.PAVEMENT:
                            nodeCol = PAVEMENT_NODE_COL
                        case TerrainType.ROAD:
                            nodeCol = ROAD_NODE_COL
                return nodeCol
    
    def ShowTooltip(self, message):
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseX -= 2
        mouseY -= 2
        
        def draw_logic():
            font = self.font 
            FIXED_WIDTH = 200
            padding = 5
            line_spacing = 2
            
            final_lines = message.split("\n")
            rendered_lines = [font.render(line.strip(), True, (255, 255, 255)) for line in final_lines]
            
            rawHeight = sum(line.get_height() + line_spacing for line in rendered_lines) - line_spacing
            totalHeight = rawHeight + (padding * 2)
            
            tooltipBg = pygame.Rect(mouseX - FIXED_WIDTH, mouseY - totalHeight, FIXED_WIDTH, totalHeight)
            pygame.draw.rect(self.screen, (0, 0, 0), tooltipBg)
            
            currY = tooltipBg.top + padding
            for surf in rendered_lines:
                line_x_offset = (FIXED_WIDTH - surf.get_width()) // 2
                self.screen.blit(surf, (tooltipBg.left + line_x_offset, currY))
                currY += surf.get_height() + line_spacing

        self.AddUIElement(draw_logic)
    
    def __RenderBackground(self):
        width, height = self.screen.get_size()
        horizontalCount = ceil(width/self.camZoom)+2
        verticalCount = ceil(height/self.camZoom)+2
        
        localOffset = pygame.Vector2(
            self.camOffset.x % self.camZoom - self.camZoom,
            self.camOffset.y % self.camZoom - self.camZoom,
        )
        
        for x in range(horizontalCount):
            pygame.draw.line(self.screen,
                            "black",
                            pygame.Vector2(self.camZoom*x, 0)+localOffset,
                            pygame.Vector2(self.camZoom*x, verticalCount*self.camZoom)+localOffset,
                            width=1)

        for y in range(verticalCount):
            pygame.draw.line(self.screen,
                            "black",
                            pygame.Vector2(0, self.camZoom*y)+localOffset,
                            pygame.Vector2(self.camZoom*horizontalCount, self.camZoom*y)+localOffset,
                            width=1)