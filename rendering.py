import pygame
import math

backgroundColor = pygame.Color("#bebebe")

class renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        
        # Camera
        self.camOffset: pygame.Vector2 = pygame.Vector2(0, 0)
        self.camZoom: int = 30
        
        self.render()
        
    def render(self):
        width, height = self.screen.get_size()
        self.screen.fill(backgroundColor)
        
        horizontalCount = math.ceil(width/self.camZoom)+2
        verticalCount = math.ceil(height/self.camZoom)+2
        
        localOffset = pygame.Vector2(
            self.camOffset.x % self.camZoom - self.camZoom*1.5,
            self.camOffset.y % self.camZoom - self.camZoom*1.5,
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
        
    def MoveCamera(self, pos: pygame.Vector2):
        self.camOffset = pos
        self.render()

    def WorldToScreenPoint(self, pos: pygame.Vector2):
        return pos + self.camOffset

    def ScreenToWorldPoint(self, pos: pygame.Vector2):
        return pos - self.camOffset