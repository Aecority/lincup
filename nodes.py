import pygame
from enum import Enum

class NodeType(Enum):
    EMPTY = 0
    DIRT = 1
    PAVEMENT = 2
    ROAD = 3
    
class Grid():
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        
        self.nodes: dict[tuple, NodeType] = {
            (x, y): NodeType.EMPTY
            for x in range(width) for y in range(height)
        }
        
    def GetNode(self, horizontal, vertical):
        return self.nodes[vertical * self.width + horizontal]