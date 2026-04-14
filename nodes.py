from enum import Enum
from dataclasses import dataclass
from collections import deque

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
    BUS = 4
    SCHOOL = 5

@dataclass
class Structure():
    origin: tuple[int, int]
    structureType: StructureType

@dataclass
class HomeQuality():
    quality: int
    nearestHospital: int
    nearestBus: int
    nearestSchool: int
    
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
        self.lifeQualities: dict[tuple[int, int], HomeQuality] = {}
    
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
    
    def InitializeLivingQuality(self):
        for k, v in self.homes.items():
            hd, bd, sd = self.BreadthFirstSearch(v)
            homeQuality = HomeQuality(quality=0, nearestHospital=hd, nearestBus=bd, nearestSchool=sd)
            self.lifeQualities[k] = homeQuality
        print(self.lifeQualities)
    
    def OriginDistance(self, start: tuple[int, int], map: dict[tuple[int, int], tuple[int, int] | None]):
        current = start
        distance = 0
        while(current != None):
            current = map[current]
            distance += 1
        return distance
    
    def BreadthFirstSearch(self, pos: list[tuple[int, int]]):
        frontier = deque(pos)
        visited = set(pos)
        
        distance = {start: 0 for start in pos}
        
        hospitalDistance = -1
        busDistance = -1
        schoolDistance = -1
        
        while frontier:
            current = frontier.popleft()
            for neighbour in self.__Neighbours(current):
                nextNode = self.GetTopNode(neighbour)
                nextNode = nextNode.structureType if isinstance(nextNode, Structure) else nextNode
                
                if neighbour not in visited and nextNode in (TerrainType.PAVEMENT, TerrainType.ROAD):
                    frontier.append(neighbour)
                    distance[neighbour] = distance[current] + 1
                    visited.add(neighbour)
                
                if neighbour not in visited:
                    match nextNode:
                        case StructureType.HOSPITAL:
                            if hospitalDistance == -1:
                                hospitalDistance = distance[current] + 1
                        case StructureType.BUS:
                            if busDistance == -1 :
                                busDistance = distance[current] + 1
                        case StructureType.SCHOOL:
                            if schoolDistance == -1 :
                                schoolDistance = distance[current] + 1
                
                if hospitalDistance != -1 and busDistance != -1 and schoolDistance != -1: return hospitalDistance, busDistance, schoolDistance
                    
        return hospitalDistance, busDistance, schoolDistance
    
    def __Neighbours(self, node: tuple[int, int]):
        x, y = node
        neighbours = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1)
        ]
        neighbours = {
            (x, y) for x, y in neighbours
            if 0 <= x < self.width and 0 <= y < self.height
        }
        
        return neighbours