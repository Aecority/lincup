import pygame
from math import ceil
from nodes import Grid, TerrainType, StructureType, Structure

backgroundColor = pygame.Color("#f4c2c2")
minZoom, maxZoom = 5, 40
bgRenderThreshold: int = 10

# Node colors -
 # Terrain
emptyNodeCol = pygame.Color("#F5F5F5")
dirtNodeCol = pygame.Color("#724419")
pavementNodeCol = pygame.Color("#A19E8E")
roadNodeCol = pygame.Color("#1D1F27")
 
 # Structures
houseNodeCol = pygame.Color("#FF7300")
apartmentNodeCol = pygame.Color("#00ff00")
hospitalNodeCol = pygame.Color("#0000ff")
schoolNodeCol = pygame.Color("#fff000")
busNodeCol = pygame.Color("#ff0000")

class renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        self.enableBgRendering: bool = True # Don't change this directly either
        
        # Camera (do NOT directly change either of these values outside this class and use the respective functions instead)
        self.camOffset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.camZoom: float = 30
        
        self.grid: Grid
        self.__gridSet: bool = False
        
        self.Render()
    
    def SetBackgroundVisibility(self, state: bool):
        self.enableBgRendering = state
    
    def Render(self):
        self.screen.fill(backgroundColor)
        if self.__gridSet:
            self.__RenderGrid()
        
        if self.camZoom > bgRenderThreshold and self.enableBgRendering:
            self.__RenderBackground()
        
    def MoveCamera(self, pos: pygame.Vector2):
        self.camOffset = pos
        
    def ZoomCamera(self, dir: float):
        zoomLevel = self.camZoom + dir
        if zoomLevel > maxZoom:
            zoomLevel = maxZoom
        elif zoomLevel < minZoom:
            zoomLevel = minZoom
        
        self.camZoom = zoomLevel
        
    def NodePosFromScreen(self, pos: tuple[int, int]):
        x, y = pos
        nodePos = int((x-self.camOffset.x)//self.camZoom), int((y-self.camOffset.y)//self.camZoom)
        return nodePos
    
    def SetStructure(self, first: tuple[int, int], second: tuple[int, int], structureType: StructureType):
        self.grid.CreateStructure(first, second, structureType)
    
    def Draw(self, selectedType: TerrainType, size: int):
        mouseX, mouseY = self.NodePosFromScreen(pygame.mouse.get_pos())
        if size<1:
            return ValueError("Invalid brush size")
        
        terrainNodes = self.grid.terrain
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

    def SetGrid(self, width, height):
        self.grid = Grid(width, height)
        self.__gridSet = True
    
    def __RenderGrid(self):
        # Replace this with only rendering visible tiles later
        sWidth, sHeight = self.screen.get_size()
        
        startX, startY = int(-self.camOffset.x // self.camZoom), int(-self.camOffset.y // self.camZoom)
        endX, endY = startX+ceil(sWidth / self.camZoom)+2, startY+ceil(sHeight / self.camZoom)+2

        for x in range(startX, endX):
            for y in range(startY, endY):
                if (x,y) not in self.grid.terrain:
                    continue
            
                xPos = round(x*self.camZoom + self.camOffset.x)
                yPos = round(y*self.camZoom + self.camOffset.y)
                size = ceil(self.camZoom)
                rect = pygame.Rect(xPos, yPos, size, size)
                
                node = self.grid.GetTopNode((x, y))
                
                if type(node) == Structure:
                    stype = node.structureType
                    match stype:
                        case StructureType.HOUSE:
                            nodeCol = houseNodeCol
                        case StructureType.APARTMENT:
                            nodeCol = apartmentNodeCol
                        case StructureType.HOSPITAL:
                            nodeCol = hospitalNodeCol
                        case StructureType.SCHOOL:
                            nodeCol = schoolNodeCol
                        case StructureType.BUS:
                            nodeCol = busNodeCol
                    
                else:
                    match node:
                        case TerrainType.EMPTY:
                            nodeCol = emptyNodeCol
                        case TerrainType.DIRT:
                            nodeCol = dirtNodeCol
                        case TerrainType.PAVEMENT:
                            nodeCol = pavementNodeCol
                        case TerrainType.ROAD:
                            nodeCol = roadNodeCol
                    
                pygame.draw.rect(self.screen, nodeCol, rect)
    
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