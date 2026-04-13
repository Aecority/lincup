from enum import Enum
from dataclasses import dataclass

# The type of terrain node
class TerrainType(Enum):
    EMPTY = 0
    DIRT = 1
    PAVEMENT = 2
    ROAD = 3

# The type of structure node
class StructureType(Enum):
    HOUSE = 1
    APARTMENT = 2
    HOSPITAL = 3
    SCHOOL = 4
    BUS = 5

@dataclass
class Structure():
    origin: tuple[int, int]
    structureType: StructureType
    
class Grid():
    def __init__(self, width: int, height: int, terrain: TerrainType):
        self.width: int = width
        self.height: int = height
        
        # Initialize grid of empty nodes
        self.terrain: dict[tuple[int, int], TerrainType] = {
            (x, y): terrain
            for x in range(width) for y in range(height)
        }
        
        self.structures: dict[tuple[int, int], Structure] = {}
    
    def CreateStructure(self, first: tuple[int, int], second: tuple[int, int], structureType: StructureType):
            xStart, xEnd = sorted((first[0], second[0]))
            yStart, yEnd = sorted((first[1], second[1]))
            updatedValues = {}
            for x in range(xStart, xEnd + 1):
                for y in range(yStart, yEnd + 1):
                    if self.structures.get((x, y), None):
                        return
                    updatedValues[(x, y)] = Structure(origin=(first), structureType=structureType)
            self.structures.update(updatedValues)
    
    def GetTopNode(self, pos: tuple[int, int]):
        if pos in self.structures:
            return self.structures[pos]
        elif pos in self.terrain:
            return self.terrain[pos]
        return None
    
    def BreadthFirstSearch(self, pos: list[tuple[int, int]]):
        frontier = pos
        flow = dict()
        
        for startNode in frontier: # Start nodes don't flow from anywhere
            flow[startNode] = None
        
        while not frontier:
            current = frontier[0]
            for next in __Neighbours(current):
                if next not in flow:
                    frontier.append(next)
                    flow[next] = current
        return flow
    
def __Neighbours(node: tuple[int, int]):
    x, y = node
    neighbours = [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1)
    ]
    return neighbours