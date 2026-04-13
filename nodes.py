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
        
        # Create grid of empty nodes
        self.terrain: dict[tuple[int, int], TerrainType] = {
            (x, y): terrain
            for x in range(width) for y in range(height)
        }
        self.structures: dict[tuple[int, int], Structure] = {}
        self.homes: dict[tuple[int, int], list[tuple[int, int]]] = {}
        self.homepaths: dict[tuple[int, int], dict[tuple[int, int], tuple[int, int] | None]] = {}
    
    def CreateStructure(self, first: tuple[int, int], second: tuple[int, int], structureType: StructureType):
            xStart, xEnd = sorted((first[0], second[0]))
            yStart, yEnd = sorted((first[1], second[1]))
            
            for x in range(xStart, xEnd + 1):
                    for y in range(yStart, yEnd + 1):
                        if (x, y) in self.structures:
                            return
                        
            isHouse = structureType in (StructureType.HOUSE, StructureType.APARTMENT)
            houseEdges = []
            updatedValues = {}
                
            for x in range(xStart, xEnd + 1):
                for y in range(yStart, yEnd + 1):
                    if isHouse and (x in (xStart, xEnd) or y in (yStart, yEnd)):
                        houseEdges.append((x, y))
                    updatedValues[(x, y)] = Structure(origin=(xStart, yStart), structureType=structureType)
            self.structures.update(updatedValues)
            if isHouse:
                self.homes[(xStart, yStart)] = houseEdges
    
    def GetTopNode(self, pos: tuple[int, int]):
        if pos in self.structures:
            return self.structures[pos]
        elif pos in self.terrain:
            return self.terrain[pos]
        return None
    
    def BreadthFirstSearch(self, pos: list[tuple[int, int]]):
        frontier = pos
        flow: dict[tuple[int, int], tuple[int, int] | None] = dict()
        i = 0
        for startNode in frontier: # Start nodes don't flow from anywhere
            flow[startNode] = None
        
        while frontier:
            current = frontier.pop(0)
            for next in self.__Neighbours(current):
                nextNode = self.GetTopNode(next)
                if type(nextNode) == Structure:
                    nextNode = nextNode.structureType
                if next not in flow and nextNode and nextNode not in StructureType:
                    frontier.append(next)
                    flow[next] = current
                    i += 1
        return flow
    
    def __Neighbours(self, node: tuple[int, int]):
        x, y = node
        neighbours = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1)
        ]
        return neighbours