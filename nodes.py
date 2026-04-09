import pygame
from enum import Enum
from dataclasses import dataclass

class NodeType(Enum):
    EMPTY = 0
    DIRT = 1
    PAVEMENT = 2
    ROAD = 3
    
@dataclass
class Node():
    nodeType: NodeType
    position: pygame.Vector2
    
class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        self.nodes: list[Node] = [
            Node(nodeType=NodeType.EMPTY, position=pygame.Vector2(x, y))
            for y in range(height) for x in range(width)
        ]
        
    def GetNode(self, horizontal, vertical):
        return self.nodes[vertical * self.width + horizontal]