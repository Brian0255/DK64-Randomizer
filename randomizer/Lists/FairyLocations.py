"""Stores the data for each potential fairy location."""

from randomizer.Enums.Levels import Levels
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Events import Events


class Fence:
    """Stores information about a fence."""

    def __init__(self, min_x: int, min_z: int, max_x: int, max_z: int):
        """Initialize with given data."""
        self.min_x = min_x
        self.min_z = min_z
        self.max_x = max_x
        self.max_z = max_z
        self.center_x = int((min_x + max_x) / 2)
        self.center_z = int((min_z + max_z) / 2)


class FairyData:
    """Stores information about a fairy location."""

    def __init__(
        self,
        *,
        name: str = "",
        map: Maps = Maps.Isles,
        region: Regions = Regions.GameStart,
        fence: Fence = None,
        spawn_y: int = 0,
        logic=None,
        is_vanilla: bool = False,
        spawn_xyz: list = None,
        natural_index: int = -1,
        is_5ds_fairy: bool = False,
    ):
        """Initialize with given data."""
        self.name = name
        self.map = map
        self.region = region
        self.fence = fence
        self.spawn_y = spawn_y
        self.logic = lambda l: l.camera
        self.is_5ds_fairy = is_5ds_fairy
        if logic is not None:
            self.logic = logic
        self.is_vanilla = is_vanilla
        if is_vanilla:
            self.spawn_xyz = [0, 0, 0]
            if spawn_xyz is not None:
                self.spawn_xyz = spawn_xyz.copy()
            else:
                self.spawn_xyz = [
                    self.fence.center_x,
                    self.spawn_y,
                    self.fence.center_z,
                ]
        self.natural_index = natural_index


relocated_5ds_fairy = FairyData(
    name="Inside Tiny 5-Door Ship",
    map=Maps.Galleon5DShipDKTiny,
    region=Regions.SaxophoneShip,
    is_vanilla=True,
    fence=Fence(916, 1703, 1217, 1854),
    natural_index=1,
    spawn_y=62,
    is_5ds_fairy=True,
)

original_5ds_fairy = FairyData(
    name="In Tiny's 5-Door Ship",
    map=Maps.Galleon5DShipDKTiny,
    region=Regions.SaxophoneShip,
    is_vanilla=True,
    spawn_xyz=[1089, 62, 2022],
    natural_index=1,
    is_5ds_fairy=True,
)

fairy_locations = {
    Levels.JungleJapes: [
        FairyData(
            name="Rambi Door Pool",
            map=Maps.JungleJapes,
            region=Regions.BeyondRambiGate,
            is_vanilla=True,
            spawn_xyz=[564, 270, 2916],
            natural_index=0,
        ),
        FairyData(
            name="Painting Room",
            map=Maps.JapesLankyCave,
            region=Regions.JapesLankyCave,
            is_vanilla=True,
            spawn_xyz=[210, 174, 391],
            logic=lambda l: (((l.grape or l.trombone) and l.Slam) or l.generalclips) and l.islanky and l.camera,
            natural_index=1,
        ),
        FairyData(
            name="Near Kong Cage",
            map=Maps.JungleJapes,
            region=Regions.JungleJapesMain,
            fence=Fence(1000, 2345, 1206, 2482),
            spawn_y=1040,
        ),
        FairyData(
            name="Near Mountain",
            map=Maps.JungleJapes,
            region=Regions.JungleJapesMain,
            fence=Fence(1300, 1793, 1950, 2162),
            spawn_y=916,
        ),
        FairyData(
            name="Above Underground Entrance",
            map=Maps.JungleJapes,
            region=Regions.JungleJapesMain,
            fence=Fence(2223, 1255, 2524, 1322),
            spawn_y=370,
        ),
        FairyData(
            name="Hive Area",
            map=Maps.JungleJapes,
            region=Regions.JapesBeyondFeatherGate,
            fence=Fence(1934, 3153, 2607, 3207),
            spawn_y=727,
        ),
        FairyData(
            name="Storm Area",
            map=Maps.JungleJapes,
            region=Regions.JapesBeyondCoconutGate2,
            fence=Fence(1450, 3678, 1910, 4280),
            spawn_y=475,
        ),
        FairyData(
            name="Inside Hive",
            map=Maps.JapesTinyHive,
            region=Regions.TinyHive,
            fence=Fence(1259, 1204, 1487, 1603),
            spawn_y=236,
        ),
        FairyData(
            name="Underground Pathway",
            map=Maps.JapesUnderGround,
            region=Regions.JapesCatacomb,
            fence=Fence(886, 524, 903, 1105),
            spawn_y=64,
        ),
        FairyData(
            name="Underground Vine Area",
            map=Maps.JapesUnderGround,
            region=Regions.JapesCatacomb,
            fence=Fence(121, 651, 354, 925),
            spawn_y=53,
        ),
        FairyData(
            name="Mine Entry",
            map=Maps.JapesMountain,
            region=Regions.Mine,
            fence=Fence(717, 274, 724, 646),
            spawn_y=125,
        ),
    ],
    Levels.AngryAztec: [
        FairyData(
            name="Tiny 5-Door Temple",
            map=Maps.AztecTiny5DTemple,
            region=Regions.TinyTemple,
            is_vanilla=True,
            spawn_xyz=[1178, 95, 704],
            logic=lambda l: l.camera and ((l.feather and l.mini and l.istiny) or l.phasewalk),
            natural_index=1,
        ),
        FairyData(
            name="Llama Temple",
            map=Maps.AztecLlamaTemple,
            region=Regions.LlamaTemple,
            is_vanilla=True,
            spawn_xyz=[1646, 500, 3091],
            natural_index=0,
        ),
        FairyData(
            name="Vase Room",
            map=Maps.AngryAztec,
            region=Regions.BetweenVinesByPortal,
            fence=Fence(127, 626, 463, 902),
            spawn_y=151,
            logic=lambda l: l.camera and ((l.pineapple and l.chunky) or l.phasewalk),
        ),
        FairyData(
            name="Oasis",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecOasis,
            fence=Fence(2206, 691, 2773, 1124),
            spawn_y=218,
        ),
        FairyData(
            name="Behind Tiny Temple",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecOasis,
            fence=Fence(3190, 424, 3503, 688),
            spawn_y=363,
        ),
        FairyData(
            name="Near Snake Road",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecConnectorTunnel,
            fence=Fence(3129, 1724, 3365, 1958),
            spawn_y=136,
        ),
        FairyData(
            name="Bonus Cage",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecConnectorTunnel,
            fence=Fence(4027, 2277, 4358, 2551),
            spawn_y=138,
        ),
        FairyData(
            name="Around Totem",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecMain,
            fence=Fence(2965, 3650, 3513, 4063),
            spawn_y=324,
        ),
        FairyData(
            name="Gong Tower",
            map=Maps.AngryAztec,
            region=Regions.AngryAztecMain,
            fence=Fence(4183, 3144, 4561, 3241),
            spawn_y=422,
        ),
        FairyData(
            name="Donkey 5DT",
            map=Maps.AztecDonkey5DTemple,
            region=Regions.DonkeyTemple,
            fence=Fence(699, 259, 755, 870),
            spawn_y=67,
            logic=lambda l: l.camera and ((l.coconut and l.isdonkey) or l.phasewalk),
        ),
        FairyData(
            name="Chunky 5DT",
            map=Maps.AztecChunky5DTemple,
            region=Regions.ChunkyTemple,
            fence=Fence(600, 601, 678, 1222),
            spawn_y=94,
            logic=lambda l: l.camera and ((l.pineapple and l.ischunky) or l.phasewalk),
        ),
        FairyData(
            name="Diddy 5DT",
            map=Maps.AztecDiddy5DTemple,
            region=Regions.DiddyTemple,
            fence=Fence(707, 236, 782, 363),
            spawn_y=47,
        ),
        FairyData(
            name="Lanky 5DT",
            map=Maps.AztecLanky5DTemple,
            region=Regions.LankyTemple,
            fence=Fence(426, 621, 496, 1209),
            spawn_y=94,
            logic=lambda l: l.camera and ((l.grape and l.islanky) or l.phasewalk),
        ),
        FairyData(
            name="Start of Llama Temple",
            map=Maps.AztecLlamaTemple,
            region=Regions.LlamaTemple,
            fence=Fence(2051, 2121, 2400, 2673),
            spawn_y=569,
        ),
        FairyData(
            name="Matching Room",
            map=Maps.AztecLlamaTemple,
            region=Regions.LlamaTemple,
            fence=Fence(952, 2101, 1153, 2667),
            spawn_y=769,
            logic=lambda l: l.camera and ((l.grape and l.islanky) or l.phasewalk or l.CanOStandTBSNoclip()),
        ),
        FairyData(
            name="Tiny Temple Start",
            map=Maps.AztecTinyTemple,
            region=Regions.TempleStart,
            fence=Fence(1195, 647, 1766, 1069),
            spawn_y=378,
        ),
        FairyData(
            name="Tiny Temple Kong Cage Room",
            map=Maps.AztecTinyTemple,
            region=Regions.TempleUnderwater,
            fence=Fence(280, 1288, 721, 1614),
            spawn_y=442,
        ),
    ],
    Levels.FranticFactory: [
        FairyData(
            name="Number Game",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            is_vanilla=True,
            spawn_xyz=[2967, 1094, 1646],
            natural_index=1,
        ),
        FairyData(
            name="Near Funky's",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            is_vanilla=True,
            spawn_xyz=[1535, 1231, 518],
            logic=lambda l: l.camera and Events.DartsPlayed in l.Events,
            natural_index=0,
        ),
        FairyData(
            name="Entrance",
            map=Maps.FranticFactory,
            region=Regions.FranticFactoryStart,
            fence=Fence(1055, 2387, 1477, 2664),
            spawn_y=864,
        ),
        FairyData(
            name="Pole",
            map=Maps.FranticFactory,
            region=Regions.BeyondHatch,
            fence=Fence(630, 1863, 680, 1920),
            spawn_y=519,
        ),
        FairyData(
            # Is technically in a different region, but can be accessed pretty easily from the lowest point of production
            name="Lower portion of Production Room",
            map=Maps.FranticFactory,
            region=Regions.LowerCore,
            fence=Fence(537, 1445, 734, 1679),
            spawn_y=282,
        ),
        FairyData(
            name="Mid-section of Production Room",
            map=Maps.FranticFactory,
            region=Regions.MiddleCore,
            fence=Fence(524, 986, 767, 1251),
            spawn_y=453,
        ),
        FairyData(
            name="Upper portion of Production Room",
            map=Maps.FranticFactory,
            region=Regions.UpperCore,
            fence=Fence(455, 1047, 756, 1652),
            spawn_y=726,
        ),
        FairyData(
            name="Storage Room",
            map=Maps.FranticFactory,
            region=Regions.BeyondHatch,
            fence=Fence(1004, 477, 1624, 919),
            spawn_y=189,
        ),
        FairyData(
            name="Near Cranky's",
            map=Maps.FranticFactory,
            region=Regions.BeyondHatch,
            fence=Fence(285, 534, 466, 909),
            spawn_y=249,
        ),
        FairyData(
            name="Arcade Tunnel",
            map=Maps.FranticFactory,
            region=Regions.BeyondHatch,
            fence=Fence(1232, 1019, 1312, 1719),
            spawn_y=1137,
        ),
        FairyData(
            name="Arcade Room",
            map=Maps.FranticFactory,
            region=Regions.BeyondHatch,
            fence=Fence(1798, 1511, 1898, 1528),
            spawn_y=1109,
        ),
        FairyData(
            name="Upper Block Tower",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            fence=Fence(2311, 1184, 2565, 1439),
            spawn_y=1439,
            logic=lambda l: l.camera and (l.spring and l.isdiddy),
        ),
        FairyData(
            name="Near Dartboard Boxes",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            fence=Fence(2445, 986, 2535, 1011),
            spawn_y=1050,
        ),
        FairyData(
            name="R&D Pole",
            map=Maps.FranticFactory,
            region=Regions.Testing,
            fence=Fence(3129, 1052, 3207, 1110),
            spawn_y=1189,
        ),
        FairyData(
            name="Car Race Entryway",
            map=Maps.FranticFactory,
            region=Regions.RandD,
            fence=Fence(3617, 1423, 3723, 1500),
            spawn_y=1301,
        ),
        FairyData(
            name="Toy Monster Room",
            map=Maps.FranticFactory,
            region=Regions.RandD,
            fence=Fence(4509, 1456, 5001, 1764),
            spawn_y=1483,
            logic=lambda l: l.camera and ((l.triangle and l.punch and l.ischunky) or l.CanAccessRNDRoom()),
        ),
        FairyData(
            name="Diddy R&D Room",
            map=Maps.FranticFactory,
            region=Regions.RandD,
            fence=Fence(4322, 387, 4672, 597),
            spawn_y=1455,
            logic=lambda l: l.camera and ((l.guitar and l.isdiddy) or l.CanAccessRNDRoom()),
        ),
        FairyData(
            name="Chute to Storage Room",
            map=Maps.FranticFactory,
            region=Regions.RandD,
            fence=Fence(4513, 843, 4666, 998),
            spawn_y=1373,
        ),
        FairyData(
            name="Dark Room",
            map=Maps.FranticFactory,
            region=Regions.BeyondHatch,
            fence=Fence(1820, 526, 2079, 874),
            spawn_y=60,
            logic=lambda l: l.camera and l.punch and l.chunky,
        ),
        FairyData(
            name="Crusher Room",
            map=Maps.FactoryCrusher,
            region=Regions.InsideCore,
            fence=Fence(70, 409, 412, 510),
            spawn_y=41,
        ),
    ],
    Levels.GloomyGalleon: [
        FairyData(
            name="In a chest",
            map=Maps.GloomyGalleon,
            region=Regions.GloomyGalleonStart,
            is_vanilla=True,
            spawn_xyz=[3547, 1795, 3703],
            logic=lambda l: l.camera and l.punch and l.chunky,
            natural_index=0,
        ),
        relocated_5ds_fairy,
        FairyData(
            name="Tiny Slam Button",
            map=Maps.GloomyGalleon,
            region=Regions.GloomyGalleonStart,
            fence=Fence(2222, 2659, 2299, 2731),
            spawn_y=1657,
        ),
        FairyData(
            name="Tunnel Intersection",
            map=Maps.GloomyGalleon,
            region=Regions.GloomyGalleonStart,
            fence=Fence(2470, 3175, 2601, 3297),
            spawn_y=1653,
        ),
        FairyData(
            name="Under Cranky Platform",
            map=Maps.GloomyGalleon,
            region=Regions.GloomyGalleonStart,
            fence=Fence(2903, 2917, 3146, 3149),
            spawn_y=1756,
        ),
        FairyData(
            name="Tunnel to Chest Area",
            map=Maps.GloomyGalleon,
            region=Regions.GloomyGalleonStart,
            fence=Fence(3014, 3311, 3152, 3776),
            spawn_y=1707,
        ),
        FairyData(
            name="Inbetween 5-Door Ship and 2-Door Ship",
            map=Maps.GloomyGalleon,
            region=Regions.ShipyardUnderwater,
            fence=Fence(1628, 1883, 1746, 2235),
            spawn_y=1220,
        ),
        FairyData(
            name="Inbetween 5-Door Ship and Seal Race",
            map=Maps.GloomyGalleon,
            region=Regions.ShipyardUnderwater,
            fence=Fence(2691, 441, 3345, 1305),
            spawn_y=1046,
        ),
        FairyData(
            name="Around Cactus",
            map=Maps.GloomyGalleon,
            region=Regions.Shipyard,
            fence=Fence(4085, 1040, 4575, 1063),
            spawn_y=1843,
        ),
        FairyData(
            name="Around Lighthouse",
            map=Maps.GloomyGalleon,
            region=Regions.LighthousePlatform,
            fence=Fence(1704, 4028, 1968, 4493),
            spawn_y=1877,
        ),
        FairyData(
            name="Seasick Ship",
            map=Maps.GalleonSickBay,
            region=Regions.SickBay,
            fence=Fence(517, 218, 751, 1024),
            spawn_y=57,
        ),
        FairyData(
            name="Top of Lighthouse",
            map=Maps.GalleonLighthouse,
            region=Regions.Lighthouse,
            fence=Fence(421, 386, 452, 594),
            spawn_y=779,
        ),
        FairyData(
            name="Mermaid Window",
            map=Maps.GalleonMermaidRoom,
            region=Regions.MermaidRoom,
            fence=Fence(146, 187, 164, 192),
            spawn_y=65,
        ),
        FairyData(
            name="Lanky's 5-Door Ship",
            map=Maps.Galleon5DShipDiddyLankyChunky,
            region=Regions.TromboneShip,
            fence=Fence(613, 634, 1084, 1549),
            spawn_y=90,
        ),
        FairyData(
            name="Tiny's 2-Door Ship",
            map=Maps.Galleon2DShip,
            region=Regions.TinyShip,
            fence=Fence(53, 77, 630, 222),
            spawn_y=80,
        ),
        FairyData(
            name="Submarine",
            map=Maps.GalleonSubmarine,
            region=Regions.Submarine,
            fence=Fence(765, 403, 1072, 502),
            spawn_y=155,
        ),
        FairyData(
            name="Inside the Treasure Chest",
            map=Maps.GalleonTreasureChest,
            region=Regions.TinyChest,
            fence=Fence(339, 853, 2191, 1648),
            spawn_y=1450,
        ),
    ],
    Levels.FungiForest: [
        FairyData(
            name="DK's Barn",
            map=Maps.ForestThornvineBarn,
            region=Regions.ThornvineBarn,
            is_vanilla=True,
            spawn_xyz=[497, 162, 502],
            logic=lambda l: l.Slam and l.camera,
            natural_index=1,
        ),
        FairyData(
            name="Dark Attic",
            map=Maps.ForestRafters,
            region=Regions.MillRafters,
            is_vanilla=True,
            spawn_xyz=[355, 50, 342],
            logic=lambda l: l.guitar and l.isdiddy and l.camera,
            natural_index=0,
        ),
        FairyData(
            name="Above Blue Tunnel",
            map=Maps.FungiForest,
            region=Regions.FungiForestStart,
            fence=Fence(2697, 1804, 3009, 2701),
            spawn_y=620,
        ),
        FairyData(
            name="Above the Clock",
            map=Maps.FungiForest,
            region=Regions.FungiForestStart,
            fence=Fence(2370, 2229, 2557, 2472),
            spawn_y=951,
        ),
        FairyData(
            name="Above the Well",
            map=Maps.FungiForest,
            region=Regions.FungiForestStart,
            fence=Fence(2067, 3098, 2335, 3237),
            spawn_y=540,
            logic=lambda l: l.camera and l.vines,
        ),
        FairyData(
            name="Above BBlast Entrance",
            map=Maps.FungiForest,
            region=Regions.MushroomLowerExterior,
            fence=Fence(126, 941, 545, 1020),
            spawn_y=764,
        ),
        FairyData(
            name="Near Crown",
            map=Maps.FungiForest,
            region=Regions.MushroomLowerExterior,
            fence=Fence(652, 1516, 1169, 1623),
            spawn_y=1010,
        ),
        FairyData(
            name="Top of Giant Mushroom",
            map=Maps.FungiForest,
            region=Regions.MushroomUpperExterior,
            fence=Fence(1356, 1442, 1675, 1596),
            spawn_y=1249,
        ),
        FairyData(
            name="Owl Tree Tunnel",
            map=Maps.FungiForest,
            region=Regions.HollowTreeArea,
            fence=Fence(1220, 2481, 1329, 2732),
            spawn_y=234,
        ),
        FairyData(
            name="Above Rabbit Race",
            map=Maps.FungiForest,
            region=Regions.HollowTreeArea,
            fence=Fence(2045, 3683, 2471, 4024),
            spawn_y=367,
        ),
        FairyData(
            name="Opposite Rabbit Race",
            map=Maps.FungiForest,
            region=Regions.HollowTreeArea,
            fence=Fence(367, 3608, 818, 4085),
            spawn_y=435,
        ),
        FairyData(
            name="Above Mill",
            map=Maps.FungiForest,
            region=Regions.MillArea,
            fence=Fence(4039, 3550, 4486, 3683),
            spawn_y=601,
        ),
        FairyData(
            name="Barn Alcove",
            map=Maps.FungiForest,
            region=Regions.MillArea,
            fence=Fence(3246, 4227, 3279, 4238),
            spawn_y=467,
        ),
        FairyData(
            name="Above path to Thornvine Barn",
            map=Maps.FungiForest,
            region=Regions.ThornvineArea,
            fence=Fence(4283, 1855, 4305, 2565),
            spawn_y=354,
        ),
        FairyData(
            name="Anthill",
            map=Maps.ForestAnthill,
            region=Regions.Anthill,
            fence=Fence(541, 307, 595, 881),
            spawn_y=328,
        ),
        FairyData(
            name="Winch Room",
            map=Maps.ForestWinchRoom,
            region=Regions.WinchRoom,
            fence=Fence(117, 179, 381, 388),
            spawn_y=67,
        ),
        FairyData(
            name="Front of Mill",
            map=Maps.ForestMillFront,
            region=Regions.GrinderRoom,
            fence=Fence(27, 313, 374, 476),
            spawn_y=131,
        ),
        FairyData(
            name="Lower Giant Mushroom Interior",
            map=Maps.ForestGiantMushroom,
            region=Regions.MushroomLower,
            fence=Fence(202, 338, 659, 650),
            spawn_y=357,
        ),
        FairyData(
            name="Upper Giant Mushroom Interior",
            map=Maps.ForestGiantMushroom,
            region=Regions.MushroomUpper,
            fence=Fence(417, 270, 602, 829),
            spawn_y=1596,
        ),
        FairyData(
            name="Lanky's Attic",
            map=Maps.ForestMillAttic,
            region=Regions.MillAttic,
            fence=Fence(180, 100, 391, 389),
            spawn_y=72,
        ),
        FairyData(
            name="Mill Interior (Rear)",
            map=Maps.ForestMillBack,
            region=Regions.MillChunkyTinyArea,
            fence=Fence(114, 533, 343, 652),
            spawn_y=173,
        ),
        FairyData(
            name="Spider Boss Room",
            map=Maps.ForestSpider,
            region=Regions.SpiderRoom,
            fence=Fence(74, 495, 1039, 787),
            spawn_y=378,
        ),
    ],
    Levels.CrystalCaves: [
        FairyData(
            name="Diddy Candles Cabin",
            map=Maps.CavesDiddyUpperCabin,
            region=Regions.DiddyUpperCabin,
            is_vanilla=True,
            spawn_xyz=[140, 100, 505],
            logic=lambda l: l.camera and (l.guitar or l.oranges) and l.spring and l.jetpack and l.isdiddy,
            natural_index=1,
        ),
        FairyData(
            name="Tiny Igloo",
            map=Maps.CavesTinyIgloo,
            region=Regions.TinyIgloo,
            is_vanilla=True,
            spawn_xyz=[309, 90, 438],
            logic=lambda l: l.Slam and (l.istiny or l.settings.free_trade_items) and l.camera,
            natural_index=0,
        ),
        FairyData(
            name="Level Start",
            map=Maps.CrystalCaves,
            region=Regions.CrystalCavesMain,
            fence=Fence(2089, 95, 2269, 330),
            spawn_y=95,
        ),
        FairyData(
            name="Gorilla Gone Room",
            map=Maps.CrystalCaves,
            region=Regions.CrystalCavesMain,
            fence=Fence(2461, 402, 2684, 542),
            spawn_y=76,
            logic=lambda l: l.camera and ((l.chunky and l.punch) or l.phasewalk or l.CanPhaseswim()),
        ),
        FairyData(
            name="Ice Castle Roof",
            map=Maps.CrystalCaves,
            region=Regions.CrystalCavesMain,
            fence=Fence(2204, 901, 2208, 1042),
            spawn_y=441,
        ),
        FairyData(
            name="Near Small Boulder",
            map=Maps.CrystalCaves,
            region=Regions.CrystalCavesMain,
            fence=Fence(1578, 942, 1736, 1072),
            spawn_y=343,
        ),
        FairyData(
            name="Bananaport Pillar",
            map=Maps.CrystalCaves,
            region=Regions.CrystalCavesMain,
            fence=Fence(1059, 1848, 1348, 1961),
            spawn_y=332,
        ),
        FairyData(
            name="Giant Boulder Room",
            map=Maps.CrystalCaves,
            region=Regions.BoulderCave,
            fence=Fence(1679, 2385, 2071, 2641),
            spawn_y=355,
        ),
        FairyData(
            name="Bonus Room",
            map=Maps.CrystalCaves,
            region=Regions.CavesBonusCave,
            fence=Fence(419, 2342, 532, 2609),
            spawn_y=239,
        ),
        FairyData(
            name="On 5-Door Igloo",
            map=Maps.CrystalCaves,
            region=Regions.IglooArea,
            fence=Fence(569, 1202, 576, 1363),
            spawn_y=177,
        ),
        FairyData(
            name="Near Bonus Waterfall",
            map=Maps.CrystalCaves,
            region=Regions.CrystalCavesMain,
            fence=Fence(2904, 721, 3094, 1103),
            spawn_y=322,
        ),
        FairyData(
            name="Blueprint Cave",
            map=Maps.CrystalCaves,
            region=Regions.CavesBlueprintCave,
            fence=Fence(3487, 553, 3548, 857),
            spawn_y=363,
        ),
        FairyData(
            name="5-Door Cabin Exterior",
            map=Maps.CrystalCaves,
            region=Regions.CabinArea,
            fence=Fence(3275, 1535, 3645, 1857),
            spawn_y=486,
        ),
        FairyData(
            name="Near 1-Door Cabin",
            map=Maps.CrystalCaves,
            region=Regions.CabinArea,
            fence=Fence(2583, 1716, 3058, 1840),
            spawn_y=302,
        ),
        FairyData(
            name="Under Waterfall Bridge",
            map=Maps.CrystalCaves,
            region=Regions.CabinArea,
            fence=Fence(2264, 1982, 2832, 2109),
            spawn_y=260,
        ),
        FairyData(
            name="Inside Tile Flip Room",
            map=Maps.CavesFrozenCastle,
            region=Regions.FrozenCastle,
            fence=Fence(106, 246, 420, 344),
            spawn_y=80,
        ),
        FairyData(
            name="Chunky 5-Door Igloo",
            map=Maps.CavesChunkyIgloo,
            region=Regions.ChunkyIgloo,
            fence=Fence(198, 257, 350, 300),
            spawn_y=75,
        ),
        FairyData(
            name="Diddy 5-Door Igloo",
            map=Maps.CavesDiddyIgloo,
            region=Regions.DiddyIgloo,
            fence=Fence(139, 261, 428, 307),
            spawn_y=104,
        ),
        FairyData(
            name="Donkey 5-Door Igloo",
            map=Maps.CavesDonkeyIgloo,
            region=Regions.DonkeyIgloo,
            fence=Fence(415, 495, 537, 532),
            spawn_y=74,
        ),
        FairyData(
            name="1-Door Cabin",
            map=Maps.CavesLankyCabin,
            region=Regions.LankyCabin,
            fence=Fence(363, 330, 539, 488),
            spawn_y=71,
        ),
        FairyData(
            name="Chunky 5-Door Cabin",
            map=Maps.CavesChunkyCabin,
            region=Regions.ChunkyCabin,
            fence=Fence(68, 109, 523, 562),
            spawn_y=74,
        ),
    ],
    Levels.CreepyCastle: [
        FairyData(
            name="Tree Sniper Room",
            map=Maps.CastleTree,
            region=Regions.CastleTree,
            is_vanilla=True,
            spawn_xyz=[1696, 400, 1054],
            logic=lambda l: l.camera and (((l.coconut or l.generalclips) and l.isdonkey) or l.phasewalk),
            natural_index=1,
        ),
        FairyData(
            name="Near Car Race",
            map=Maps.CastleMuseum,
            region=Regions.MuseumBehindGlass,
            is_vanilla=True,
            spawn_xyz=[277, 247, 1598],
            natural_index=0,
        ),
        FairyData(
            name="Start",
            map=Maps.CreepyCastle,
            region=Regions.CreepyCastleMain,
            fence=Fence(257, -41, 719, 143),
            spawn_y=497,
        ),
        FairyData(
            name="On Castle Tree",
            map=Maps.CreepyCastle,
            region=Regions.CreepyCastleMain,
            fence=Fence(1228, 211, 1287, 316),
            spawn_y=847,
        ),
        FairyData(
            name="Above Moat",
            map=Maps.CreepyCastle,
            region=Regions.CreepyCastleMain,
            fence=Fence(942, 769, 1371, 1050),
            spawn_y=806,
        ),
        FairyData(
            name="Opposite Library Entrance",
            map=Maps.CreepyCastle,
            region=Regions.CreepyCastleMain,
            fence=Fence(713, 690, 989, 914),
            spawn_y=1553,
        ),
        FairyData(
            name="Above Snide's",
            map=Maps.CreepyCastle,
            region=Regions.CreepyCastleMain,
            fence=Fence(650, 1207, 845, 1509),
            spawn_y=1997,
        ),
        FairyData(
            name="Near Wind Tower",
            map=Maps.CreepyCastle,
            region=Regions.CreepyCastleMain,
            fence=Fence(1207, 1224, 1433, 1586),
            spawn_y=1902,
        ),
        FairyData(
            name="Ballroom",
            map=Maps.CastleBallroom,
            region=Regions.Ballroom,
            fence=Fence(265, 251, 798, 924),
            spawn_y=480,
            logic=lambda l: l.camera and l.jetpack and l.isdiddy,
        ),
        FairyData(
            name="Lanky Dungeon",
            map=Maps.CastleDungeon,
            region=Regions.Dungeon,
            fence=Fence(424, 175, 664, 1123),
            spawn_y=230,
            logic=lambda l: l.camera and (l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.phasewalk) and l.trombone and l.balloon and l.islanky,
        ),
        FairyData(
            name="Donkey Dungeon",
            map=Maps.CastleDungeon,
            region=Regions.Dungeon,
            fence=Fence(1175, 1878, 1575, 2109),
            spawn_y=235,
            logic=lambda l: l.camera and ((l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.isdonkey) or l.phasewalk),
        ),
        FairyData(
            name="Above entrance to Mausoleum",
            map=Maps.CastleLowerCave,
            region=Regions.LowerCave,
            fence=Fence(1613, 1228, 1768, 1385),
            spawn_y=439,
        ),
        FairyData(
            name="Near Funky's",
            map=Maps.CastleLowerCave,
            region=Regions.LowerCave,
            fence=Fence(1362, 299, 1512, 551),
            spawn_y=300,
        ),
        FairyData(
            name="Above Donkey Diddy Chunky Crypt Entrance",
            map=Maps.CastleLowerCave,
            region=Regions.LowerCave,
            fence=Fence(134, 1173, 702, 1293),
            spawn_y=309,
        ),
        FairyData(
            name="Wind Tower",
            map=Maps.CastleTower,
            region=Regions.Tower,
            fence=Fence(378, 149, 392, 630),
            spawn_y=407,
        ),
        FairyData(
            name="Library",
            map=Maps.CastleLibrary,
            region=Regions.Library,
            fence=Fence(823, 649, 1820, 777),
            spawn_y=165,
        ),
    ],
    Levels.DKIsles: [
        FairyData(
            name="Small Island",
            map=Maps.Isles,
            region=Regions.IslesMain,
            is_vanilla=True,
            spawn_xyz=[1057, 634, 1456],
            natural_index=2,
        ),
        FairyData(
            name="Upper Krem Isles",
            map=Maps.Isles,
            region=Regions.KremIsleTopLevel,
            is_vanilla=True,
            spawn_xyz=[2358, 1798, 3884],
            natural_index=3,
        ),
        FairyData(
            name="Factory Lobby",
            map=Maps.FranticFactoryLobby,
            region=Regions.FranticFactoryLobby,
            is_vanilla=True,
            spawn_xyz=[245, 81, 150],
            logic=lambda l: l.camera and l.punch and l.chunky,
            natural_index=0,
        ),
        FairyData(
            name="Fungi Lobby",
            map=Maps.FungiForestLobby,
            region=Regions.FungiForestLobby,
            is_vanilla=True,
            spawn_xyz=[472, 163, 612],
            logic=lambda l: l.camera and l.feather and l.tiny,
            natural_index=1,
        ),
        FairyData(
            name="Aztec Roof",
            map=Maps.Isles,
            region=Regions.IslesMainUpper,
            fence=Fence(3396, 1667, 3603, 1815),
            spawn_y=1227,
        ),
        FairyData(
            name="Behind Fungi Building",
            map=Maps.Isles,
            region=Regions.CabinIsle,
            fence=Fence(2227, 564, 2506, 875),
            spawn_y=1637,
        ),
        FairyData(
            name="On Banana Fairy Island",
            map=Maps.Isles,
            region=Regions.CabinIsle,  # Technically it's on BFI area, but it requires rocketbarrel to access
            fence=Fence(860, 2358, 868, 2486),
            spawn_y=1031,
            logic=lambda l: l.camera and l.jetpack and l.isdiddy and Events.IslesDiddyBarrelSpawn in l.Events,
        ),
        FairyData(
            name="Lower Krem Isles",
            map=Maps.Isles,
            region=Regions.KremIsle,
            fence=Fence(1818, 3625, 1975, 4122),
            spawn_y=647,
        ),
        FairyData(
            name="On K. Lumsy",
            map=Maps.Isles,
            region=Regions.KremIsle,
            fence=Fence(3279, 3310, 3409, 3528),
            spawn_y=747,
        ),
        FairyData(
            name="In Front of Krem Isles",
            map=Maps.Isles,
            region=Regions.KremIsleBeyondLift,
            fence=Fence(2608, 3054, 2895, 3373),
            spawn_y=1309,
        ),
        FairyData(
            name="Inside Fairy Island",
            map=Maps.BananaFairyRoom,
            region=Regions.BananaFairyRoom,
            fence=Fence(506, 457, 722, 604),
            spawn_y=336,
        ),
        FairyData(
            name="Angry Aztec Lobby",
            map=Maps.AngryAztecLobby,
            region=Regions.AngryAztecLobby,
            fence=Fence(945, 487, 1090, 746),
            spawn_y=72,
            logic=lambda l: l.camera and ((l.feather and l.tiny) or l.phasewalk),
        ),
        FairyData(
            name="Creepy Castle Lobby",
            map=Maps.CreepyCastleLobby,
            region=Regions.CreepyCastleLobby,
            fence=Fence(567, 137, 575, 154),
            spawn_y=-15,
        ),
        FairyData(
            name="Crystal Caves Lobby",
            map=Maps.CrystalCavesLobby,
            region=Regions.CrystalCavesLobby,
            fence=Fence(160, 328, 342, 442),
            spawn_y=44,
            logic=lambda l: l.camera and ((l.punch and l.chunky) or l.phasewalk or l.ledgeclip),
        ),
        FairyData(
            name="Snide Room",
            map=Maps.IslesSnideRoom,
            region=Regions.IslesSnideRoom,
            fence=Fence(432, 157, 511, 198),
            spawn_y=136,
        ),
        FairyData(
            name="Training Grounds Entrance",
            map=Maps.TrainingGrounds,
            region=Regions.TrainingGrounds,
            fence=Fence(1538, 337, 1649, 376),
            spawn_y=91,
        ),
        FairyData(
            name="Training Grounds Hidden Mountain",
            map=Maps.TrainingGrounds,
            region=Regions.TrainingGrounds,
            fence=Fence(756, 1111, 857, 1339),
            spawn_y=453,
        ),
        FairyData(
            name="Treehouse Windows",
            map=Maps.Treehouse,
            region=Regions.Treehouse,
            fence=Fence(248, 252, 441, 351),
            spawn_y=118,
        ),
    ],
    Levels.HideoutHelm: [
        FairyData(
            name="Key 8 Room (1)",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,
            is_vanilla=True,
            spawn_xyz=[164, 118, 5213],
            logic=lambda l: l.camera and Events.HelmKeyAccess in l.Events,
            natural_index=0,
        ),
        FairyData(
            name="Key 8 Room (2)",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,
            is_vanilla=True,
            spawn_xyz=[135, 98, 5224],
            logic=lambda l: l.camera and Events.HelmKeyAccess in l.Events,
            natural_index=1,
        ),
        FairyData(
            name="Pineapple Switch Room",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,  # Not HideoutHelmStart because you could start in BoM room, requiring you to beat Helm in order to access this
            fence=Fence(1034, 1201, 1088, 1328),
            spawn_y=-150,
            logic=lambda l: l.camera and (l.handstand and l.lanky),
        ),
        FairyData(
            name="Under Grate",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,  # Not HideoutHelmStart because you could start in BoM room, requiring you to beat Helm in order to access this
            fence=Fence(1108, 2206, 1162, 2321),
            spawn_y=-164,
            logic=lambda l: l.camera and (l.handstand and l.lanky) and (l.chunky and l.pineapple and l.vines),
        ),
        FairyData(
            name="Under Chunky Room Stairs",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmMain,
            fence=Fence(1244, 3108, 1353, 3150),
            spawn_y=-132,
        ),
        FairyData(
            name="Above the Blast-o-Matic",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmMain,
            fence=Fence(804, 3194, 1355, 3648),
            spawn_y=540,
            logic=lambda l: l.camera and l.jetpack and l.isdiddy,
        ),
        FairyData(
            name="Navigation Room",
            map=Maps.HideoutHelm,
            region=Regions.HideoutHelmAfterBoM,
            fence=Fence(1555, 4683, 1555, 4704),
            spawn_y=0,
        ),
    ],
}
