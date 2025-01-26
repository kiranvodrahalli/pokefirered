import json
import random
import numpy as np

encounter_chart_path = "/Users/kiranv/home/code/pokefirered/src/data/wild_encounters_orig.json"

habitat_template_path = "/Users/kiranv/home/code/pokefirered/src/data/habitat_template.json"

randomized_encounters_path = "/Users/kiranv/home/code/pokefirered/src/data/wild_encounters.json"


# Pokemon Roster (Gen I and II, excluding legendaries, only base forms)
pokemon_roster = [
    "BULBASAUR", "CHARMANDER", "SQUIRTLE", "CATERPIE", "WEEDLE", "PIDGEY",
    "RATTATA", "SPEAROW", "EKANS", "SANDSHREW", "NIDORAN_F",
    "NIDORAN_M", "VULPIX", "ZUBAT", "ODDISH",
    "PARAS", "VENONAT", "DIGLETT", "MEOWTH", "PSYDUCK", "MANKEY",
    "GROWLITHE", "POLIWAG", "ABRA", "MACHOP", "BELLSPROUT", "TENTACOOL",
    "GEODUDE", "PONYTA", "SLOWPOKE", "MAGNEMITE", "FARFETCHD", "DODUO",
    "SEEL", "GRIMER", "SHELLDER", "GASTLY", "ONIX", "DROWZEE",
    "KRABBY", "VOLTORB", "EXEGGCUTE", "CUBONE",
    "LICKITUNG", "KOFFING", "RHYHORN", "CHANSEY", "TANGELA", "KANGASKHAN",
    "HORSEA", "GOLDEEN", "STARYU", "MR_MIME", "SCYTHER", "PINSIR", "TAUROS",
    "MAGIKARP", "LAPRAS", "DITTO", "EEVEE", "PORYGON", "OMANYTE", "KABUTO", "AERODACTYL",
    "SNORLAX", "DRATINI", "CHIKORITA", "CYNDAQUIL", "TOTODILE", "SENTRET",
    "HOOTHOOT", "LEDYBA", "SPINARAK", "CHINCHOU", "PICHU", "CLEFFA",
    "IGGLYBUFF", "TOGEPI", "NATU", "MAREEP", "MARILL", "SUDOWOODO", "HOPPIP", 
    "AIPOM", "SUNKERN", "YANMA", "WOOPER", "MURKROW",
    "MISDREAVUS", "UNOWN", "WOBBUFFET", "GIRAFARIG", "PINECO", "DUNSPARCE", 
    "GLIGAR", "SNUBBULL", "QWILFISH", "SHUCKLE", "HERACROSS", "SNEASEL", "TEDDIURSA",
    "SLUGMA", "SWINUB", "CORSOLA", "REMORAID", "DELIBIRD", "MANTINE", "SKARMORY",
    "HOUNDOUR", "PHANPY", "STANTLER", "SMEARGLE", "TYROGUE", "SMOOCHUM", "ELEKID",
    "MAGBY", "MILTANK", "LARVITAR",
]

# A dictionary of defined Pokemon habitats mapping to a list of possible Pokemon levels.
habitat_types = {
    "ForestEarly": {"range": (2, 7)},
    "ForestMid": {"range": (8, 18)},
    "ForestLate": {"range": (20, 35)},
    "ForestEdgeEarly": {"range": (2, 7)},
    "ForestEdgeMid": {"range": (8, 18)},
    "ForestEdgeLate": {"range": (20, 35)},
    "PlainsEarly": {"range": (2, 7)},
    "PlainsMid": {"range": (8, 18)},
    "PlainsLate": {"range": (20, 35)},
    "MeadowEarly": {"range": (3, 10)},
    "MeadowMid": {"range": (10, 20)},
    "MeadowLate": {"range": (20, 30)},
    "MountainFootEarly": {"range": (5, 12)},
    "MountainFootMid": {"range": (12, 20)},
    "MountainFootLate": {"range": (22, 35)},
    "MountainPeakEarly": {"range": (10, 20)},
    "MountainPeakMid": {"range": (20, 35)},
    "MountainPeakLate": {"range": (35, 50)},
    "CaveEntranceEarly": {"range": (5, 12)},
    "CaveEntranceMid": {"range": (12, 20)},
    "CaveEntranceLate": {"range": (20, 35)},
    "CaveDepthEarly": {"range": (7, 15)},
    "CaveDepthMid": {"range": (15, 25)},
    "CaveDepthLate": {"range": (25, 40)},
    "UndergroundLakeSurf": {"range": (20, 30)},
    "UndergroundLakeFish": {"range": (5, 35)},
    "CityOutskirtsEarly": {"range": (3, 10)},
    "CityOutskirtsMid": {"range": (10, 20)},
    "CityOutskirtsLate": {"range": (20, 30)},
    "ShallowSeaSurf": {"range": (5, 20)},
    "ShallowSeaFish": {"range": (5, 25)},
    "DeepSeaSurf": {"range": (20, 40)},
    "DeepSeaFish": {"range": (15, 35)},
    "RiverSurf": {"range": (10, 30)},
    "RiverFish": {"range": (5, 25)},
    "LakeSurf": {"range": (15, 30)},
    "LakeFish": {"range": (5, 35)},
    "VolcanicEarly": {"range": (24, 30)},
    "VolcanicMid": {"range": (30, 36)},
    "VolcanicLate": {"range": (38, 42)},
    "IcyEarly": {"range": (23, 30)},
    "IcyMid": {"range": (30, 40)},
    "IcyLate": {"range": (40, 53)},
    "RuinsEarly": {"range": (10, 18)},
    "RuinsMid": {"range": (18, 25)},
    "RuinsLate": {"range": (25, 35)},
    "MansionEarly": {"range": (18, 28)},
    "MansionMid": {"range": (28, 32)},
    "MansionLate": {"range": (32, 38)},
    "Safari1": {"range": (22, 33)},
    "Safari2": {"range": (22, 33)},
    "Safari3": {"range": (22, 33)},
    "Safari4": {"range": (22, 33)},
    "SafariSurf": {"range": (22, 33)},
    "SafariFish": {"range": (22, 33)},
    "PowerPlant": {"range": (22, 35)},
    "CeruleanCave": {"range": (46, 67)},
}

# A map from every Pokemon FireRed/LeafGreen map area to a dictionary of 
# different encounter types (land_mons, water_mons, fishing_mons, and rock_smash_mons).
# Note that rock_smash_mons are Pokemon that can be found by breaking open rocks.
# For each encounter type, we provide a list of possible Pokemon habitats to 
# sample from for randomization purposes.
# TODO(kiranv): Check that every single map location in wild_encounters.json
# is present as a key in this dictionary, with all encounter types mapped to a list
# of habitats from habitat_types.
encounter_mapping = {
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER": {
        "land_mons": ["RuinsLate"],
    },
    "MAP_VIRIDIAN_FOREST": {
        "land_mons": ["ForestEarly"],
    },
    "MAP_MT_MOON_1F": {
        "land_mons": ["CaveEntranceEarly", "MountainPeakEarly"],
    },
    "MAP_MT_MOON_B1F": {
        "land_mons": ["CaveDepthEarly"],
    },
    "MAP_MT_MOON_B2F": {
        "land_mons": ["CaveDepthEarly"],
    },
    "MAP_SSANNE_EXTERIOR": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_DIGLETTS_CAVE_B1F": {
        "land_mons": ["CaveDepthMid"],
    },
    "MAP_VICTORY_ROAD_1F": {
        "land_mons": ["CaveDepthLate", "MountainPeakLate"],
    },
    "MAP_VICTORY_ROAD_2F": {
        "land_mons": ["CaveDepthLate", "MountainPeakLate"],
    },
    "MAP_VICTORY_ROAD_3F": {
        "land_mons": ["CaveDepthLate", "MountainPeakLate"],
    },
    "MAP_POKEMON_MANSION_1F": {
        "land_mons": ["MansionEarly"],
    },
    "MAP_POKEMON_MANSION_2F": {
        "land_mons": ["MansionMid"],
    },
    "MAP_POKEMON_MANSION_3F": {
        "land_mons": ["MansionMid"],
    },
    "MAP_POKEMON_MANSION_B1F": {
        "land_mons": ["MansionLate"],
    },
    "MAP_SAFARI_ZONE_CENTER": {
        "land_mons": ["Safari4"],
        "water_mons": ["SafariSurf"],
        "fishing_mons": ["SafariFish"],
    },
    "MAP_SAFARI_ZONE_EAST": {
        "land_mons": ["Safari1"],
        "water_mons": ["SafariSurf"],
        "fishing_mons": ["SafariFish"],
    },
    "MAP_SAFARI_ZONE_NORTH": {
        "land_mons": ["Safari2"],
        "water_mons": ["SafariSurf"],
        "fishing_mons": ["SafariFish"],
    },
    "MAP_SAFARI_ZONE_WEST": {
        "land_mons": ["Safari3"],
        "water_mons": ["SafariSurf"],
        "fishing_mons": ["SafariFish"],
    },
    "MAP_CERULEAN_CAVE_1F": {
        "land_mons": ["CaveDepthLate", "CeruleanCave"],
        "water_mons": ["UndergroundLakeSurf"],
        "rock_smash_mons": ["CaveDepthLate"],
        "fishing_mons": ["UndergroundLakeFish"],
    },
    "MAP_CERULEAN_CAVE_2F": {
        "land_mons": ["CaveDepthLate", "CeruleanCave"],
        "rock_smash_mons": ["CaveDepthLate"],
    },
    "MAP_CERULEAN_CAVE_B1F": {
        "land_mons": ["CaveDepthLate", "CeruleanCave"],
        "water_mons": ["UndergroundLakeSurf"],
        "rock_smash_mons": ["CaveDepthLate"],
        "fishing_mons": ["UndergroundLakeFish"],
    },
    "MAP_ROCK_TUNNEL_1F": {
        "land_mons": ["CaveDepthMid", "MountainPeakMid"],
        "rock_smash_mons": ["CaveDepthMid"],
    },
    "MAP_ROCK_TUNNEL_B1F": {
        "land_mons": ["CaveDepthMid", "RuinsMid"],
        "rock_smash_mons": ["CaveDepthMid"],
    },
    "MAP_SEAFOAM_ISLANDS_1F": {
        "land_mons": ["IcyEarly"],
    },
    "MAP_SEAFOAM_ISLANDS_B1F": {
        "land_mons": ["IcyMid"],
    },
    "MAP_SEAFOAM_ISLANDS_B2F": {
        "land_mons": ["IcyMid"],
    },
    "MAP_SEAFOAM_ISLANDS_B3F": {
        "land_mons": ["IcyLate"],
        "water_mons": ["UndergroundLakeSurf"],
        "fishing_mons": ["UndergroundLakeFish"],
    },
    "MAP_SEAFOAM_ISLANDS_B4F": {
        "land_mons": ["IcyLate"],
        "water_mons": ["UndergroundLakeSurf"],
        "fishing_mons": ["UndergroundLakeFish"],
    },
    "MAP_POKEMON_TOWER_3F": {
        "land_mons": ["RuinsEarly"],
    },
    "MAP_POKEMON_TOWER_4F": {
        "land_mons": ["RuinsEarly"],
    },
    "MAP_POKEMON_TOWER_5F": {
        "land_mons": ["RuinsMid"],
    },
    "MAP_POKEMON_TOWER_6F": {
        "land_mons": ["RuinsMid"],
    },
    "MAP_POKEMON_TOWER_7F": {
        "land_mons": ["RuinsMid"],
    },
    "MAP_POWER_PLANT": {
        "land_mons": ["PowerPlant"],
    },
    "MAP_MT_EMBER_EXTERIOR": {
        "land_mons": ["VolcanicMid", "MountainFootMid", "MountainPeakMid"],
        "rock_smash_mons": ["VolcanicEarly"],
    },
    "MAP_MT_EMBER_SUMMIT_PATH_1F": {
        "land_mons": ["VolcanicMid", "MountainPeakMid"],
    },
    "MAP_MT_EMBER_SUMMIT_PATH_2F": {
        "land_mons": ["VolcanicMid", "MountainPeakMid"],
        "rock_smash_mons": ["VolcanicMid"],
    },
    "MAP_MT_EMBER_SUMMIT_PATH_3F": {
        "land_mons": ["VolcanicMid", "MountainPeakMid"],
    },
    "MAP_MT_EMBER_RUBY_PATH_1F": {
        "land_mons": ["VolcanicLate", "MountainPeakLate"],
        "rock_smash_mons": ["VolcanicLate"],
    },
    "MAP_MT_EMBER_RUBY_PATH_B1F": {
        "land_mons": ["VolcanicLate", "MountainPeakLate"],
        "rock_smash_mons": ["VolcanicLate"],
    },
    "MAP_MT_EMBER_RUBY_PATH_B2F": {
        "land_mons": ["VolcanicLate", "MountainPeakLate"],
        "rock_smash_mons": ["VolcanicLate"],
    },
    "MAP_MT_EMBER_RUBY_PATH_B3F": {
        "land_mons": ["VolcanicLate", "MountainPeakLate"],
        "rock_smash_mons": ["VolcanicLate"],
    },
    "MAP_MT_EMBER_RUBY_PATH_B1F_STAIRS": {
        "land_mons": ["VolcanicLate", "MountainPeakLate"],
        "rock_smash_mons": ["VolcanicLate"],
    },
    "MAP_MT_EMBER_RUBY_PATH_B2F_STAIRS": {
        "land_mons": ["VolcanicLate", "MountainPeakLate"],
        "rock_smash_mons": ["VolcanicLate"],
    },
    "MAP_THREE_ISLAND_BERRY_FOREST": {
        "land_mons": ["ForestLate"],
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE": {
        "land_mons": ["IcyLate"],
        "water_mons": ["UndergroundLakeSurf"],
        "fishing_mons": ["UndergroundLakeFish"],
    },
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F": {
        "land_mons": ["IcyEarly"],
    },
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F": {
        "land_mons": ["IcyMid"],
    },
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK": {
        "land_mons": ["IcyLate"],
        "water_mons": ["DeepSeaSurf"],
        "fishing_mons": ["DeepSeaFish"],
    },
    "MAP_SIX_ISLAND_PATTERN_BUSH": {
        "land_mons": ["ForestEdgeMid"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM1": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM2": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM3": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM4": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM5": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM6": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM7": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM8": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM9": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM10": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM11": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM12": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM13": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM14": {
        "land_mons": ["CaveDepthLate"],
    },
    "MAP_ONE_ISLAND_KINDLE_ROAD": {
        "land_mons": ["PlainsLate", "MountainFootLate"],
        "water_mons": ["ShallowSeaSurf"],
        "rock_smash_mons": ["MountainFootLate"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ONE_ISLAND_TREASURE_BEACH": {
        "land_mons": ["PlainsLate", "MeadowLate"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_TWO_ISLAND_CAPE_BRINK": {
        "land_mons": ["MeadowLate"],
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_THREE_ISLAND_BOND_BRIDGE": {
        "land_mons": ["MeadowLate"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_THREE_ISLAND_PORT": {
        "land_mons": ["MeadowLate"],
    },
    "MAP_FIVE_ISLAND_RESORT_GORGEOUS": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_FIVE_ISLAND_WATER_LABYRINTH": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_FIVE_ISLAND_MEADOW": {
        "land_mons": ["MeadowLate"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_FIVE_ISLAND_MEMORIAL_PILLAR": {
        "land_mons": ["MeadowEarly"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_SIX_ISLAND_OUTCAST_ISLAND": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_SIX_ISLAND_GREEN_PATH": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_SIX_ISLAND_WATER_PATH": {
        "land_mons": ["MeadowLate"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_SIX_ISLAND_RUIN_VALLEY": {
        "land_mons": ["RuinsMid"],
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_SEVEN_ISLAND_TRAINER_TOWER": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE": {
        "land_mons": ["MountainFootLate"],
    },
    "MAP_SEVEN_ISLAND_SEVAULT_CANYON": {
        "land_mons": ["MountainPeakLate"],
        "rock_smash_mons": ["MountainPeakLate"],
    },
    "MAP_SEVEN_ISLAND_TANOBY_RUINS": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ROUTE1": {
        "land_mons": ["PlainsEarly", "CityOutskirtsEarly"],
    },
    "MAP_ROUTE2": {
        "land_mons": ["ForestEdgeEarly", "CityOutskirtsEarly"],
    },
    "MAP_ROUTE3": {
        "land_mons": ["PlainsEarly", "CityOutskirtsEarly", "MountainFootEarly"],
    },
    "MAP_ROUTE4": {
        "land_mons": ["MountainFootEarly"],
        "water_mons": ["RiverSurf"],
        "fishing_mons": ["RiverFish"],
    },
    "MAP_ROUTE5": {
        "land_mons": ["MeadowEarly", "PlainsMid", "CityOutskirtsEarly"],
    },
    "MAP_ROUTE6": {
        "land_mons": ["MeadowEarly", "PlainsMid", "CityOutskirtsMid"],
        "water_mons": ["RiverSurf"],
        "fishing_mons": ["RiverFish"],
    },
    "MAP_ROUTE7": {
        "land_mons": ["CityOutskirtsMid", "MeadowMid"],
    },
    "MAP_ROUTE8": {
        "land_mons": ["CityOutskirtsMid", "MeadowMid", "RuinsEarly"],
    },
    "MAP_ROUTE9": {
        "land_mons": ["MountainFootEarly", "PlainsMid"],
    },
    "MAP_ROUTE10": {
        "land_mons": ["MountainFootEarly", "RuinsEarly"],
        "water_mons": ["RiverSurf"],
        "fishing_mons": ["RiverFish"],
    },
    "MAP_ROUTE11": {
        "land_mons": ["MeadowMid", "PlainsMid", "CityOutskirtsMid"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ROUTE12": {
        "land_mons": ["MeadowMid"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ROUTE13": {
        "land_mons": ["MeadowMid", "PlainsMid"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ROUTE14": {
        "land_mons": ["MeadowMid", "PlainsMid"],
    },
    "MAP_ROUTE15": {
        "land_mons": ["PlainsMid", "CityOutskirtsMid"],
    },
    "MAP_ROUTE16": {
        "land_mons": ["PlainsMid", "CityOutskirtsMid"],
    },
    "MAP_ROUTE17": {
        "land_mons": ["PlainsMid"],
    },
    "MAP_ROUTE18": {
        "land_mons": ["PlainsMid", "MeadowMid"],
    },
    "MAP_ROUTE19": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ROUTE20": {
        "water_mons": ["DeepSeaSurf"],
        "fishing_mons": ["DeepSeaFish"],
    },
    "MAP_ROUTE21_NORTH": {
        "land_mons": ["MeadowLate", "CityOutskirtsLate"],
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ROUTE21_SOUTH": {
        "land_mons": ["PlainsLate"],
        "water_mons": ["DeepSeaSurf"],
        "fishing_mons": ["DeepSeaFish"],
    },
    "MAP_ROUTE22": {
        "land_mons": ["PlainsEarly"],
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_ROUTE23": {
        "land_mons": ["CaveEntranceLate", "MountainFootLate"],
        "water_mons": ["RiverSurf"],
        "fishing_mons": ["RiverFish"],
    },
    "MAP_ROUTE24": {
        "land_mons": ["ForestEdgeMid", "MeadowEarly"],
        "water_mons": ["RiverSurf"],
        "fishing_mons": ["RiverFish"],
    },
    "MAP_ROUTE25": {
        "land_mons": ["ForestEdgeMid", "MeadowEarly"],
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_PALLET_TOWN": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_VIRIDIAN_CITY": {
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_CERULEAN_CITY": {
        "water_mons": ["RiverSurf"],
        "fishing_mons": ["RiverFish"],
    },
    "MAP_VERMILION_CITY": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_CELADON_CITY": {
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_FUCHSIA_CITY": {
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_CINNABAR_ISLAND": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_ONE_ISLAND": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_FOUR_ISLAND": {
        "water_mons": ["LakeSurf"],
        "fishing_mons": ["LakeFish"],
    },
    "MAP_FIVE_ISLAND": {
        "water_mons": ["ShallowSeaSurf"],
        "fishing_mons": ["ShallowSeaFish"],
    },
    "MAP_SIX_ISLAND_ALTERING_CAVE": {
        "land_mons": ["CaveDepthLate"],
    },
}



def generate_habitat_template(original_encounters_file=encounter_chart_path, output_template_file=habitat_template_path):
    """
    Generates a habitat template JSON file from the original encounter data.

    Args:
        original_encounters_file: Path to the wild_encounters_orig.json file.
        output_template_file: Path to save the new habitat template JSON file.
    """

    with open(original_encounters_file, 'r') as f:
        data = json.load(f)

    # Simplify the structure
    for group in data["wild_encounter_groups"]:
        for encounter in group["encounters"]:
            for key in ['land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons']:
                if key in encounter:
                    # Assign a random habitat type based on the map and key.
                    map_name = encounter['map']
                    # List of relevant habitats.
                    relevant_habitats = encounter_mapping[map_name][key]
                    min_level = min(habitat_types[curr_habitat]['range'][0] for curr_habitat in relevant_habitats)
                    max_level = max(habitat_types[curr_habitat]['range'][1] for curr_habitat in relevant_habitats)
                    encounter[key] = {
                        "habitat_types": relevant_habitats,
                        "encounter_rate": encounter[key]["encounter_rate"],
                        "min_level": min_level,
                        "max_level": max_level
                    }

    with open(output_template_file, 'w') as f:
        json.dump(data, f, indent=2)

# TODO(kiranv): Add rock smash mons?
# Keeping:
# 1. Forest
# 2. ForestEdge
# 3. Plains
# 4. Meadow
# 5. MountainFoot
# 6. MountainPeak
# 7. CaveEntrance
# 8. CaveDepth
# 9. UndergroundLake {Surf/Fish}
# 10. CityOutskirts
# 11. ShallowSea {Surf/Fish}
# 12. DeepSea {Surf/Fish}
# 13. River {Surf/Fish}
# 14. Lake {Surf/Fish}
# 15. Volcanic
# 16. Icy
# 17. Ruins
# 18. Mansion
# 19. Safari {1/2/3/4}
# 20. Safari {Surf/Fish}
# 21. PowerPlant
# 22. CeruleanCave
habitat_mapping = {
    "ForestEarly": {
        "species": {
            "CATERPIE": 4,
            "WEEDLE": 4,
            "LEDYBA": 4,
            "SPINARAK": 4,
            "PIDGEY": 3,
            "HOOTHOOT": 3,
            "RATTATA": 3,
            "SENTRET": 3,
            "NATU": 2,
            "EKANS": 2,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "PARAS": 2,
            "VENONAT": 2,
            "GASTLY": 2,
            "EXEGGCUTE": 2,
            "TANGELA": 2,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "HOPPIP": 2,
            "SUNKERN": 2,
            "BULBASAUR": 2,
            "CHIKORITA": 2,
            "PINECO": 2,
            "SNUBBULL": 2,
            "YANMA": 2,
            "AIPOM": 2,
            "TEDDIURSA": 2,
            "SUDOWOODO": 2,
            "MISDREAVUS": 2,
            "MURKROW": 2,
            "ABRA": 2,
            "MAREEP": 2,
            "MARILL": 2,
            "FARFETCHD": 2,
            "DROWZEE": 2,
            "STANTLER": 2,
            "SMEARGLE": 2,
            "PHANPY": 2,
            "ELEKID": 2,
            "GROWLITHE": 2,
            "PINSIR": 1,
            "SCYTHER": 1,
            "HERACROSS": 1,
            "GIRAFARIG": 1,
            "SHUCKLE": 1,
            "SNORLAX": 1,
            "CHANSEY": 1,
            "KANGASKHAN": 1,
            "CHARMANDER": 1,
            "SQUIRTLE": 1,
            "CYNDAQUIL": 1,
            "TOTODILE": 1,
        },
    },
    "ForestMid": {
        "species": {
            "CATERPIE": 2,
            "WEEDLE": 2,
            "LEDYBA": 2,
            "SPINARAK": 2,
            "PIDGEY": 2,
            "HOOTHOOT": 2,
            "RATTATA": 2,
            "SENTRET": 2,
            "NATU": 2,
            "EKANS": 2,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "PARAS": 2,
            "VENONAT": 2,
            "GASTLY": 3,
            "EXEGGCUTE": 3,
            "TANGELA": 3,
            "EEVEE": 3,
            "PICHU": 3,
            "TOGEPI": 3,
            "HOPPIP": 3,
            "SUNKERN": 3,
            "BULBASAUR": 2,
            "CHIKORITA": 2,
            "PINECO": 3,
            "SNUBBULL": 2,
            "YANMA": 3,
            "AIPOM": 3,
            "TEDDIURSA": 3,
            "SUDOWOODO": 3,
            "MISDREAVUS": 3,
            "MURKROW": 3,
            "ABRA": 3,
            "MAREEP": 2,
            "MARILL": 2,
            "FARFETCHD": 3,
            "DROWZEE": 3,
            "STANTLER": 3,
            "SMEARGLE": 3,
            "PHANPY": 3,
            "ELEKID": 3,
            "GROWLITHE": 2,
            "PINSIR": 2,
            "SCYTHER": 2,
            "HERACROSS": 2,
            "GIRAFARIG": 2,
            "SHUCKLE": 2,
            "SNORLAX": 2,
            "CHANSEY": 2,
            "KANGASKHAN": 2,
            "CHARMANDER": 1,
            "SQUIRTLE": 1,
            "CYNDAQUIL": 1,
            "TOTODILE": 1,
        },
    },
    "ForestLate": {
        "species": {
            "CATERPIE": 1,
            "WEEDLE": 1,
            "LEDYBA": 1,
            "SPINARAK": 1,
            "PIDGEY": 1,
            "HOOTHOOT": 1,
            "RATTATA": 1,
            "SENTRET": 1,
            "NATU": 2,
            "EKANS": 2,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "PARAS": 2,
            "VENONAT": 2,
            "GASTLY": 3,
            "EXEGGCUTE": 3,
            "TANGELA": 3,
            "EEVEE": 3,
            "PICHU": 3,
            "TOGEPI": 3,
            "HOPPIP": 3,
            "SUNKERN": 3,
            "BULBASAUR": 2,
            "CHIKORITA": 2,
            "PINECO": 3,
            "SNUBBULL": 2,
            "YANMA": 3,
            "AIPOM": 3,
            "TEDDIURSA": 3,
            "SUDOWOODO": 3,
            "MISDREAVUS": 3,
            "MURKROW": 3,
            "ABRA": 3,
            "MAREEP": 2,
            "MARILL": 2,
            "FARFETCHD": 3,
            "DROWZEE": 3,
            "STANTLER": 3,
            "SMEARGLE": 3,
            "PHANPY": 3,
            "ELEKID": 3,
            "GROWLITHE": 2,
            "PINSIR": 4,
            "SCYTHER": 4,
            "HERACROSS": 4,
            "GIRAFARIG": 4,
            "SHUCKLE": 4,
            "SNORLAX": 4,
            "CHANSEY": 4,
            "KANGASKHAN": 4,
            "CHARMANDER": 1,
            "SQUIRTLE": 1,
            "CYNDAQUIL": 1,
            "TOTODILE": 1,
        },
    },
    "ForestEdgeEarly": {
        "species": {
            "CATERPIE": 2,
            "WEEDLE": 2,
            "LEDYBA": 2,
            "SPINARAK": 2,
            "PIDGEY": 2,
            "HOOTHOOT": 2,
            "SPEAROW": 2,
            "RATTATA": 2,
            "MEOWTH": 2,
            "SENTRET": 2,
            "EKANS": 3,
            "NIDORAN_F": 3,
            "NIDORAN_M": 3,
            "ODDISH": 3,
            "BELLSPROUT": 3,
            "PARAS": 3,
            "VENONAT": 3,
            "TANGELA": 2,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "HOPPIP": 2,
            "SUNKERN": 2,
            "BULBASAUR": 3,
            "CHIKORITA": 3,
            "SNUBBULL": 2,
            "YANMA": 2,
            "MURKROW": 2,
            "HOUNDOUR": 2,
            "ABRA": 2,
            "MAREEP": 2,
            "MARILL": 2,
            "FARFETCHD": 2,
            "DROWZEE": 2,
            "STANTLER": 2,
            "SMEARGLE": 2,
            "PHANPY": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "GROWLITHE": 2,
            "GIRAFARIG": 1,
            "CHARMANDER": 2,
            "SQUIRTLE": 2,
            "CYNDAQUIL": 2,
            "TOTODILE": 2,
            "MR_MIME": 2,
        },
    },
    "ForestEdgeMid": {
        "species": {
            "CATERPIE": 2,
            "WEEDLE": 2,
            "LEDYBA": 2,
            "SPINARAK": 2,
            "PIDGEY": 2,
            "HOOTHOOT": 2,
            "SPEAROW": 2,
            "RATTATA": 2,
            "MEOWTH": 2,
            "SENTRET": 2,
            "EKANS": 3,
            "NIDORAN_F": 4,
            "NIDORAN_M": 4,
            "ODDISH": 4,
            "BELLSPROUT": 4,
            "PARAS": 3,
            "VENONAT": 3,
            "TANGELA": 4,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "HOPPIP": 2,
            "SUNKERN": 2,
            "BULBASAUR": 4,
            "CHIKORITA": 4,
            "SNUBBULL": 2,
            "YANMA": 2,
            "MURKROW": 2,
            "HOUNDOUR": 2,
            "ABRA": 3,
            "MAREEP": 2,
            "MARILL": 2,
            "FARFETCHD": 2,
            "DROWZEE": 2,
            "STANTLER": 2,
            "SMEARGLE": 2,
            "PHANPY": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "GROWLITHE": 2,
            "GIRAFARIG": 1,
            "CHARMANDER": 3,
            "SQUIRTLE": 3,
            "CYNDAQUIL": 3,
            "TOTODILE": 3,
            "MR_MIME": 3,
        },
    },
    "ForestEdgeLate": {
        "species": {
            "CATERPIE": 2,
            "WEEDLE": 2,
            "LEDYBA": 2,
            "SPINARAK": 2,
            "PIDGEY": 2,
            "HOOTHOOT": 2,
            "SPEAROW": 2,
            "RATTATA": 2,
            "MEOWTH": 2,
            "SENTRET": 2,
            "EKANS": 3,
            "NIDORAN_F": 4,
            "NIDORAN_M": 4,
            "ODDISH": 4,
            "BELLSPROUT": 4,
            "PARAS": 3,
            "VENONAT": 3,
            "TANGELA": 4,
            "EEVEE": 4,
            "PICHU": 4,
            "TOGEPI": 2,
            "HOPPIP": 2,
            "SUNKERN": 2,
            "BULBASAUR": 3,
            "CHIKORITA": 3,
            "SNUBBULL": 2,
            "YANMA": 2,
            "MURKROW": 2,
            "HOUNDOUR": 2,
            "ABRA": 4,
            "MAREEP": 4,
            "MARILL": 4,
            "FARFETCHD": 4,
            "DROWZEE": 4,
            "STANTLER": 4,
            "SMEARGLE": 2,
            "PHANPY": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "GROWLITHE": 2,
            "GIRAFARIG": 4,
            "CHARMANDER": 3,
            "SQUIRTLE": 3,
            "CYNDAQUIL": 3,
            "TOTODILE": 3,
            "MR_MIME": 3,
        },
    },
    "PlainsEarly": {
        "species": {
            "CHARMANDER": 2,
            "CYNDAQUIL": 2,
            "CHIKORITA": 2,
            "RATTATA": 3,
            "SENTRET": 3,
            "SPEAROW": 3,
            "EKANS": 3,
            "SANDSHREW": 3,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "MANKEY": 3,
            "DODUO": 2,
            "HOUNDOUR": 2,
            "CHIKORITA": 2,
            "BULBASAUR": 2,
            "MAREEP": 2,
            "PHANPY": 2,
            "IGGLYBUFF": 2,
            "GROWLITHE": 2,
            "PONYTA": 2,
            "RHYHORN": 1,
            "GIRAFARIG": 1,
            "MILTANK": 1,
            "TAUROS": 1,
            "KANGASKHAN": 1,
            "MR_MIME": 1,
            "TANGELA": 1,
            "SLUGMA": 1,
            "SCYTHER": 1,
            "PINSIR": 1,
        },
    },
    "PlainsMid": {
        "species": {
            "CHARMANDER": 2,
            "CYNDAQUIL": 2,
            "CHIKORITA": 2,
            "RATTATA": 2,
            "SENTRET": 2,
            "SPEAROW": 3,
            "EKANS": 3,
            "SANDSHREW": 3,
            "NIDORAN_F": 3,
            "NIDORAN_M": 3,
            "MANKEY": 4,
            "DODUO": 3,
            "HOUNDOUR": 3,
            "CHIKORITA": 2,
            "BULBASAUR": 2,
            "MAREEP": 2,
            "PHANPY": 3,
            "IGGLYBUFF": 3,
            "GROWLITHE": 3,
            "PONYTA": 3,
            "RHYHORN": 3,
            "GIRAFARIG": 3,
            "MILTANK": 3,
            "TAUROS": 3,
            "KANGASKHAN": 2,
            "MR_MIME": 2,
            "TANGELA": 2,
            "SLUGMA": 2,
            "SCYTHER": 2,
            "PINSIR": 2,
        },
    },
    "PlainsLate": {
        "species": {
            "CHARMANDER": 2,
            "CYNDAQUIL": 2,
            "CHIKORITA": 2,
            "RATTATA": 2,
            "SENTRET": 2,
            "SPEAROW": 4,
            "EKANS": 4,
            "SANDSHREW": 4,
            "NIDORAN_F": 4,
            "NIDORAN_M": 4,
            "MANKEY": 4,
            "DODUO": 3,
            "HOUNDOUR": 3,
            "CHIKORITA": 2,
            "BULBASAUR": 2,
            "MAREEP": 2,
            "PHANPY": 3,
            "IGGLYBUFF": 3,
            "GROWLITHE": 3,
            "PONYTA": 3,
            "RHYHORN": 3,
            "GIRAFARIG": 3,
            "MILTANK": 3,
            "TAUROS": 3,
            "KANGASKHAN": 4,
            "MR_MIME": 4,
            "TANGELA": 4,
            "SLUGMA": 4,
            "SCYTHER": 3,
            "PINSIR": 3,
        },
    },
    "MeadowEarly": {
        "species": {
            "PIDGEY": 3,
            "RATTATA": 3,
            "SPEAROW": 3,
            "IGGLYBUFF": 3,
            "CLEFFA": 3,
            "PICHU": 3,
            "EEVEE": 3,
            "TOGEPI": 3,
            "SUNKERN": 3,
            "LEDYBA": 3,
            "SPINARAK": 3,
            "MARILL": 3,
            "MAREEP": 3,
            "YANMA": 3,
            "AIPOM": 3,
            "HOPPIP": 3,
            "SENTRET": 3,
            "HOOTHOOT": 3,
            "WOOPER": 3,
            "POLIWAG": 3,
            "SNUBBULL": 3,
            "EKANS": 2,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "VULPIX": 2,
            "PARAS": 2,
            "PONYTA": 2,
            "SLOWPOKE": 2,
            "FARFETCHD": 2,
            "DROWZEE": 2,
            "EXEGGCUTE": 2,
            "MEOWTH": 2,
            "CUBONE": 2,
            "DITTO": 2,
            "LICKITUNG": 2,
            "MILTANK": 2,
            "BULBASAUR": 2,
            "CHIKORITA": 2,
            "SQUIRTLE": 1,
            "TOTODILE": 1,
            "ELEKID": 1,
            "MAGBY": 1,
            "SMOOCHUM": 1,
            "CHANSEY": 1,
            "TANGELA": 1,
            "MR_MIME": 1,
            "SNORLAX": 1,
            "SCYTHER": 1,
            "PINSIR": 1,
        },
    },
    "MeadowMid": {
        "species": {
            "PIDGEY": 2,
            "RATTATA": 2,
            "SPEAROW": 1,
            "IGGLYBUFF": 3,
            "CLEFFA": 3,
            "PICHU": 3,
            "EEVEE": 3,
            "TOGEPI": 3,
            "SUNKERN": 3,
            "LEDYBA": 3,
            "SPINARAK": 3,
            "MARILL": 3,
            "MAREEP": 3,
            "YANMA": 3,
            "AIPOM": 3,
            "HOPPIP": 3,
            "SENTRET": 2,
            "HOOTHOOT": 2,
            "WOOPER": 3,
            "POLIWAG": 3,
            "SNUBBULL": 3,
            "EKANS": 1,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "VULPIX": 3,
            "PARAS": 2,
            "PONYTA": 3,
            "SLOWPOKE": 3,
            "FARFETCHD": 3,
            "DROWZEE": 3,
            "EXEGGCUTE": 3,
            "MEOWTH": 3,
            "CUBONE": 2,
            "DITTO": 2,
            "LICKITUNG": 3,
            "MILTANK": 3,
            "BULBASAUR": 2,
            "CHIKORITA": 2,
            "SQUIRTLE": 1,
            "TOTODILE": 1,
            "ELEKID": 1,
            "MAGBY": 1,
            "SMOOCHUM": 1,
            "CHANSEY": 2,
            "TANGELA": 2,
            "MR_MIME": 2,
            "SNORLAX": 1,
            "SCYTHER": 2,
            "PINSIR": 2,
        },
    },
    "MeadowLate": {
        "species": {
            "PIDGEY": 2,
            "RATTATA": 2,
            "SPEAROW": 1,
            "IGGLYBUFF": 3,
            "CLEFFA": 3,
            "PICHU": 3,
            "EEVEE": 3,
            "TOGEPI": 3,
            "SUNKERN": 3,
            "LEDYBA": 3,
            "SPINARAK": 3,
            "MARILL": 4,
            "MAREEP": 4,
            "YANMA": 3,
            "AIPOM": 3,
            "HOPPIP": 3,
            "SENTRET": 2,
            "HOOTHOOT": 2,
            "WOOPER": 3,
            "POLIWAG": 3,
            "SNUBBULL": 3,
            "EKANS": 1,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "VULPIX": 4,
            "PARAS": 2,
            "PONYTA": 4,
            "SLOWPOKE": 4,
            "FARFETCHD": 3,
            "DROWZEE": 3,
            "EXEGGCUTE": 3,
            "MEOWTH": 3,
            "CUBONE": 2,
            "DITTO": 3,
            "LICKITUNG": 4,
            "MILTANK": 4,
            "BULBASAUR": 2,
            "CHIKORITA": 2,
            "SQUIRTLE": 1,
            "TOTODILE": 1,
            "ELEKID": 1,
            "MAGBY": 1,
            "SMOOCHUM": 1,
            "CHANSEY": 4,
            "TANGELA": 4,
            "MR_MIME": 4,
            "SNORLAX": 3,
            "SCYTHER": 3,
            "PINSIR": 3,
        },
    },
    "MountainFootEarly": {
        "species": {
            "GEODUDE": 4,
            "MACHOP": 4,
            "MANKEY": 3,
            "TYROGUE": 3,
            "SANDSHREW": 3,
            "MAGNEMITE": 3,
            "TEDDIURSA": 2,
            "PHANPY": 2,
            "SWINUB": 2,
            "SKARMORY": 2,
            "GLIGAR": 2,
            "SNEASEL": 2,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "WOOPER": 2,
            "MARILL": 2,
            "SUDOWOODO": 2,
            "MURKROW": 2,
            "MISDREAVUS": 2,
            "HOUNDOUR": 2,
            "VULPIX": 2,
            "MAGBY": 2,
            "SPEAROW": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ZUBAT": 2,
            "PARAS": 2,
            "RHYHORN": 2,
            "CYNDAQUIL": 2,
            "CHARMANDER": 2,
            "SLUGMA": 3,
            "LARVITAR": 2,
            "DIGLETT": 2,
        },
    },
    "MountainFootMid": {
        "species": {
            "GEODUDE": 4,
            "MACHOP": 4,
            "MANKEY": 3,
            "TYROGUE": 3,
            "SANDSHREW": 3,
            "MAGNEMITE": 3,
            "TEDDIURSA": 2,
            "PHANPY": 2,
            "SWINUB": 3,
            "SKARMORY": 3,
            "GLIGAR": 3,
            "SNEASEL": 3,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "WOOPER": 2,
            "MARILL": 2,
            "SUDOWOODO": 2,
            "MURKROW": 3,
            "MISDREAVUS": 3,
            "HOUNDOUR": 3,
            "VULPIX": 2,
            "MAGBY": 3,
            "SPEAROW": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ZUBAT": 2,
            "PARAS": 2,
            "RHYHORN": 3,
            "CYNDAQUIL": 2,
            "CHARMANDER": 2,
            "SLUGMA": 3,
            "LARVITAR": 3,
            "DIGLETT": 2,
            "ONIX": 2,
        },
    },
    "MountainFootLate": {
        "species": {
            "GEODUDE": 2,
            "MACHOP": 2,
            "MANKEY": 2,
            "TYROGUE": 2,
            "SANDSHREW": 2,
            "MAGNEMITE": 4,
            "TEDDIURSA": 2,
            "PHANPY": 2,
            "SWINUB": 3,
            "SKARMORY": 3,
            "GLIGAR": 3,
            "SNEASEL": 3,
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "WOOPER": 2,
            "MARILL": 2,
            "SUDOWOODO": 2,
            "MURKROW": 3,
            "MISDREAVUS": 3,
            "HOUNDOUR": 3,
            "VULPIX": 2,
            "MAGBY": 3,
            "SPEAROW": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ZUBAT": 2,
            "PARAS": 2,
            "RHYHORN": 3,
            "CYNDAQUIL": 2,
            "CHARMANDER": 2,
            "SLUGMA": 3,
            "LARVITAR": 3,
            "DIGLETT": 2,
            "ONIX": 3,
        },
    },
    "MountainPeakEarly": {
        "species": {
            "GEODUDE": 2,
            "MACHOP": 2,
            "TYROGUE": 3,
            "MAGNEMITE": 3,
            "SWINUB": 3,
            "SKARMORY": 3,
            "SLUGMA": 3,
            "GLIGAR": 4,
            "SNEASEL": 3,
            "MURKROW": 2,
            "MISDREAVUS": 2,
            "HOUNDOUR": 2,
            "VULPIX": 2,
            "MAGBY": 2,
            "CLEFFA": 2,
            "ZUBAT": 2,
            "CYNDAQUIL": 2,
            "CHARMANDER": 2,
            "LARVITAR": 3,
            "ONIX": 2,
            "DELIBIRD": 2,
            "AERODACTYL": 1,
        },
    },
    "MountainPeakMid": {
        "species": {
            "GEODUDE": 2,
            "MACHOP": 2,
            "TYROGUE": 3,
            "MAGNEMITE": 3,
            "SWINUB": 3,
            "SKARMORY": 4,
            "SLUGMA": 3,
            "GLIGAR": 4,
            "SNEASEL": 4,
            "MURKROW": 4,
            "MISDREAVUS": 4,
            "HOUNDOUR": 3,
            "VULPIX": 2,
            "MAGBY": 2,
            "CLEFFA": 3,
            "ZUBAT": 2,
            "CYNDAQUIL": 2,
            "CHARMANDER": 2,
            "LARVITAR": 3,
            "ONIX": 2,
            "DELIBIRD": 2,
            "AERODACTYL": 2,
        },
    },
    "MountainPeakLate": {
        "species": {
            "GEODUDE": 2,
            "MACHOP": 2,
            "TYROGUE": 3,
            "MAGNEMITE": 3,
            "SWINUB": 3,
            "SKARMORY": 4,
            "SLUGMA": 3,
            "GLIGAR": 4,
            "SNEASEL": 4,
            "MURKROW": 4,
            "MISDREAVUS": 4,
            "HOUNDOUR": 4,
            "VULPIX": 4,
            "MAGBY": 2,
            "CLEFFA": 3,
            "ZUBAT": 2,
            "CYNDAQUIL": 2,
            "CHARMANDER": 2,
            "LARVITAR": 4,
            "ONIX": 3,
            "DELIBIRD": 2,
            "AERODACTYL": 3,
        },
    },
    "CaveEntranceEarly": {
        "species": {
            "ZUBAT": 3,
            "GEODUDE": 3,
            "PARAS": 2,
            "DIGLETT": 2,
            "SANDSHREW": 2,
            "ABRA": 2,
            "MACHOP": 2,
            "GASTLY": 2,
            "CUBONE": 2,
            "SWINUB": 2,
            "ONIX": 1,
            "DUNSPARCE": 1,
            "LARVITAR": 1,
            "LICKITUNG": 1,
            "OMANYTE": 1,
            "KABUTO": 1,
            "CLEFFA": 2,
            "MARILL": 1,
            "WOOPER": 1,
            "MURKROW": 1,
            "MISDREAVUS": 1,
            "SHUCKLE": 1,
            "UNOWN": 1,
            "WOBBUFFET": 1,
            "TEDDIURSA": 1,
            "PHANPY": 1,
            "TYROGUE": 1,
            "ELEKID": 1,
            "MAGBY": 1,
        },
    },
    "CaveEntranceMid": {
        "species": {
            "ZUBAT": 3,
            "GEODUDE": 3,
            "PARAS": 2,
            "DIGLETT": 2,
            "SANDSHREW": 2,
            "ABRA": 2,
            "MACHOP": 2,
            "GASTLY": 2,
            "CUBONE": 2,
            "SWINUB": 2,
            "ONIX": 3,
            "DUNSPARCE": 2,
            "LARVITAR": 2,
            "LICKITUNG": 2,
            "OMANYTE": 1,
            "KABUTO": 1,
            "CLEFFA": 2,
            "MARILL": 2,
            "WOOPER": 2,
            "MURKROW": 2,
            "MISDREAVUS": 2,
            "SHUCKLE": 2,
            "UNOWN": 2,
            "WOBBUFFET": 2,
            "TEDDIURSA": 2,
            "PHANPY": 1,
            "TYROGUE": 2,
            "ELEKID": 1,
            "MAGBY": 2,
        },
    },
    "CaveEntranceLate": {
        "species": {
            "ZUBAT": 3,
            "GEODUDE": 3,
            "PARAS": 2,
            "DIGLETT": 2,
            "SANDSHREW": 2,
            "ABRA": 3,
            "MACHOP": 3,
            "GASTLY": 3,
            "CUBONE": 3,
            "SWINUB": 3,
            "ONIX": 3,
            "DUNSPARCE": 2,
            "LARVITAR": 3,
            "LICKITUNG": 2,
            "OMANYTE": 2,
            "KABUTO": 2,
            "CLEFFA": 2,
            "MARILL": 2,
            "WOOPER": 2,
            "MURKROW": 2,
            "MISDREAVUS": 2,
            "SHUCKLE": 2,
            "UNOWN": 3,
            "WOBBUFFET": 3,
            "TEDDIURSA": 3,
            "PHANPY": 2,
            "TYROGUE": 3,
            "ELEKID": 2,
            "MAGBY": 3,
        },
    },
    "CaveDepthEarly": {
        "species": {
            "ZUBAT": 3,
            "GEODUDE": 3,
            "DIGLETT": 2,
            "GASTLY": 2,
            "CUBONE": 2,
            "SWINUB": 2,
            "MAGNEMITE": 2,
            "KANGASKHAN": 2,
            "ONIX": 2,
            "DUNSPARCE": 2,
            "LARVITAR": 2,
            "SNEASEL": 2,
            "OMANYTE": 2,
            "KABUTO": 2,
            "CLEFFA": 3,
            "MARILL": 2,
            "MURKROW": 2,
            "MISDREAVUS": 2,
            "UNOWN": 2,
            "WOBBUFFET": 2,
            "TYROGUE": 2,
            "SLUGMA": 2,
            "DITTO": 1,
        },
    },
    "CaveDepthMid": {
        "species": {
            "ZUBAT": 3,
            "GEODUDE": 3,
            "DIGLETT": 3,
            "GASTLY": 3,
            "CUBONE": 3,
            "SWINUB": 3,
            "MAGNEMITE": 2,
            "KANGASKHAN": 2,
            "ONIX": 3,
            "DUNSPARCE": 3,
            "LARVITAR": 3,
            "SNEASEL": 2,
            "OMANYTE": 2,
            "KABUTO": 2,
            "CLEFFA": 3,
            "MARILL": 2,
            "MURKROW": 2,
            "MISDREAVUS": 2,
            "UNOWN": 3,
            "WOBBUFFET": 3,
            "TYROGUE": 2,
            "SLUGMA": 2,
            "DITTO": 2,
        },
    },
    "CaveDepthLate": {
        "species": {
            "ZUBAT": 2,
            "GEODUDE": 2,
            "DIGLETT": 2,
            "GASTLY": 3,
            "CUBONE": 2,
            "SWINUB": 2,
            "MAGNEMITE": 2,
            "KANGASKHAN": 2,
            "ONIX": 3,
            "DUNSPARCE": 3,
            "LARVITAR": 4,
            "SNEASEL": 2,
            "OMANYTE": 3,
            "KABUTO": 3,
            "CLEFFA": 3,
            "MARILL": 2,
            "MURKROW": 4,
            "MISDREAVUS": 4,
            "UNOWN": 3,
            "WOBBUFFET": 4,
            "TYROGUE": 3,
            "SLUGMA": 3,
            "DITTO": 2,
        },
    },
    "UndergroundLakeSurf": {
        "species": {
            "PSYDUCK": 3,
            "WOOPER": 3,
            "SLOWPOKE": 3,
            "SEEL": 2,
            "GOLDEEN": 2,
            "POLIWAG": 2,
            "TOTODILE": 2,
            "SQUIRTLE": 2,
            "MARILL": 2,
            "REMORAID": 2,
            "ZUBAT": 2,
            "LAPRAS": 2,
            "DRATINI": 1,
            "OMANYTE": 1,
            "KABUTO": 1,
        },
    },
    "UndergroundLakeFish": {
        "species": {
            "MAGIKARP": 3,
            "POLIWAG": 2,
            "GOLDEEN": 2,
            "SLOWPOKE": 2,
            "DRATINI": 1,
            "OMANYTE": 2,
            "KABUTO": 2,
            "REMORAID": 2,
        },
    },
    "CityOutskirtsEarly": {
        "species": {
            "PIDGEY": 3,
            "HOOTHOOT": 3,
            "RATTATA": 3,
            "SENTRET": 3,
            "SPEAROW": 2,
            "MEOWTH": 2,
            "GROWLITHE": 2,
            "VULPIX": 2,
            "PSYDUCK": 2,
            "HOUNDOUR": 2,
            "MURKROW": 2,
            "ABRA": 2,
            "MAGNEMITE": 2,
            "GRIMER": 2,
            "KOFFING": 2,
            "VOLTORB": 2,
            "SNUBBULL": 2,
            "AIPOM": 2,
            "STANTLER": 2,
            "MAREEP": 2,
            "MARILL": 2,
            "SMEARGLE": 2,
            "ELEKID": 1,
            "SMOOCHUM": 1,
            "MAGBY": 1,
            "POLIWAG": 2,
            "VENONAT": 2,
            "EKANS": 2,
            "DROWZEE": 2,
            "WEEDLE": 1,
            "CATERPIE": 1,
            "LEDYBA": 1,
            "SPINARAK": 1,
            "BULBASAUR": 1,
            "CHARMANDER": 1,
            "SQUIRTLE": 1,
            "CHIKORITA": 1,
            "CYNDAQUIL": 1,
            "TOTODILE": 1,
            "PICHU": 1,
            "TOGEPI": 1,
            "CHANSEY": 1,
            "MR_MIME": 1,
            "LICKITUNG": 1,
            "TANGELA": 1,
            "EEVEE": 2,
        },
    },
    "CityOutskirtsMid": {
        "species": {
            "PIDGEY": 2,
            "HOOTHOOT": 2,
            "RATTATA": 2,
            "SENTRET": 2,
            "SPEAROW": 3,
            "MEOWTH": 3,
            "GROWLITHE": 3,
            "VULPIX": 3,
            "PSYDUCK": 3,
            "HOUNDOUR": 3,
            "MURKROW": 3,
            "ABRA": 3,
            "MAGNEMITE": 4,
            "GRIMER": 4,
            "KOFFING": 4,
            "VOLTORB": 4,
            "SNUBBULL": 3,
            "AIPOM": 3,
            "STANTLER": 3,
            "MAREEP": 3,
            "MARILL": 3,
            "SMEARGLE": 3,
            "ELEKID": 2,
            "SMOOCHUM": 2,
            "MAGBY": 2,
            "POLIWAG": 3,
            "VENONAT": 3,
            "EKANS": 3,
            "DROWZEE": 3,
            "WEEDLE": 1,
            "CATERPIE": 1,
            "LEDYBA": 1,
            "SPINARAK": 1,
            "BULBASAUR": 1,
            "CHARMANDER": 1,
            "SQUIRTLE": 1,
            "CHIKORITA": 1,
            "CYNDAQUIL": 1,
            "TOTODILE": 1,
            "PICHU": 1,
            "TOGEPI": 1,
            "CHANSEY": 2,
            "MR_MIME": 2,
            "LICKITUNG": 2,
            "TANGELA": 2,
            "EEVEE": 3,
        },
    },
    "CityOutskirtsLate": {
        "species": {
            "PIDGEY": 2,
            "HOOTHOOT": 2,
            "RATTATA": 2,
            "SENTRET": 2,
            "SPEAROW": 3,
            "MEOWTH": 3,
            "GROWLITHE": 3,
            "VULPIX": 3,
            "PSYDUCK": 3,
            "HOUNDOUR": 3,
            "MURKROW": 3,
            "ABRA": 3,
            "MAGNEMITE": 4,
            "GRIMER": 4,
            "KOFFING": 4,
            "VOLTORB": 4,
            "SNUBBULL": 3,
            "AIPOM": 3,
            "STANTLER": 3,
            "MAREEP": 3,
            "MARILL": 3,
            "SMEARGLE": 3,
            "ELEKID": 2,
            "SMOOCHUM": 2,
            "MAGBY": 2,
            "POLIWAG": 3,
            "VENONAT": 3,
            "EKANS": 3,
            "DROWZEE": 3,
            "WEEDLE": 1,
            "CATERPIE": 1,
            "LEDYBA": 1,
            "SPINARAK": 1,
            "BULBASAUR": 1,
            "CHARMANDER": 1,
            "SQUIRTLE": 1,
            "CHIKORITA": 1,
            "CYNDAQUIL": 1,
            "TOTODILE": 1,
            "PICHU": 1,
            "TOGEPI": 1,
            "CHANSEY": 4,
            "MR_MIME": 4,
            "LICKITUNG": 4,
            "TANGELA": 4,
            "EEVEE": 4,
        },
    },
    "ShallowSeaSurf": {
        "species": {
            "TENTACOOL": 3,
            "HORSEA": 2,
            "SLOWPOKE": 2,
            "SEEL": 2,
            "SHELLDER": 2,
            "QWILFISH": 2,
            "REMORAID": 2,
            "MANTINE": 2,
            "KRABBY": 1,
            "STARYU": 2,
            "MAGIKARP": 1,
            "SQUIRTLE": 2,
            "TOTODILE": 2,
            "OMANYTE": 1,
            "KABUTO": 1,
            "LAPRAS": 1,
            "CORSOLA": 2
        },
    },
    "ShallowSeaFish": {
        "species": {
            "MAGIKARP": 3,
            "TENTACOOL": 2,
            "HORSEA": 2,
            "SHELLDER": 2,
            "KRABBY": 2,
            "GOLDEEN": 2,
            "STARYU": 2,
            "CHINCHOU": 2,
            "CORSOLA": 2,
            "QWILFISH": 2,
            "REMORAID": 2,
            "KABUTO": 2,
            "OMANYTE": 2,
        },
    },
    "DeepSeaSurf": {
        "species": {
            "TENTACOOL": 3,
            "HORSEA": 2,
            "SEEL": 2,
            "STARYU": 2,
            "LAPRAS": 2,
            "MANTINE": 2,
            "CORSOLA": 2,
            "REMORAID": 2,
            "CHINCHOU": 1,
        },
    },
    "DeepSeaFish": {
        "species": {
            "MAGIKARP": 3,
            "HORSEA": 2,
            "SHELLDER": 2,
            "STARYU": 2,
            "TENTACOOL": 2,
            "CHINCHOU": 2,
            "QWILFISH": 2,
            "REMORAID": 2,
            "KABUTO": 2,
            "OMANYTE": 2,
            "CORSOLA": 2,
        },
    },
    "RiverSurf": {
        "species": {
            "PSYDUCK": 3,
            "SLOWPOKE": 3,
            "POLIWAG": 2,
            "KRABBY": 1,
            "GOLDEEN": 2,
            "SQUIRTLE": 3,
            "TOTODILE": 3,
            "MARILL": 3,
            "WOOPER": 2,
            "REMORAID": 2,
            "DRATINI": 1,
        },
    },
    "RiverFish": {
        "species": {
            "MAGIKARP": 3,
            "POLIWAG": 2,
            "GOLDEEN": 2,
            "KRABBY": 2,
            "HORSEA": 1,
            "PSYDUCK": 2,
            "SLOWPOKE": 2,
            "WOOPER": 2,
            "REMORAID": 2,
            "DRATINI": 2,
        },
    },
    "LakeSurf": {
        "species": {
            "PSYDUCK": 3,
            "SLOWPOKE": 3,
            "POLIWAG": 2,
            "MAGIKARP": 1,
            "GOLDEEN": 2,
            "MARILL": 2,
            "WOOPER": 2,
            "SQUIRTLE": 2,
            "TOTODILE": 2,
            "DRATINI": 1,
            "LAPRAS": 1,
        },
    },
    "LakeFish": {
        "species": {
            "MAGIKARP": 3,
            "POLIWAG": 2,
            "GOLDEEN": 2,
            "PSYDUCK": 2,
            "SLOWPOKE": 2,
            "DRATINI": 2,
            "MARILL": 2,
            "WOOPER": 2
        },
    },
    "VolcanicEarly": {
        "species": {
            "GEODUDE": 3,
            "MACHOP": 2,
            "ONIX": 2,
            "PONYTA": 2,
            "GROWLITHE": 2,
            "VULPIX": 2,
            "MAGNEMITE": 1,
            "MAGBY": 2,
            "SLUGMA": 2,
            "CHARMANDER": 2,
            "HOUNDOUR": 2,
            "CYNDAQUIL": 2,
            "RHYHORN": 2,
            "KOFFING": 2,
            "GRIMER": 2,
            "SKARMORY": 2,
            "AERODACTYL": 1,
            "LARVITAR": 1,
        },
    },
    "VolcanicMid": {
        "species": {
            "GEODUDE": 3,
            "MACHOP": 2,
            "ONIX": 2,
            "PONYTA": 2,
            "GROWLITHE": 2,
            "VULPIX": 2,
            "MAGNEMITE": 1,
            "MAGBY": 3,
            "SLUGMA": 3,
            "CHARMANDER": 2,
            "HOUNDOUR": 2,
            "CYNDAQUIL": 2,
            "RHYHORN": 2,
            "KOFFING": 2,
            "GRIMER": 2,
            "SKARMORY": 2,
            "AERODACTYL": 1,
            "LARVITAR": 2,
        },
    },
    "VolcanicLate": {
        "species": {
            "GEODUDE": 2,
            "MACHOP": 2,
            "ONIX": 2,
            "PONYTA": 2,
            "GROWLITHE": 2,
            "VULPIX": 2,
            "MAGNEMITE": 1,
            "MAGBY": 3,
            "SLUGMA": 3,
            "CHARMANDER": 2,
            "HOUNDOUR": 2,
            "CYNDAQUIL": 2,
            "RHYHORN": 3,
            "KOFFING": 3,
            "GRIMER": 3,
            "SKARMORY": 3,
            "AERODACTYL": 2,
            "LARVITAR": 3,
        },
    },
    "IcyEarly": {
        "species": {
            "ZUBAT": 2,
            "SLOWPOKE": 2,
            "SWINUB": 2,
            "SMOOCHUM": 1,
            "DELIBIRD": 1,
            "SNEASEL": 1,
        },
    },
    "IcyMid": {
        "species": {
            "ZUBAT": 2,
            "SLOWPOKE": 2,
            "SWINUB": 2,
            "SMOOCHUM": 1,
            "DELIBIRD": 2,
            "SNEASEL": 2,
        },
    },
    "IcyLate": {
        "species": {
            "ZUBAT": 2,
            "SLOWPOKE": 2,
            "SWINUB": 2,
            "SMOOCHUM": 2,
            "DELIBIRD": 3,
            "SNEASEL": 3,
        },
    },
    "RuinsEarly": {
        "species": {
            "ZUBAT": 2,
            "GASTLY": 2,
            "MISDREAVUS": 2,
            "MURKROW": 2,
            "SPINARAK": 2,
            "YANMA": 2,
            "NATU": 3,
            "WOOPER": 1,
            "UNOWN": 3,
            "ABRA": 3,
            "WOBBUFFET": 2,
            "VULPIX": 2,
            "CUBONE": 2,
            "MAGNEMITE": 2,
            "EXEGGCUTE": 2,
            "DROWZEE": 2,
            "MR_MIME": 2,
            "TANGELA": 2,
            "LARVITAR": 2,
            "GIRAFARIG": 2,
            "DUNSPARCE": 2,
            "STANTLER": 2,
            "SMEARGLE": 2,
        },
    },
    "RuinsMid": {
        "species": {
            "ZUBAT": 2,
            "GASTLY": 4,
            "MISDREAVUS": 3,
            "MURKROW": 3,
            "SPINARAK": 2,
            "YANMA": 2,
            "NATU": 4,
            "WOOPER": 2,
            "UNOWN": 3,
            "ABRA": 3,
            "WOBBUFFET": 2,
            "VULPIX": 3,
            "CUBONE": 2,
            "MAGNEMITE": 3,
            "EXEGGCUTE": 2,
            "DROWZEE": 2,
            "MR_MIME": 3,
            "TANGELA": 2,
            "LARVITAR": 2,
            "GIRAFARIG": 2,
            "DUNSPARCE": 2,
            "STANTLER": 2,
            "SMEARGLE": 2,
        },
    },
    "RuinsLate": {
        "species": {
            "ZUBAT": 2,
            "GASTLY": 4,
            "MISDREAVUS": 4,
            "MURKROW": 4,
            "SPINARAK": 2,
            "YANMA": 2,
            "NATU": 2,
            "WOOPER": 2,
            "UNOWN": 4,
            "ABRA": 2,
            "WOBBUFFET": 3,
            "VULPIX": 2,
            "CUBONE": 2,
            "MAGNEMITE": 2,
            "EXEGGCUTE": 2,
            "DROWZEE": 2,
            "MR_MIME": 3,
            "TANGELA": 3,
            "LARVITAR": 4,
            "GIRAFARIG": 4,
            "DUNSPARCE": 4,
            "STANTLER": 4,
            "SMEARGLE": 4,
        },
    },
    "MansionEarly": {
        "species": {
            "RATTATA": 2,
            "PICHU": 2,
            "EEVEE": 2,
            "KOFFING": 2,
            "GRIMER": 2,
            "VULPIX": 2,
            "GROWLITHE": 2,
            "HOUNDOUR": 2,
            "MAGNEMITE": 2,
            "ELEKID": 2,
            "MURKROW": 2,
            "MISDREAVUS": 1,
            "CHARMANDER": 1,
            "CYNDAQUIL": 1,
            "MAGBY": 1,
            "SMEARGLE": 1,
            "GASTLY": 1,
            "DITTO": 1,
            "PORYGON": 1,
            "MR_MIME": 1,
            "LICKITUNG": 1,
        },
    },
    "MansionMid": {
        "species": {
            "RATTATA": 1,
            "PICHU": 1,
            "EEVEE": 2,
            "KOFFING": 2,
            "GRIMER": 2,
            "VULPIX": 2,
            "GROWLITHE": 2,
            "HOUNDOUR": 2,
            "MAGNEMITE": 2,
            "ELEKID": 2,
            "MURKROW": 1,
            "MISDREAVUS": 2,
            "CHARMANDER": 2,
            "CYNDAQUIL": 2,
            "MAGBY": 2,
            "SMEARGLE": 2,
            "GASTLY": 2,
            "DITTO": 2,
            "PORYGON": 2,
            "MR_MIME": 2,
            "LICKITUNG": 2,
        },
    },
    "MansionLate": {
        "species": {
            "RATTATA": 1,
            "PICHU": 1,
            "EEVEE": 1,
            "KOFFING": 3,
            "GRIMER": 3,
            "VULPIX": 2,
            "GROWLITHE": 2,
            "HOUNDOUR": 3,
            "MAGNEMITE": 2,
            "ELEKID": 2,
            "MURKROW": 1,
            "MISDREAVUS": 3,
            "CHARMANDER": 2,
            "CYNDAQUIL": 2,
            "MAGBY": 3,
            "SMEARGLE": 2,
            "GASTLY": 3,
            "DITTO": 4,
            "PORYGON": 4,
            "MR_MIME": 3,
            "LICKITUNG": 3,
        },
    },
    "Safari1": {
        "species": {
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "PARAS": 2,
            "DODUO": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "VENONAT": 2,
            "EXEGGCUTE": 2,
            "CUBONE": 2,
            "RHYHORN": 2,
            "KANGASKHAN": 2,
            "SCYTHER": 2,
            "PINSIR": 2,
            "HERACROSS": 12,
            "WOBBUFFET": 2,
            "TAUROS": 2,
            "MILTANK": 2,
            "STANTLER": 2,
            "CHANSEY": 2,
            "AIPOM": 2,
            "GIRAFARIG": 2,
            "MILTANK": 2,
            "BULBASAUR": 2,
            "CHARMANDER": 2,
            "SQUIRTLE": 2,
            "CHIKORITA": 2,
            "CYNDAQUIL": 2,
            "TOTODILE": 2,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "SPINARAK": 2,
            "LEDYBA": 2,
            "WEEDLE": 2,
            "CATERPIE": 2,
            "PINECO": 2,
            "SHUCKLE": 2,
            "PIDGEY": 1,
            "RATTATA": 1,
            "SENTRET": 1,
            "HOOTHOOT": 1,
            "HOUNDOUR": 2,
            "MR_MIME": 2,
            "LICKITUNG": 2,
            "PORYGON": 2,
            "DITTO": 2,
            "SNORLAX": 2,
            "OMANYTE": 2,
            "KABUTO": 2,
            "AERODACTYL": 2,
            "TANGELA": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "LARVITAR": 2,
            "DUNSPARCE": 2,
            "GLIGAR": 2,
            "SNUBBULL": 2,
            "DELIBIRD": 2,
            "SUNKERN": 2,
            "YANMA": 2,
            "SMEARGLE": 2,
            "TYROGUE": 2,
        },
    },
    "Safari2": {
        "species": {
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "PARAS": 2,
            "DODUO": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "VENONAT": 2,
            "EXEGGCUTE": 2,
            "CUBONE": 2,
            "RHYHORN": 2,
            "KANGASKHAN": 12,
            "SCYTHER": 2,
            "PINSIR": 2,
            "HERACROSS": 12,
            "WOBBUFFET": 2,
            "TAUROS": 12,
            "MILTANK": 2,
            "STANTLER": 2,
            "CHANSEY": 2,
            "AIPOM": 2,
            "GIRAFARIG": 2,
            "MILTANK": 2,
            "BULBASAUR": 2,
            "CHARMANDER": 2,
            "SQUIRTLE": 2,
            "CHIKORITA": 2,
            "CYNDAQUIL": 2,
            "TOTODILE": 2,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "SPINARAK": 2,
            "LEDYBA": 2,
            "WEEDLE": 2,
            "CATERPIE": 2,
            "PINECO": 2,
            "SHUCKLE": 2,
            "PIDGEY": 1,
            "RATTATA": 1,
            "SENTRET": 1,
            "HOOTHOOT": 1,
            "HOUNDOUR": 2,
            "MR_MIME": 2,
            "LICKITUNG": 2,
            "PORYGON": 2,
            "DITTO": 2,
            "SNORLAX": 12,
            "OMANYTE": 2,
            "KABUTO": 2,
            "AERODACTYL": 12,
            "TANGELA": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "LARVITAR": 2,
            "DUNSPARCE": 2,
            "GLIGAR": 2,
            "SNUBBULL": 2,
            "DELIBIRD": 2,
            "SUNKERN": 2,
            "YANMA": 2,
            "SMEARGLE": 2,
            "TYROGUE": 2,
        },
    },
    "Safari3": {
        "species": {
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "PARAS": 2,
            "DODUO": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "VENONAT": 2,
            "EXEGGCUTE": 2,
            "CUBONE": 2,
            "RHYHORN": 2,
            "KANGASKHAN": 2,
            "SCYTHER": 12,
            "PINSIR": 12,
            "HERACROSS": 12,
            "WOBBUFFET": 2,
            "TAUROS": 2,
            "MILTANK": 2,
            "STANTLER": 2,
            "CHANSEY": 2,
            "AIPOM": 2,
            "GIRAFARIG": 2,
            "MILTANK": 2,
            "BULBASAUR": 2,
            "CHARMANDER": 2,
            "SQUIRTLE": 2,
            "CHIKORITA": 2,
            "CYNDAQUIL": 2,
            "TOTODILE": 2,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "SPINARAK": 2,
            "LEDYBA": 2,
            "WEEDLE": 2,
            "CATERPIE": 2,
            "PINECO": 2,
            "SHUCKLE": 2,
            "PIDGEY": 1,
            "RATTATA": 1,
            "SENTRET": 1,
            "HOOTHOOT": 1,
            "HOUNDOUR": 2,
            "MR_MIME": 2,
            "LICKITUNG": 2,
            "PORYGON": 2,
            "DITTO": 2,
            "SNORLAX": 2,
            "OMANYTE": 2,
            "KABUTO": 2,
            "AERODACTYL": 12,
            "TANGELA": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "LARVITAR": 2,
            "DUNSPARCE": 12,
            "GLIGAR": 12,
            "SNUBBULL": 2,
            "DELIBIRD": 2,
            "SUNKERN": 2,
            "YANMA": 2,
            "SMEARGLE": 12,
            "TYROGUE": 2,
        },
    },
    "Safari4": {
        "species": {
            "NIDORAN_F": 2,
            "NIDORAN_M": 2,
            "PARAS": 2,
            "DODUO": 2,
            "ODDISH": 2,
            "BELLSPROUT": 2,
            "VENONAT": 2,
            "EXEGGCUTE": 12,
            "CUBONE": 2,
            "RHYHORN": 2,
            "KANGASKHAN": 12,
            "SCYTHER": 2,
            "PINSIR": 2,
            "HERACROSS": 12,
            "WOBBUFFET": 2,
            "TAUROS": 2,
            "MILTANK": 12,
            "STANTLER": 2,
            "CHANSEY": 12,
            "AIPOM": 2,
            "GIRAFARIG": 12,
            "MILTANK": 2,
            "BULBASAUR": 2,
            "CHARMANDER": 2,
            "SQUIRTLE": 2,
            "CHIKORITA": 2,
            "CYNDAQUIL": 2,
            "TOTODILE": 2,
            "EEVEE": 2,
            "PICHU": 2,
            "TOGEPI": 2,
            "SPINARAK": 2,
            "LEDYBA": 2,
            "WEEDLE": 2,
            "CATERPIE": 2,
            "PINECO": 2,
            "SHUCKLE": 2,
            "PIDGEY": 1,
            "RATTATA": 1,
            "SENTRET": 1,
            "HOOTHOOT": 1,
            "HOUNDOUR": 2,
            "MR_MIME": 2,
            "LICKITUNG": 2,
            "PORYGON": 2,
            "DITTO": 2,
            "SNORLAX": 2,
            "OMANYTE": 2,
            "KABUTO": 2,
            "AERODACTYL": 12,
            "TANGELA": 2,
            "CLEFFA": 2,
            "IGGLYBUFF": 2,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "LARVITAR": 2,
            "DUNSPARCE": 2,
            "GLIGAR": 2,
            "SNUBBULL": 2,
            "DELIBIRD": 2,
            "SUNKERN": 2,
            "YANMA": 2,
            "SMEARGLE": 2,
            "TYROGUE": 2,
        },
    },
    "SafariSurf": {
        "species": {
            "PSYDUCK": 2,
            "SLOWPOKE": 2,
            "WOOPER": 2,
            "TOTODILE": 2,
            "SQUIRTLE": 2,
            "DRATINI": 3,
            "OMANYTE": 2,
            "KABUTO": 2,
            "POLIWAG": 2,
            "GOLDEEN": 2,
            "STARYU": 2,
            "HORSEA": 2,
            "SEEL": 2,
            "SHELLDER": 2,
            "MARILL": 2,
            "LAPRAS": 3,
            "REMORAID": 2,
            "KRABBY": 1,
            "CORSOLA": 1,
        },
    },
    "SafariFish": {
        "species": {
            "MAGIKARP": 3,
            "POLIWAG": 2,
            "GOLDEEN": 2,
            "PSYDUCK": 2,
            "SLOWPOKE": 2,
            "DRATINI": 2,
            "KRABBY": 2,
            "HORSEA": 2,
            "REMORAID": 2,
            "CORSOLA": 2,
            "CHINCHOU": 2,
        },
    },
    "PowerPlant": {
        "species": {
            "PICHU": 2,
            "MAGNEMITE": 4,
            "VOLTORB": 4,
            "ELEKID": 3,
            "MAGBY": 1,
            "EEVEE": 2,
            "GRIMER": 2,
            "KOFFING": 2,
            "DITTO": 2,
            "PORYGON": 3,
            "MR_MIME": 2,
            "LICKITUNG": 2,
            "ABRA": 2,
            "UNOWN": 2,
        },
    },
    "CeruleanCave": {
        "species": {
            "EKANS": 2,
            "PICHU": 1,
            "SANDSHREW": 2,
            "ZUBAT": 2,
            "PARAS": 2,
            "PICHU": 2,
            "EEVEE": 2,
            "VENONAT": 2,
            "ABRA": 2,
            "MAGNEMITE": 2,
            "DODUO": 2,
            "DROWZEE": 2,
            "VOLTORB": 2,
            "CUBONE": 2,
            "LICKITUNG": 2,
            "BELLSPROUT": 2,
            "ODDISH": 2,
            "HOUNDOUR": 2,
            "AERODACTYL": 4,
            "UNOWN": 4,
            "WOBBUFFET": 4,
            "KABUTO": 4,
            "OMANYTE": 4,
            "RHYHORN": 2,
            "CHANSEY": 2,
            "DITTO": 2,
            "IGGLYBUFF": 1,
            "PORYGON": 2,
            "GASTLY": 2,
            "MISDREAVUS": 2,
            "MURKROW": 2,
            "LARVITAR": 3,
            "ELEKID": 2,
            "MAGBY": 2,
            "SMOOCHUM": 2,
            "TANGELA": 2,
            "MR_MIME": 2,
            "SCYTHER": 2,
            "PINSIR": 2,
            "HERACROSS": 2,
            "SNORLAX": 2,
            "KANGASKHAN": 2,
            "FARFETCHD": 2,
            "SLOWPOKE": 2,
        },
    },
}

# List of maps that are unlocked pre-Sevii Islands
KANTO_MAP_LOCS = [
    "MAP_VIRIDIAN_FOREST",
    "MAP_MT_MOON_1F",
    "MAP_MT_MOON_B1F",
    "MAP_MT_MOON_B2F",
    "MAP_SSANNE_EXTERIOR",
    "MAP_DIGLETTS_CAVE_B1F",
    "MAP_VICTORY_ROAD_1F",
    "MAP_VICTORY_ROAD_2F",
    "MAP_VICTORY_ROAD_3F",
    "MAP_POKEMON_MANSION_1F",
    "MAP_POKEMON_MANSION_2F",
    "MAP_POKEMON_MANSION_3F",
    "MAP_POKEMON_MANSION_B1F",
    "MAP_SAFARI_ZONE_CENTER",
    "MAP_SAFARI_ZONE_EAST",
    "MAP_SAFARI_ZONE_NORTH",
    "MAP_SAFARI_ZONE_WEST",
    "MAP_CERULEAN_CAVE_1F",
    "MAP_CERULEAN_CAVE_2F",
    "MAP_CERULEAN_CAVE_B1F",
    "MAP_ROCK_TUNNEL_1F",
    "MAP_ROCK_TUNNEL_B1F",
    "MAP_SEAFOAM_ISLANDS_1F",
    "MAP_SEAFOAM_ISLANDS_B1F",
    "MAP_SEAFOAM_ISLANDS_B2F",
    "MAP_SEAFOAM_ISLANDS_B3F",
    "MAP_SEAFOAM_ISLANDS_B4F",
    "MAP_POKEMON_TOWER_3F",
    "MAP_POKEMON_TOWER_4F",
    "MAP_POKEMON_TOWER_5F",
    "MAP_POKEMON_TOWER_6F",
    "MAP_POKEMON_TOWER_7F",
    "MAP_ROUTE1",
    "MAP_ROUTE2",
    "MAP_ROUTE3",
    "MAP_ROUTE4",
    "MAP_ROUTE5",
    "MAP_ROUTE6",
    "MAP_ROUTE7",
    "MAP_ROUTE8",
    "MAP_ROUTE9",
    "MAP_ROUTE10",
    "MAP_ROUTE11",
    "MAP_ROUTE12",
    "MAP_ROUTE13",
    "MAP_ROUTE14",
    "MAP_ROUTE15",
    "MAP_ROUTE16",
    "MAP_ROUTE17",
    "MAP_ROUTE18",
    "MAP_ROUTE19",
    "MAP_ROUTE20",
    "MAP_ROUTE21_NORTH",
    "MAP_ROUTE21_SOUTH",
    "MAP_ROUTE22",
    "MAP_ROUTE23",
    "MAP_ROUTE24",
    "MAP_ROUTE25",
    "MAP_PALLET_TOWN",
    "MAP_VIRIDIAN_CITY",
    "MAP_CERULEAN_CITY",
    "MAP_VERMILION_CITY",
    "MAP_CELADON_CITY",
    "MAP_FUCHSIA_CITY",
    "MAP_CINNABAR_ISLAND",
    "MAP_POWER_PLANT",
    # Sevii Islands accessible pre-Elite Four
    "MAP_MT_EMBER_EXTERIOR",
    "MAP_MT_EMBER_SUMMIT_PATH_1F",
    "MAP_MT_EMBER_SUMMIT_PATH_2F",
    "MAP_MT_EMBER_SUMMIT_PATH_3F",
    "MAP_THREE_ISLAND_BERRY_FOREST",
    "MAP_ONE_ISLAND_KINDLE_ROAD",
    "MAP_ONE_ISLAND_TREASURE_BEACH",
    "MAP_TWO_ISLAND_CAPE_BRINK",
    "MAP_THREE_ISLAND_BOND_BRIDGE",
    "MAP_THREE_ISLAND_PORT",
    "MAP_ONE_ISLAND",
    "MAP_FOUR_ISLAND",
    "MAP_FIVE_ISLAND",
]

# List of maps that are unlocked post-Sevii Islands
POSTGAME_SEVII_MAP_LOCS = [
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_MONEAN_CHAMBER",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_LIPTOO_CHAMBER",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_WEEPTH_CHAMBER",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_DILFORD_CHAMBER",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_SCUFIB_CHAMBER",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_RIXY_CHAMBER",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS_VIAPOIS_CHAMBER",
    "MAP_MT_EMBER_RUBY_PATH_1F",
    "MAP_MT_EMBER_RUBY_PATH_B1F",
    "MAP_MT_EMBER_RUBY_PATH_B2F",
    "MAP_MT_EMBER_RUBY_PATH_B3F",
    "MAP_MT_EMBER_RUBY_PATH_B1F_STAIRS",
    "MAP_MT_EMBER_RUBY_PATH_B2F_STAIRS",
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_ENTRANCE",
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_1F",
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_B1F",
    "MAP_FOUR_ISLAND_ICEFALL_CAVE_BACK",
    "MAP_SIX_ISLAND_PATTERN_BUSH",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM1",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM2",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM3",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM4",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM5",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM6",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM7",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM8",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM9",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM10",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM11",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM12",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM13",
    "MAP_FIVE_ISLAND_LOST_CAVE_ROOM14",
    "MAP_FIVE_ISLAND_RESORT_GORGEOUS",
    "MAP_FIVE_ISLAND_WATER_LABYRINTH",
    "MAP_FIVE_ISLAND_MEADOW",
    "MAP_FIVE_ISLAND_MEMORIAL_PILLAR",
    "MAP_SIX_ISLAND_OUTCAST_ISLAND",
    "MAP_SIX_ISLAND_GREEN_PATH",
    "MAP_SIX_ISLAND_WATER_PATH",
    "MAP_SIX_ISLAND_RUIN_VALLEY",
    "MAP_SEVEN_ISLAND_TRAINER_TOWER",
    "MAP_SEVEN_ISLAND_SEVAULT_CANYON_ENTRANCE",
    "MAP_SEVEN_ISLAND_SEVAULT_CANYON",
    "MAP_SEVEN_ISLAND_TANOBY_RUINS",
    "MAP_SIX_ISLAND_ALTERING_CAVE",
]

def is_pre_elite_four(map_name):
    """
    Checks if a given map is unlocked before beating the Elite Four.
    
    Args:
        map_name: The name of the map to check.
        
    Returns:
        True if the map is unlocked before beating the Elite Four, False otherwise.
    """
    return map_name in KANTO_MAP_LOCS

def get_evolution_stage(base_pokemon, level):
    """
    Determines the evolution stage of a Pokemon based on its level.

    Args:
        base_pokemon: The base form of the Pokemon (e.g., "BULBASAUR").
        level: The current level of the Pokemon.

    Returns:
        The species name of the evolved Pokemon, or the base form if no evolution is needed.
    """
    
    # Define the evolution levels for each Pokemon.
    # This is a simplified example and may need to be expanded.
    # Here, evolution corresponds to whether or not we "evolve"
    # a stage in the encounter table.
    # The level caps are set differently as a result.
    evolution_data = {
        "BULBASAUR": {"next_stage": "IVYSAUR", "level": 22},
        "IVYSAUR": {"next_stage": "VENUSAUR", "level": 44},
        "CHARMANDER": {"next_stage": "CHARMELEON", "level": 22},
        "CHARMELEON": {"next_stage": "CHARIZARD", "level": 44},
        "SQUIRTLE": {"next_stage": "WARTORTLE", "level": 22},
        "WARTORTLE": {"next_stage": "BLASTOISE", "level": 44},
        "CATERPIE": {"next_stage": "METAPOD", "level": 8},
        "METAPOD": {"next_stage": "BUTTERFREE", "level": 18},
        "WEEDLE": {"next_stage": "KAKUNA", "level": 8},
        "KAKUNA": {"next_stage": "BEEDRILL", "level": 18},
        "PIDGEY": {"next_stage": "PIDGEOTTO", "level": 22},
        "PIDGEOTTO": {"next_stage": "PIDGEOT", "level": 44},
        "RATTATA": {"next_stage": "RATICATE", "level": 25},
        "SPEAROW": {"next_stage": "FEAROW", "level": 28},
        "EKANS": {"next_stage": "ARBOK", "level": 32},
        "PICHU": {"next_stage": "PIKACHU", "level": 5},
        "PIKACHU": {"next_stage": "RAICHU", "level": 35},
        "CLEFFA": {"next_stage": "CLEFAIRY", "level": 5},
        "CLEFAIRY": {"next_stage": "CLEFABLE", "level": 30},
        "IGGLYBUFF": {"next_stage": "JIGGLYPUFF", "level": 5},
        "JIGGLYPUFF": {"next_stage": "WIGGLYTUFF", "level": 30},
        "SANDSHREW": {"next_stage": "SANDSLASH", "level": 38},
        "NIDORAN_F": {"next_stage": "NIDORINA", "level": 22},
        "NIDORINA": {"next_stage": "NIDOQUEEN", "level": 48},
        "NIDORAN_M": {"next_stage": "NIDORINO", "level": 22},
        "NIDORINO": {"next_stage": "NIDOKING", "level": 48},
        "VULPIX": {"next_stage": "NINETALES", "level": 40},
        "ZUBAT": {"next_stage": "GOLBAT", "level": 28},
        "GOLBAT": {"next_stage": "CROBAT", "level": 48},
        "ODDISH": {"next_stage": "GLOOM", "level": 29},
        "GLOOM": {"next_stage": "VILEPLUME", "next_stage2": "BELLOSSOM", "level": 48},
        "PARAS": {"next_stage": "PARASECT", "level": 36},
        "VENONAT": {"next_stage": "VENOMOTH", "level": 38},
        "DIGLETT": {"next_stage": "DUGTRIO", "level": 30},
        "MEOWTH": {"next_stage": "PERSIAN", "level": 35},
        "PSYDUCK": {"next_stage": "GOLDUCK", "level": 38},
        "MANKEY": {"next_stage": "PRIMEAPE", "level": 40},
        "GROWLITHE": {"next_stage": "ARCANINE", "level": 50},
        "POLIWAG": {"next_stage": "POLIWHIRL", "level": 25},
        "POLIWHIRL": {"next_stage": "POLIWRATH", "next_stage2": "POLITOED", "level": 48},
        "ABRA": {"next_stage": "KADABRA", "level": 16},
        "KADABRA": {"next_stage": "ALAKAZAM", "level": 50},
        "MACHOP": {"next_stage": "MACHOKE", "level": 32},
        "MACHOKE": {"next_stage": "MACHAMP", "level": 50},
        "BELLSPROUT": {"next_stage": "WEEPINBELL", "level": 28},
        "WEEPINBELL": {"next_stage": "VICTREEBEL", "level": 44},
        "TENTACOOL": {"next_stage": "TENTACRUEL", "level": 35},
        "GEODUDE": {"next_stage": "GRAVELER", "level": 26},
        "GRAVELER": {"next_stage": "GOLEM", "level": 48},
        "PONYTA": {"next_stage": "RAPIDASH", "level": 45},
        "SLOWPOKE": {"next_stage": "SLOWBRO", "level": 42},
        "MAGNEMITE": {"next_stage": "MAGNETON", "level": 38},
        "DODUO": {"next_stage": "DODRIO", "level": 36},
        "SEEL": {"next_stage": "DEWGONG", "level": 36},
        "GRIMER": {"next_stage": "MUK", "level": 35},
        "SHELLDER": {"next_stage": "CLOYSTER", "level": 39},
        "GASTLY": {"next_stage": "HAUNTER", "level": 24},
        "HAUNTER": {"next_stage": "GENGAR", "level": 45},
        "ONIX": {"next_stage": "STEELIX", "level": 50},
        "DROWZEE": {"next_stage": "HYPNO", "level": 36},
        "KRABBY": {"next_stage": "KINGLER", "level": 33},
        "VOLTORB": {"next_stage": "ELECTRODE", "level": 35},
        "EXEGGCUTE": {"next_stage": "EXEGGUTOR", "level": 42},
        "CUBONE": {"next_stage": "MAROWAK", "level": 36},
        "KOFFING": {"next_stage": "WEEZING", "level": 38},
        "CHANSEY": {"next_stage": "BLISSEY", "level": 45},
        "RHYHORN": {"next_stage": "RHYDON", "level": 48},
        "HORSEA": {"next_stage": "SEADRA", "level": 29},
        "SEADRA": {"next_stage": "KINGDRA", "level": 50},
        "GOLDEEN": {"next_stage": "SEAKING", "level": 28},
        "STARYU": {"next_stage": "STARMIE", "level": 45},
        "SCYTHER": {"next_stage": "SCIZOR", "level": 48},
        "MAGIKARP": {"next_stage": "GYARADOS", "level": 35},
        "EEVEE": {"next_stage": "VAPOREON", "level": 101}, # No Eevee evolutions in the wild.
        "OMANYTE": {"next_stage": "OMASTAR", "level": 45},
        "KABUTO": {"next_stage": "KABUTOPS", "level": 45},
        "DRATINI": {"next_stage": "DRAGONAIR", "level": 40},
        "DRAGONAIR": {"next_stage": "DRAGONITE", "level": 50},
        "CHIKORITA": {"next_stage": "BAYLEEF", "level": 22},
        "BAYLEEF": {"next_stage": "MEGANIUM", "level": 44},
        "CYNDAQUIL": {"next_stage": "QUILAVA", "level": 22},
        "QUILAVA": {"next_stage": "TYPHLOSION", "level": 44},
        "TOTODILE": {"next_stage": "CROCONAW", "level": 22},
        "CROCONAW": {"next_stage": "FERALIGATR", "level": 44},
        "SENTRET": {"next_stage": "FURRET", "level": 18},
        "HOOTHOOT": {"next_stage": "NOCTOWL", "level": 24},
        "LEDYBA": {"next_stage": "LEDIAN", "level": 22},
        "PINECO": {"next_stage": "FORRETRESS", "level": 35},
        "SPINARAK": {"next_stage": "ARIADOS", "level": 26},
        "CHINCHOU": {"next_stage": "LANTURN", "level": 33},
        "TOGEPI": {"next_stage": "TOGETIC", "level": 45},
        "NATU": {"next_stage": "XATU", "level": 30},
        "MAREEP": {"next_stage": "FLAAFFY", "level": 22},
        "FLAAFFY": {"next_stage": "AMPHAROS", "level": 38},
        "MARILL": {"next_stage": "AZUMARILL", "level": 24},
        "HOPPIP": {"next_stage": "SKIPLOOM", "level": 24},
        "SKIPLOOM": {"next_stage": "JUMPLUFF", "level": 35},
        "SUNKERN": {"next_stage": "SUNFLORA", "level": 29},
        "WOOPER": {"next_stage": "QUAGSIRE", "level": 28},
        "SNUBBULL": {"next_stage": "GRANBULL", "level": 28},
        "TEDDIURSA": {"next_stage": "URSARING", "level": 39},
        "SLUGMA": {"next_stage": "MAGCARGO", "level": 35},
        "SWINUB": {"next_stage": "PILOSWINE", "level": 35},
        "REMORAID": {"next_stage": "OCTILLERY", "level": 30},
        "HOUNDOUR": {"next_stage": "HOUNDOOM", "level": 30},
        "PHANPY": {"next_stage": "DONPHAN", "level": 30},
        "PORYGON": {"next_stage": "PORYGON2", "level": 40},
        "TYROGUE": {"next_stage": "HITMONLEE", "next_stage2": "HITMONCHAN", "next_stage3": "HITMONTOP", "level": 35},
        "SMOOCHUM": {"next_stage": "JYNX", "level": 22},
        "ELEKID": {"next_stage": "ELECTABUZZ", "level": 22},
        "MAGBY": {"next_stage": "MAGMAR", "level": 22},
        "LARVITAR": {"next_stage": "PUPITAR", "level": 35},
        "PUPITAR": {"next_stage": "TYRANITAR", "level": 60},
    }

    current_pokemon = base_pokemon
    stage = 0
    while current_pokemon in evolution_data and level >= evolution_data[current_pokemon]["level"]:
        if "next_stage2" not in evolution_data[current_pokemon]:
            next_stage = evolution_data[current_pokemon]["next_stage"]
        elif "next_stage3" not in evolution_data[current_pokemon]:
            ns1 = evolution_data[current_pokemon]["next_stage"]
            ns2 = evolution_data[current_pokemon]["next_stage2"]
            if random.random() > 0.5:
                next_stage = ns1
            else:
                next_stage = ns2
        else:
            ns1 = evolution_data[current_pokemon]["next_stage"]
            ns2 = evolution_data[current_pokemon]["next_stage2"]
            ns3 = evolution_data[current_pokemon]["next_stage3"]
            if random.random() < 1./3.:
                next_stage = ns1
            elif random.random() < 2./3.:
                next_stage = ns2
            else:
                next_stage = ns3
        if random.random() > 0.5:
            current_pokemon = next_stage
            stage += 1
        else:
            break

    return current_pokemon

# TODO(kiranv): add checks that all 251 catchable (exclude legends) are present in the current randomized map before postgame.
# If the check fails, make a small number of corrections so that every non-legendary Pokemon in Gen I and II is catchable
# in the encounter table.
# TODO(kiranv): When randomizing, check the level of the encounter. If the encounter level
# is high, consider evolving the base stage to the appropriate form, with some probability.
def randomize_encounters(template_file=habitat_template_path, habitat_mapping=habitat_mapping, output_file=randomized_encounters_path):
    """
    Randomizes the encounters based on the habitat template and mapping,
    now considering encounter weights.

    Args:
        template_file: Path to the habitat template JSON file.
        habitat_mapping: The dictionary mapping habitat types to Pokémon lists with weights.
        output_file: Path to save the randomized encounters JSON file.
    """
    with open(template_file, 'r') as f:
        data = json.load(f)

    # TODO(kiranv): 
    # 1. First sample a unique set of Pokemon that will always have encounters in many 
    #    instances of a given habitat. Like Tentacool, Rattata, Zubat, Pidgey, etc.
    #    These will be used to fill rest of encounter table in a specific map loc.
    # 2. For each new map loc (randomized order), sample (4?) unique Pokemon to show up
    #    (keeping track, so that we fill all Pokemon in dex before elite 4).
    # This will ensure both some homogeneity/ character to sampled region, while having
    # interesting rare encounters.
    # 3. Can choose 2 of unique 4 sampled to be "rare", and 2 to be more common, each time.

    # TODO(kiranv):
    # Sample 4 common encounters for each environment type. These will always be added.
    # Then, after the 4 common encounters are created for each environment type,
    # sample 4 more to fill in.
    # finally, the last 4 slots can be filled in the "missing pokemon" round.

    num_common_pokemon_per_habitat = 4
    common_pokemon = {}
    for habitat_type in habitat_mapping:
        # Sample 4 common pokemon.
        pokemon_data = habitat_mapping[habitat_type]["species"]
        possible_pokemon = list(pokemon_data.keys())
        weights = np.array(list(pokemon_data.values()))
        probs = weights/np.sum(weights)
        chosen_pokemon = np.random.choice(possible_pokemon, size=num_common_pokemon_per_habitat, p=probs, replace=False)
        common_pokemon[habitat_type] = chosen_pokemon.tolist()

    print(f"Common Pokemon per Habitat")
    for key in common_pokemon:
        print(f"{key}: {common_pokemon[key]}")

    # Keep track of Pokemon that have already been assigned to a location.
    pre_elite_four_pokemon = set()

    for group in data["wild_encounter_groups"]:
        for encounter in group["encounters"]:
            print(f"Assigning encounter {encounter}")
            # Check if encounter location is accessible pre-Elite Four.
            is_pre_elite_four_loc = is_pre_elite_four(encounter["map"])
            print(f"Is Pre-E4?: {is_pre_elite_four_loc}")
            for key in ['land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons']:
                if key in encounter:
                    print(f"Assigning key {key}")
                    # List of habitats to sample from.
                    habitat_types = encounter[key]["habitat_types"]
                    print(f"{key} has these habitats: {habitat_types}\n\n")
                    min_level = encounter[key]["min_level"]
                    max_level = encounter[key]["max_level"]

                    # Built possible_pokemon list and weights list.
                    possible_common_pokemon = []
                    possible_pokemon = []
                    weights = []
                    for habitat_type in habitat_types:
                        if habitat_type in habitat_mapping:
                            pokemon_data = habitat_mapping[habitat_type]["species"]
                            possible_common_pokemon.extend(common_pokemon[habitat_type])
                            possible_pokemon.extend(list(pokemon_data.keys()))
                            weights.extend(list(pokemon_data.values()))
                    
                    probs = np.array(weights)/sum(weights)
                    
                    # First sample the 4 common pokemon uniformly.
                    num_common_pokemon = 4
                    sampled_pokemon = []
                    common_sample = np.random.choice(possible_common_pokemon, size=num_common_pokemon, replace=False)
                    print(f"\nCommon Sample: {common_sample}")
                        

                    # Sample 4 more pokemon from general list.
                    # This time we allow for sampling with replacement.
                    four_more = np.random.choice(possible_pokemon, size=4, p=probs, replace=True)
                    print(f"Four more: {four_more}")

                    sampled_pokemon = common_sample.tolist() + four_more.tolist()
                    if is_pre_elite_four_loc:
                        for pokemon in sampled_pokemon:
                            pre_elite_four_pokemon.add(pokemon)
                    
                    print(f"Sampled Pokemon (first 8): {sampled_pokemon}")

                    encounter[key]["mons"] = []
                    for i in range(len(sampled_pokemon)):
                        # Randomly determine the level for this encounter.
                        curr_min_level = random.randint(min_level, max_level)
                        curr_max_level = random.randint(curr_min_level, max_level)
                        # Determine the evolved form based on the level.
                        chosen_pokemon = sampled_pokemon[i]
                        evolved_pokemon = get_evolution_stage(chosen_pokemon, curr_min_level)
                        
                        encounter[key]["mons"].append(
                            {
                                "min_level": curr_min_level,
                                "max_level": curr_max_level,
                                "species": "SPECIES_" + evolved_pokemon.upper(),
                            }
                        )
                    print(f"Final Encounter Table:\n{encounter[key]["mons"]}")
                    print("\n===============================\n")
    
    # Ensure that all non-legendary Pokemon are catchable before the Elite Four.
    all_catchable = set(pokemon_roster)
    missing_pokemon = all_catchable - pre_elite_four_pokemon
    
    # If any are missing, add them to a suitable pre-Elite Four location.
    if missing_pokemon:
        print(f"Warning: {len(missing_pokemon)} Pokemon were not assigned a pre-Elite Four encounter.")
        print(f"Missing Pokemon: {missing_pokemon}")
        for pokemon in missing_pokemon:
            # Find a suitable pre-Elite Four location to add the missing Pokemon.
            added = False
            for group in data["wild_encounter_groups"]:
                if added:
                    break
                for encounter in group["encounters"]:
                    if added:
                        break
                    for key in ['land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons']:
                        if added:
                            break
                        if key in encounter and is_pre_elite_four(encounter["map"]):
                            # Check if adding this Pokemon is appropriate for the habitat.
                            for habitat_type in encounter[key]["habitat_types"]:
                                if pokemon in habitat_mapping[habitat_type]["species"]:
                                    # Add the Pokemon to this encounter.
                                    min_level = encounter[key]["min_level"]
                                    max_level = encounter[key]["max_level"]
                                    curr_min_level = random.randint(min_level, max_level)
                                    curr_max_level = random.randint(curr_min_level, max_level)
                                    evolved_pokemon = get_evolution_stage(pokemon, curr_min_level)
                                    encounter[key]["mons"].append(
                                        {
                                            "min_level": curr_min_level,
                                            "max_level": curr_max_level,
                                            "species": "SPECIES_" + evolved_pokemon.upper(),
                                        }
                                    )
                                    added = True
                                    print(f"Adding {pokemon} to {key} in {encounter}")
                                    pre_elite_four_pokemon.add(pokemon)
                                    break
    # Finally, sample for the missing Pokemon to fill out to 12.
    for group in data["wild_encounter_groups"]:
        for encounter in group["encounters"]:
            # Check if encounter location is accessible pre-Elite Four.
            is_pre_elite_four_loc = is_pre_elite_four(encounter["map"])
            print(f"Is Pre-E4?: {is_pre_elite_four_loc}")
            for key in ['land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons']:
                if key in encounter:
                    curr_mons = encounter[key]["mons"]
                    num_curr_mons = len(curr_mons)
                    print(f"{encounter}-{key} has {num_curr_mons} mons. Sampling the rest.")
                    print(f"Assigning key {key}")
                        
                    # List of habitats to sample from.
                    habitat_types = encounter[key]["habitat_types"]
                    print(f"{key} has these habitats: {habitat_types}\n\n")
                    min_level = encounter[key]["min_level"]
                    max_level = encounter[key]["max_level"]

                    # Built possible_pokemon list and weights list.
                    possible_pokemon = []
                    weights = []
                    for habitat_type in habitat_types:
                        if habitat_type in habitat_mapping:
                            pokemon_data = habitat_mapping[habitat_type]["species"]
                            possible_pokemon.extend(list(pokemon_data.keys()))
                            weights.extend(list(pokemon_data.values()))
                    
                    probs = np.array(weights)/sum(weights)
                    
                    # Sample the remaining pokemon.
                    # This time we allow for sampling with replacement.
                    complete = np.random.choice(possible_pokemon, size=12-num_curr_mons, p=probs, replace=True)
                    complete = complete.tolist()
                    print(f"Complete: {complete}")

                    if is_pre_elite_four_loc:
                        for pokemon in complete:
                            pre_elite_four_pokemon.add(pokemon)
                    

                    for i in range(len(complete)):
                        # Randomly determine the level for this encounter.
                        curr_min_level = random.randint(min_level, max_level)
                        curr_max_level = random.randint(curr_min_level, max_level)
                        # Determine the evolved form based on the level.
                        chosen_pokemon = complete[i]
                        evolved_pokemon = get_evolution_stage(chosen_pokemon, curr_min_level)
                        
                        encounter[key]["mons"].append(
                            {
                                "min_level": curr_min_level,
                                "max_level": curr_max_level,
                                "species": "SPECIES_" + evolved_pokemon.upper(),
                            }
                        )
                    print(f"TRUE Final Encounter Table:\n{encounter[key]["mons"]}")
                    print("\n===============================\n")

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    generate_habitat_template()
    randomize_encounters()