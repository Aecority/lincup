import pygame
import math
from nodes import Grid

backgroundColor = pygame.Color("#f4c2c2")
minZoom, maxZoom = 5, 40
bgRenderThreshold: int = 10

class renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        # Camera (do NOT directly change either of these values and use the respective functions instead)
        self.camOffset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.camZoom: float = 30
        
        self.grid: Grid
        self.__gridSet: bool = False
        
        self.Render()
        
    def Render(self):
        self.screen.fill(backgroundColor)
        if self.camZoom > bgRenderThreshold: self.__RenderBackground()
        
        if self.__gridSet: self.__RenderGrid()
        
    def MoveCamera(self, pos: pygame.Vector2):
        self.camOffset = pos
        self.Render()
        
    def ZoomCamera(self, dir: float):
        zoomLevel = self.camZoom + dir
        print(zoomLevel)
        if zoomLevel > maxZoom:
            zoomLevel = maxZoom
        elif zoomLevel < minZoom:
            zoomLevel = minZoom
        
        self.camZoom = zoomLevel
        self.Render()

    def WorldToScreenPoint(self, pos: pygame.Vector2):
        return pos + self.camOffset

    def ScreenToWorldPoint(self, pos: pygame.Vector2): # Unused currently, remove if unused after project completion
        return pos - self.camOffset
    
    def SetGrid(self, width, height):
        self.grid = Grid(width, height)
        self.__gridSet = True
        
    def __RenderGrid(self):
        for i in range(self.grid.height):
            for j in range(self.grid.width):
                rect = pygame.Rect(j*self.camZoom+self.camOffset.x, i*self.camZoom+self.camOffset.y, self.camZoom, self.camZoom)
                pygame.draw.rect(self.screen, "green", rect)
    
    def __RenderBackground(self):
        width, height = self.screen.get_size()
        horizontalCount = math.ceil(width/self.camZoom)+2
        verticalCount = math.ceil(height/self.camZoom)+2
        
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