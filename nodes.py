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
    nearestSchool: int
    nearestBus: int
    hospitalDistanceFromBus: int
    schoolDistanceFromBus: int
    
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
        self.homes: dict[tuple[int, int], set[tuple[int, int]]] = {}
        self.buses: dict[tuple[int, int], set[tuple[int, int]]] = {}
        
        self.lifeQualitySet: bool = False
        self.lifeQualities: dict[tuple[int, int], HomeQuality] = {}

    def HomeQualityToReadable(self, hq: HomeQuality):
        tooltip: str = "Home Quality\n\n"
        
        tooltip += f"Nearest Hospital: {hq.nearestHospital}\n"
        tooltip += f"Nearest Bus: {hq.nearestBus}\n"
        tooltip += f"Nearest School: {hq.nearestSchool}\n\n"
        
        tooltip += f"Overall: {hq.quality}"
        
        return tooltip
    
    def CreateStructure(self, first: tuple[int, int], second: tuple[int, int], structureType: StructureType):
            xStart, xEnd = sorted((first[0], second[0]))
            yStart, yEnd = sorted((first[1], second[1]))
            
            for x in range(xStart, xEnd + 1):
                    for y in range(yStart, yEnd + 1):
                        if (x, y) in self.structures:
                            return
                        
            isHouse = structureType in (StructureType.HOUSE, StructureType.APARTMENT)
            houseEdges = set()
            
            isBus = structureType == StructureType.BUS
            busEdges = set()
            
            updatedValues = {}
            
            for x in range(xStart, xEnd + 1):
                for y in range(yStart, yEnd + 1):
                    isBoundary = (x in (xStart, xEnd) or y in (yStart, yEnd))
                    if isHouse and isBoundary:
                        houseEdges.add((x, y))
                    if isBus and isBoundary:
                        busEdges.add((x, y))
                    updatedValues[(x, y)] = Structure(origin=(xStart, yStart), structureType=structureType)
            self.structures.update(updatedValues)
            if isHouse:
                self.homes[(xStart, yStart)] = houseEdges
            if isBus:
                self.buses[(xStart, yStart)] = busEdges
            self.lifeQualitySet = False
    
    def RemoveStructure(self, pos: tuple[int, int]):
        node = self.structures.get(pos)

        if not node:
            return

        origin = node.origin
        stype = node.structureType

        self.structures = {
            k: v for k, v in self.structures.items()
            if v.origin != origin
        }

        if stype in (StructureType.HOUSE, StructureType.APARTMENT):
            self.homes.pop(origin, None)

        if stype is StructureType.BUS:
            self.buses.pop(origin, None)

        self.lifeQualitySet = False
    
    def GetTopNode(self, pos: tuple[int, int]):
        if pos in self.structures:
            return self.structures[pos]
        elif pos in self.terrain:
            return self.terrain[pos]
        return None
    
    def InitializeLivingQuality(self):
        for k, v in self.homes.items():
            hd, sd, bd, nbo = self.BreadthFirstSearch(v)
            hdb = -1
            sdb = -1
            if nbo != None:
                hdb, sdb, _, _ = self.BreadthFirstSearch(
                    self.buses[nbo]
                )
                
            # -- Quality Evaluation --
            # Write your code here
            # ------------------------
            
            homeQuality = HomeQuality(quality=0, nearestHospital=hd, nearestSchool=sd, nearestBus=bd, hospitalDistanceFromBus=hdb, schoolDistanceFromBus=sdb)
            self.lifeQualities[k] = homeQuality
        self.lifeQualitySet = True
    
    def BreadthFirstSearch(self, pos: set[tuple[int, int]]):
        frontier = deque(pos)
        visited = set(pos)
        
        distance = {start: 0 for start in pos}
        
        hospitalDistance = -1
        busDistance = -1
        schoolDistance = -1
        
        nearestBusOrigin: tuple[int, int] | None = None
        
        while frontier:
            current = frontier.popleft()
            for neighbour in self.__Neighbours(current):
                nextNode = self.GetTopNode(neighbour)
                
                if neighbour not in visited:
                    if nextNode in (TerrainType.PAVEMENT, TerrainType.ROAD):
                        frontier.append(neighbour)
                        distance[neighbour] = distance[current] + 1
                        visited.add(neighbour)
                    
                    if isinstance(nextNode, Structure):
                        match nextNode.structureType:
                            case StructureType.HOSPITAL:
                                if hospitalDistance == -1:
                                    hospitalDistance = distance[current]
                            case StructureType.BUS:
                                if busDistance == -1 :
                                    nearestBusOrigin = nextNode.origin
                                    busDistance = distance[current]
                            case StructureType.SCHOOL:
                                if schoolDistance == -1 :
                                    schoolDistance = distance[current]
                
                if hospitalDistance != -1 and busDistance != -1 and schoolDistance != -1:
                    return hospitalDistance, schoolDistance, busDistance, nearestBusOrigin
                    
        return hospitalDistance, schoolDistance, busDistance, nearestBusOrigin
    
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