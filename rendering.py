import pygame
from math import ceil
from nodes import Grid, NodeType

backgroundColor = pygame.Color("#f4c2c2")
minZoom, maxZoom = 5, 40
bgRenderThreshold: int = 10

# Node colors
emptyNodeCol = pygame.Color("#F5F5F5")
dirtNodeCol = pygame.Color("#724419")
pavementNodeCol = pygame.Color("#A19E8E")
roadNodeCol = pygame.Color("#1D1F27")

class renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        self.enableBgRendering: bool = True
        
        # Camera (do NOT directly change either of these values outside this class and use the respective functions instead)
        self.camOffset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.camZoom: float = 30
        
        self.grid: Grid
        self.__gridSet: bool = False
        
        self.Render()
        
    def Render(self):
        self.screen.fill(backgroundColor)
        if self.__gridSet:
            self.__RenderGrid()
        
        if self.camZoom > bgRenderThreshold and self.enableBgRendering:
            self.__RenderBackground()
        
    def MoveCamera(self, pos: pygame.Vector2):
        self.camOffset = pos
        self.Render()
        
    def ZoomCamera(self, dir: float):
        zoomLevel = self.camZoom + dir
        if zoomLevel > maxZoom:
            zoomLevel = maxZoom
        elif zoomLevel < minZoom:
            zoomLevel = minZoom
        
        self.camZoom = zoomLevel
        self.Render()
        
    def NodePosFromMouse(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        nodePos = ((mouseX-self.camOffset.x)//self.camZoom), ((mouseY-self.camOffset.y)//self.camZoom)
        return nodePos
    
    def Draw(self, selectedType: NodeType, size: int):
        centrePos = self.NodePosFromMouse()
        if size<1:
            return ValueError("Invalid brush size")
        if size==1:
            targetType = self.grid.nodes.get(centrePos, None)
            if centrePos and targetType != None and targetType != selectedType:
                self.grid.nodes[centrePos] = selectedType
            return
        drawNodes = self.grid.GetNeighbours(centrePos, size-1) | {centrePos}
        for pos in drawNodes.copy():
            targetType = self.grid.nodes.get(pos, None)
            if pos and targetType != None and targetType != selectedType:
                self.grid.nodes[pos] = selectedType

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
                if (x,y) not in self.grid.nodes:
                    continue
            
                xPos = round(x*self.camZoom + self.camOffset.x)
                yPos = round(y*self.camZoom + self.camOffset.y)
                size = ceil(self.camZoom)
                rect = pygame.Rect(xPos, yPos, size, size)
                
                match self.grid.nodes.get((x, y)):
                    case NodeType.EMPTY:
                        nodeCol = emptyNodeCol
                    case NodeType.DIRT:
                        nodeCol = dirtNodeCol
                    case NodeType.PAVEMENT:
                        nodeCol = pavementNodeCol
                    case NodeType.ROAD:
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