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

    def GetNeighbours(self, pos: tuple, step=1):
        if (step < 1):
            raise RuntimeError
        if self.nodes.get(pos, None)==None:
            return []
        
        neighbours: list[tuple[int, int]] = [pos]
        
        x, y = pos
        potentialNeighbours = [
                (x-1, y),
                (x+1, y),
                (x, y-1),
                (x, y+1)
            ]
        for n in potentialNeighbours:
            if self.nodes.get(n, None)==None:
                potentialNeighbours.remove(n)
                
        if step == 1:
            return potentialNeighbours+neighbours
        elif step > 1:
            neighbours.extend(potentialNeighbours)
            for n in potentialNeighbours:
                neighbours.extend(self.GetNeighbours(n, step-1))
        return neighbours