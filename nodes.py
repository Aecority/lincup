from enum import Enum

# The type of node
class NodeType(Enum):
    EMPTY = 0
    DIRT = 1
    PAVEMENT = 2
    ROAD = 3
    
class Grid():
    def __init__(self, width, height):
        self.width: int = width
        self.height: int = height
        
        # Initialize grid of empty nodes
        self.nodes: dict[tuple, NodeType] = {
            (x, y): NodeType.EMPTY
            for x in range(width) for y in range(height)
        }

    def GetNeighbours(self, pos: tuple, step=1, found=[]):
        if (step < 1):
            raise RuntimeError
        if self.nodes.get(pos, None)==None:
            return set()
        
        neighbours: set[tuple[int, int]] = set()
        
        x, y = pos
        potentialNeighbours = {
                (x-1, y),
                (x+1, y),
                (x, y-1),
                (x, y+1)
        }
                
        if step == 1:
            return potentialNeighbours | neighbours
        elif step > 1:
            neighbours.update(potentialNeighbours)
            for n in potentialNeighbours:
                neighbours.update(self.GetNeighbours(n, step-1, found+[pos]))
                
        for n in neighbours.copy():
            if self.nodes.get(n, None)==None or n==pos:
                neighbours.remove(n)
        return neighbours