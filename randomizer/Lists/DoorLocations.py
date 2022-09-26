"""Stores the data for each potential T&S and Wrinkly door location."""
from randomizer.Enums.Events import Events
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Time import Time
from randomizer.Enums.Kongs import Kongs


class DoorData:
    """Stores information about a door location."""

    def __init__(
        self,
        *,
        name="",
        map=0,
        logicregion="",
        location=[0, 0, 0, 0],
        rx=0,
        rz=0,
        kong_lst=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        tough_spot=False,
        enabled=False,
        scale=1,
        logic=0
    ):
        """Initialize with provided data."""
        self.name = name
        self.map = map
        self.location = location
        self.logicregion = logicregion
        self.rx = rx
        self.rz = rz
        self.kongs = kong_lst
        self.scale = scale
        self.logic = logic
        self.placed = False
        self.assigned_kong = None
        self.tough_spot = tough_spot
        self.enabled = enabled

    def assignDoor(self, kong):
        """Assign door to kong."""
        self.placed = True
        self.assigned_kong = kong


door_locations = {
    Levels.JungleJapes: [
        DoorData(name="Japes Lobby: Middle Right", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[169.075, 10.833, 594.613, 90], enabled=True),  # DK Door
        DoorData(name="Japes Lobby: Far Left", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[647.565, 0, 791.912, 183], enabled=True),  # Diddy Door
        DoorData(name="Japes Lobby: Close Right", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[156.565, 10.833, 494.73, 98], enabled=True),  # Lanky Door
        DoorData(name="Japes Lobby: Far Right", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[252.558, 0, 760.733, 163], enabled=True),  # Tiny Door
        DoorData(name="Japes Lobby: Close Left", map=Maps.JungleJapesLobby, logicregion=Regions.JungleJapesLobby, location=[821.85, 0, 615.167, 264], enabled=True),  # Chunky Door
    ],
    Levels.AngryAztec: [
        DoorData(name="Aztec Lobby: Pillar Wall", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[499.179, 0, 146.628, 0], enabled=True),  # DK Door
        DoorData(name="Aztec Lobby: Lower Right", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[441.456, 0, 614.029, 180], enabled=True),  # Diddy Door
        DoorData(name="Aztec Lobby: Left of Portal", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[628.762, 80, 713.93, 177], enabled=True),  # Lanky Door
        DoorData(name="Aztec Lobby: Right of Portal", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[377.124, 80, 712.484, 179], enabled=True),  # Tiny Door
        DoorData(name="Aztec Lobby: Behind Feather Door", map=Maps.AngryAztecLobby, logicregion=Regions.AngryAztecLobby, location=[1070.018, 0, 738.609, 190], enabled=True),  # Custom Chunky Door
        DoorData(name="Next to Candy - right", map=Maps.AngryAztec, logicregion=Regions.AngryAztecStart, location=[2468, 120, 473.5, 298.75]),
    ],
    Levels.FranticFactory: [
        DoorData(name="Factory Lobby: Low Left", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[544.362, 0, 660.802, 182], enabled=True),  # DK Door
        DoorData(name="Factory Lobby: Top Left", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[660.685, 133.5, 660.774, 182], enabled=True),  # Diddy Door
        DoorData(name="Factory Lobby: Top Center", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[468.047, 85.833, 662.907, 180], enabled=True),  # Lanky Door
        DoorData(name="Factory Lobby: Top Right", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[275.533, 133.5, 661.908, 180], enabled=True),  # Tiny Door
        DoorData(name="Factory Lobby: Low Right", map=Maps.FranticFactoryLobby, logicregion=Regions.FranticFactoryLobby, location=[393.114, 0, 662.562, 182], enabled=True),  # Chunky Door
        DoorData(name="Crusher Room - start", map=Maps.FactoryCrusher, logicregion=Regions.FranticFactoryLobby, location=[475, 0, 539, 180], enabled=True),
    ],
    Levels.GloomyGalleon: [
        DoorData(name="Galleon Lobby: Far Left", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[1022.133, 139.667, 846.41, 276], enabled=True),  # DK Door
        DoorData(name="Galleon Lobby: Far Right", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[345.039, 139.667, 884.162, 92], enabled=True),  # Diddy Door
        DoorData(name="Galleon Lobby: Close Right", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[464.68, 159.667, 1069.446, 161], enabled=True),  # Lanky Door
        DoorData(name="Galleon Lobby: Near DK Portal", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[582.36, 159.667, 1088.258, 180], enabled=True),  # Tiny Door
        DoorData(name="Galleon Lobby: Close Left", map=Maps.GloomyGalleonLobby, logicregion=Regions.GloomyGalleonLobby, location=[876.388, 178.667, 1063.828, 192], enabled=True),  # Chunky Door
        DoorData(name="Treasure Chest Exterior", map=Maps.GloomyGalleon, logicregion=Regions.TreasureRoom, location=[1938, 1440, 524, 330]),
        DoorData(name="Next to Warp 3 in Cranky's Area", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[3071, 1890, 2838, 0]),
        DoorData(name="In Primate Punch Chest Room - right", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[3460, 1670, 4001, 180]),
        DoorData(name="Next to Cannonball game", map=Maps.GloomyGalleon, logicregion=Regions.GalleonBeyondPineappleGate, location=[1334, 1610, 2523, 0], logic=lambda l: Events.WaterSwitch in l.Events),
        DoorData(name="Music Cactus - bottom front left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4239, 1289, 880, 38.31]),
        DoorData(name="Music Cactus - bottom back left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4444, 1290, 803, 307.7]),
        DoorData(name="Music Cactus - bottom front right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4524, 1290, 1145, 218.31]),
        DoorData(name="Music Cactus - bottom back right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[4587, 1290, 972, 307.85]),
        DoorData(name="In hallway to Shipyard - Tiny switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2205, 1620, 2700, 90]),
        DoorData(name="In hallway to Shipyard - Lanky switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2615, 1620, 2844, 302]),
        DoorData(name="In hallway to Primate Punch Chests", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[3007, 1670, 3866, 135.42]),
        DoorData(name="Under Baboon Blast pad", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[1674.5, 1610, 4042.5, 261.15]),
        DoorData(name="Under RocketBarrel barrel", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[1360, 1609, 4048, 86]),
        DoorData(name="Next to Coconut switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2065.75, 1628, 3418.75, 28]),
        DoorData(name="Entrance Tunnel - near entrance", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2112, 1628, 3223, 135]),
        DoorData(name="Next to Peanut switch", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2462, 1619, 2688, 270]),
        DoorData(name="Tiny's 5D ship", map=Maps.Galleon5DShipDKTiny, logicregion=Regions.SaxophoneShip, location=[735, 0, 1336, 270], kong_lst=[Kongs.tiny]),
        DoorData(name="Lanky's 5D ship", map=Maps.Galleon5DShipDiddyLankyChunky, logicregion=Regions.TromboneShip, location=[1099, 0, 1051, 270], kong_lst=[Kongs.lanky]),
        DoorData(name="Behind Chunky punch gate in Cranky Area", map=Maps.GloomyGalleon, location=[3275, 1670, 2353.65, 13.65], kong_lst=[Kongs.chunky], logic=lambda l: l.punch),
        DoorData(name="Lighthouse Interior", map=Maps.GalleonLighthouse, logicregion=Regions.Lighthouse, location=[508, 200, 409, 135.2], kong_lst=[Kongs.donkey]),
        DoorData(name="Low water alcove in lighthouse area", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[540.3, 1564, 4094, 110]),
        DoorData(name="Behind boxes in Cranky Area", map=Maps.GloomyGalleon, logicregion=Regions.GloomyGalleonStart, location=[2891.5, 1688, 3493, 124]),
        DoorData(name="Lanky's 2D ship", map=Maps.Galleon2DShip, logicregion=Regions.LankyShip, location=[1616, 0, 939, 179.5], kong_lst=[Kongs.lanky]),
        DoorData(name="Mech Fish Gate - far left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[2651, 140.5, 503, 92]),
        DoorData(name="Mech Fish Gate - left", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[2792, 175, 299.3, 15.9], rz=7.3),
        DoorData(name="Mech Fish Gate - middle", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[3225, 205, 303, 329], rz=-4.7),
        DoorData(name="Mech Fish Gate - right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[3406, 166, 531, 260], rx=290, rz=-290),
        DoorData(name="Mech Fish Gate - far right", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[3310, 147, 828, 216.5], rx=16, rz=-16),
        DoorData(name="Cannonball Area Exit", map=Maps.GloomyGalleon, logicregion=Regions.GalleonBeyondPineappleGate, location=[1524.1, 1461, 2898, 278]),
        DoorData(name="2Dship's secret 3rd door", map=Maps.GloomyGalleon, logicregion=Regions.Shipyard, location=[1109, 1189.9, 1978, 95], rz=-47, enabled=True),
        DoorData(name="In Mermaid's Palace", map=Maps.GalleonMermaidRoom, logicregion=Regions.MermaidRoom, location=[274, 0, 481, 150], kong_lst=[Kongs.tiny]),
        DoorData(name="Near Mermaid's Palace - right", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[1445, 141, 4859, 180]),
        DoorData(name="Near Mermaid's Palace - left", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[1400, 112.8, 4215, 346.5], rz=3),
        DoorData(name="Near Mermaid's Palace - Under Tag Barrel", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[915, 164, 3967, 30], rx=7, rz=3, enabled=True),
        DoorData(name="On top of Seal cage", map=Maps.GloomyGalleon, logicregion=Regions.LighthouseArea, location=[2238, 1837, 4099, 251.7], kong_lst=[Kongs.diddy], logic=lambda l: l.jetpack, tough_spot=True),
    ],
    Levels.FungiForest: [
        DoorData(name="Fungi Lobby: On High Box", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[449.866, 45.922, 254.6, 270], enabled=True),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near Gorilla Gone Door", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[136.842, 0, 669.81, 90], enabled=True),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Opposite Gorilla Gone Door", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[450.219, 0, 689.048, 270], enabled=True),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near B. Locker", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[293, 0, 154.197, 0], enabled=True, scale=1.2),  # Custom Location (Removing Wheel)
        DoorData(name="Fungi Lobby: Near Entrance", map=Maps.FungiForestLobby, logicregion=Regions.FungiForestLobby, location=[450.862, 0, 565.029, 270], enabled=True),  # Custom Location (Removing Wheel)
    ],
    Levels.CrystalCaves: [
        DoorData(name="Caves Lobby: Far Left", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[1103.665, 146.5, 823.872, 194], enabled=True),  # DK Door
        DoorData(name="Caves Lobby: Top Ledge", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[731.84, 280.5, 704.935, 120], enabled=True, kong_lst=[Kongs.diddy]),  # Diddy Door
        DoorData(name="Caves Lobby: Near Left", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[1046.523, 13.5, 476.611, 189], enabled=True),  # Lanky Door
        DoorData(name="Caves Lobby: Far Right", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[955.407, 146.664, 843.472, 187], enabled=True),  # Tiny Door
        DoorData(name="Caves Lobby: Near Right", map=Maps.CrystalCavesLobby, logicregion=Regions.CrystalCavesLobby, location=[881.545, 13.466, 508.666, 193], enabled=True),  # Chunky Door
        DoorData(name="Outside Lanky's Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2400, 276, 1892.5, 21.75], rx=0, rz=0, enabled=True),
        DoorData(name="Outside Chunky's Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3515.65, 175, 1893, 273.7], rx=0, rz=0, enabled=True),
        DoorData(name="Outside Diddy's Lower Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3697.5, 260, 1505, 291], rx=0, rz=0, enabled=True),
        DoorData(name="Outside Diddy's Upper Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3666.7, 343, 1762, 273.8], rx=0, rz=0, enabled=True),
        DoorData(name="Under the Waterfall (Cabin Area)", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2230, 0, 2178, 100], rx=0, rz=0, enabled=True),
        DoorData(name="Across from the 5Door Cabin", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2970, 128, 1499, 68.5], rx=9, rz=11, enabled=True),
        DoorData(name="5Door Igloo - DK's right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[585, 48, 1396, 5], scale=0.95, enabled=True),
        DoorData(name="5Door Igloo - Diddy's right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[684.9, 48, 1312, 75], scale=0.95, enabled=True),
        DoorData(name="5Door Igloo - Tiny's right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[635, 48, 1190, 148], scale=0.95, enabled=True),
        DoorData(name="5Door Igloo - Chunky's right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[504.5, 48, 1200, 220.3], scale=0.95, enabled=True),
        DoorData(name="5Door Igloo - Lanky's right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[473.1, 48, 1327, 292.7], scale=0.95, enabled=True),
        DoorData(name="Ice Castle Area - Near Rock Switch", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1349.6, 330, 1079, 86.7], rx=4, rz=0, enabled=True),
        DoorData(name="In Chunky's 5Door Cabin on a Book Shelf", map=Maps.CavesChunkyCabin, logicregion=Regions.ChunkyCabin, location=[403.5, 44, 579, 180], rx=0, rz=0, kong_lst=[Kongs.chunky], enabled=True),
        DoorData(name="Between Funky and Ice Castle - on land", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2240.65, 65.8, 1185, 89.25], rx=0, rz=0, enabled=True),
        DoorData(name="Between Funky and Ice Castle - underwater", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2370, 0, 1096, 196], rx=0, rz=0, enabled=True),
        DoorData(name="In Water Near W4 Opposite Cranky - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1187, 0, 2410, 133.5], rx=0, rz=0, enabled=True),
        DoorData(name="In Water Near W4 Opposite Cranky - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1441, 0, 2385, 208], rx=0, rz=0, enabled=True),
        DoorData(name="Under Bridge to Cranky", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1140, 0, 1704, 350.4], rx=0, rz=0, enabled=True),
        DoorData(name="Under Handstand Slope", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1272, 93, 1291, 75], rx=0, rz=0),
        DoorData(name="Mini Monkey Ledge", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3110, 257, 1142, 265], rx=0, rz=0),
        DoorData(name="Across from Snide", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1819, 85, 1437, 218], rx=0, rz=0),
        DoorData(name="Slope to Cranky with Mini Monkey Hole", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1047, 190, 2418, 175], rx=0, rz=0),
        DoorData(name="Level Entrance - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1812, -29, 342, 224.5], rx=0, rz=0),
        DoorData(name="Level Entrance - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[1820, -29, 97, 315], rx=0, rz=0),
        DoorData(name="Ice Castle - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2184, 343, 992, 315], rx=0, rz=0),
        DoorData(name="Ice Castle - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2227, 343, 951, 131], rx=0, rz=0),
        DoorData(name="Igloo Area - left of entrance", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[637, 2, 1593, 176], rx=0, rz=0),
        DoorData(name="Igloo Area - Behind Tag Barrel Island", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[168, 1, 1565, 124], rx=0, rz=0),
        DoorData(name="Igloo Area - Behind Warp 1", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[290, 1, 901, 53.43], rx=0, rz=0),
        DoorData(name="Igloo Area - right of entrance", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[941, 2, 1222, 270], rx=0, rz=0),
        DoorData(name="Under Funky's Store", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[2876, 2, 1236, 112.6], rx=0, rz=0),
        DoorData(name="Next to Waterfall that's Next to Funky", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3082, 1, 1262, 270], rx=0, rz=0),
        DoorData(name="In Water Under Funky - left", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3029, 2, 671, 4.5], rx=0, rz=0),
        DoorData(name="In Water Under Funky - center", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3207, 1, 820, 294.6], rx=0, rz=0),
        DoorData(name="In Water Under Funky - right", map=Maps.CrystalCaves, logicregion=Regions.CrystalCavesMain, location=[3199, 2, 952, 257], rx=0, rz=0),
    ],
    Levels.CreepyCastle: [
        DoorData(name="Castle Lobby: Central Pillar (1)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[499.978, 71.833, 634.25, 240], enabled=True),  # DK Door
        DoorData(name="Castle Lobby: Central Pillar (2)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[499.545, 71.833, 725.653, 300], enabled=True),  # Diddy Door
        DoorData(name="Castle Lobby: Central Pillar (3)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[661.738, 71.833, 726.433, 60], enabled=True),  # Lanky Door
        DoorData(name="Castle Lobby: Central Pillar (4)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[660.732, 71.833, 635.288, 118], enabled=True),  # Tiny Door
        DoorData(name="Castle Lobby: Central Pillar (5)", map=Maps.CreepyCastleLobby, logicregion=Regions.CreepyCastleLobby, location=[581.215, 71.833, 588.444, 182], enabled=True),  # Chunky Door
    ],
}
