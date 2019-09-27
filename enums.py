from enum import Enum, auto


class BandCombination(Enum):
    GENERAL_LAND_COVER = auto()
    WATER = auto()
    EXPOSED_SOIL = auto()
    VEGETATION = auto()
    ROOFING_AND_ROADS = auto()
    ARTIFICIAL_FEATURES_IN_DESERT = auto()
    ARTIFICIAL_FEATURES_IN_VEGETATION = auto()
    UNDERWATER_OBSTRUCTION = auto()
    DIRECTION_OF_TRAVEL = auto()
    POLYMERS_PLASTICS = auto()
    SEEING_FIRE_THROUGH_SMOKE = auto()
    FIRES = auto()
    FIRES_AND_CHARRED_VEGETATION = auto()
    MINERALS = auto()
    SOIL_MOISTURE = auto()
    STANDING_WATER = auto()
    METAL = auto()


class BandTable(Enum):
    COASTAL = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 5
    RED_EDGE = 6
    NEAR_INFRARED_1 = 7
    NEAR_INFRARED_2 = 8
    SWIR_1 = 9
    SWIR_2 = 10
    SWIR_3 = 11
    SWIR_4 = 12
    SWIR_5 = 13
    SWIR_6 = 14
    SWIR_7 = 15
    SWIR_8 = 16
