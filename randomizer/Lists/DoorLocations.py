"""Stores the data for each potential TnS and Wrinkly door location."""

from randomizer.Enums.DoorType import DoorType
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Settings import (
    BananaportRando,
    DKPortalRando,
    RemovedBarriersSelected,
    ActivateAllBananaports,
    FungiTimeSetting,
    ShufflePortLocations,
    ShuffleLoadingZones,
)
from randomizer.Enums.Time import Time
from randomizer.Logic import RegionsOriginal as RegionList
from randomizer.LogicClasses import TransitionFront
from randomizer.Patching.Library.Generic import IsItemSelected
from randomizer.Lists.MapsAndExits import RegionMapList

LEVEL_MAIN_MAPS = (
    Maps.JungleJapes,
    Maps.AngryAztec,
    Maps.FranticFactory,
    Maps.GloomyGalleon,
    Maps.FungiForest,
    Maps.CrystalCaves,
    Maps.CreepyCastle,
)

LEVEL_ENTRY_HANDLER_REGIONS = (
    Regions.JungleJapesEntryHandler,
    Regions.AngryAztecEntryHandler,
    Regions.FranticFactoryEntryHandler,
    Regions.GloomyGalleonEntryHandler,
    Regions.FungiForestEntryHandler,
    Regions.CrystalCavesEntryHandler,
    Regions.CreepyCastleEntryHandler,
)

UNDERWATER_LOGIC_REGIONS = (
    Regions.TempleUnderwater,
    Regions.LighthouseUnderwater,
    Regions.LighthouseEnguardeDoor,
    Regions.ShipyardUnderwater,
    Regions.TreasureRoom,
    Regions.TinyChest,
    Regions.Submarine,
    Regions.LankyShip,
    Regions.TinyShip,
    Regions.BongosShip,
    Regions.GuitarShip,
    Regions.TromboneShip,
    Regions.SaxophoneShip,
    Regions.TriangleShip,
    Regions.Mechafish,
    Regions.MermaidRoom,
)


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
        scale=1,
        kong_lst=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        group=0,
        moveless=True,
        logic=None,
        placed: DoorType = DoorType.null,
        default_kong=None,
        door_type: list[DoorType] = [DoorType.boss, DoorType.dk_portal, DoorType.wrinkly],
        dk_portal_logic=None,
        dos_door=False,
        far_enough_from_wall=False,
    ):
        """Initialize with provided data."""
        self.name = name
        self.map = map
        self.logicregion = logicregion
        self.location = location
        self.rx = rx
        self.rz = rz
        self.scale = scale
        self.kongs = kong_lst
        self.group = group  # groups door locations to ensure troff n scoff portals don't generate right next to each other
        self.moveless = moveless  # moveless means that a door location can be accessed without any moves (except vines for in Aztec)
        if logic is None:
            self.logic = lambda l: True
        else:
            self.logic = logic
        self.placed = placed
        self.default_kong = default_kong
        self.default_placed = placed  # info about what door_type a door location is in vanilla
        self.dos_door = dos_door  # We need extra doors in Japes to make Dos' Doors work - this flag is for specifically that
        self.door_type = door_type.copy()  # denotes what types it can be
        # If we do not explicitly bar this door from being a DK portal, assume that it is allowed to be
        if dk_portal_logic is None:
            self.dk_portal_logic = lambda s: True
        else:
            self.dk_portal_logic = dk_portal_logic
        if True:  # Disable if we figure it's not necessary
            if DoorType.dk_portal in self.door_type and self.logicregion in UNDERWATER_LOGIC_REGIONS:
                # Disable portals in underwater regions
                self.door_type = [x for x in self.door_type if x != DoorType.dk_portal]
        # if self.default_placed == DoorType.dk_portal:
        #     # Disable TnS spawning here because of it being slightly bugged when exiting as DK/Chunky
        #     # Instantly re-activates the portal for some reason?
        #     # TODO: Figure out how to prevent this so we can remove this condition
        #     self.door_type = [x for x in self.door_type if x != DoorType.boss]
        self.default_door_list = self.door_type.copy()
        # if self.default_placed == DoorType.dk_portal:
        #     # Disable other doors being able to occupy the space of DK portals, for now
        #     self.door_type = [DoorType.dk_portal]
        self.assigned_kong = None
        self.far_enough_from_wall = far_enough_from_wall or placed != DoorType.null or rx != 0 or scale <= 0.8  # Keep track of which doors wouldn't benefit enough from a Z-buffering fix [NYI]

    def assignDoor(self, kong):
        """Assign door to kong."""
        self.placed = DoorType.wrinkly
        self.assigned_kong = kong

    def assignPortal(self, spoiler):
        """Assign TnS Portal to slot."""
        self.placed = DoorType.boss
        portal_region = spoiler.RegionList[self.logicregion]
        boss_region_id = GetBossLobbyRegionIdForRegion(self.logicregion, portal_region)
        portal_region.exits.append(TransitionFront(boss_region_id, self.logic))

    def updateDoorTypeLogic(self, spoiler):
        """Update door type list depending on enabled settings."""
        if self.dk_portal_logic(spoiler):
            if self.logicregion not in UNDERWATER_LOGIC_REGIONS and DoorType.dk_portal not in self.door_type:
                self.door_type.append(DoorType.dk_portal)
        else:
            if DoorType.dk_portal in self.door_type:
                self.door_type.remove(DoorType.dk_portal)
        if spoiler.settings.dk_portal_location_rando_v2 == DKPortalRando.main_only:
            if self.map not in LEVEL_MAIN_MAPS and DoorType.dk_portal in self.door_type:
                self.door_type = [x for x in self.door_type if x != DoorType.dk_portal]

    def assignDKPortal(self, spoiler, level):
        """Assign DK Portal to slot."""
        self.placed = DoorType.dk_portal
        placement_region = LEVEL_ENTRY_HANDLER_REGIONS[level]
        spoiler.RegionList[placement_region].exits[1] = TransitionFront(self.logicregion, lambda l: True)
        tied_map = RegionMapList[self.logicregion]
        if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all:
            spoiler.settings.level_portal_destinations[level] = {
                "map": tied_map,
                "exit": -1,
            }
        spoiler.settings.level_void_maps[level] = tied_map
        spoiler.settings.level_entrance_regions[level] = self.logicregion


def GetBossLobbyRegionIdForRegion(region_id, region):
    """Return the region id of the boss lobby the given region id and Region object should take you to."""
    if region_id == Regions.JungleJapesLobby or region.level == Levels.JungleJapes:
        return Regions.JapesBossLobby
    elif region_id == Regions.AngryAztecLobby or region.level == Levels.AngryAztec:
        return Regions.AztecBossLobby
    elif region_id == Regions.FranticFactoryLobby or region.level == Levels.FranticFactory:
        return Regions.FactoryBossLobby
    elif region_id == Regions.GloomyGalleonLobby or region.level == Levels.GloomyGalleon:
        return Regions.GalleonBossLobby
    elif region_id == Regions.FungiForestLobby or region.level == Levels.FungiForest:
        return Regions.ForestBossLobby
    elif region_id == Regions.CrystalCavesLobby or region.level == Levels.CrystalCaves:
        return Regions.CavesBossLobby
    elif region_id == Regions.CreepyCastleLobby or region.level == Levels.CreepyCastle:
        return Regions.CastleBossLobby
    else:
        return None


def isBarrierRemoved(spoiler, barrier_id: RemovedBarriersSelected):
    """Return whether the barrier has been removed."""
    return IsItemSelected(spoiler.settings.remove_barriers_enabled, spoiler.settings.remove_barriers_selected, barrier_id)


door_locations = {
    Levels.JungleJapes: [
        DoorData(
            name="Japes Lobby - Middle Right",
            map=Maps.JungleJapesLobby,
            logicregion=Regions.JungleJapesLobby,
            location=[169.075, 10.833, 594.613, 90.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
        ),  # DK Door
        DoorData(
            name="Japes Lobby - Far Left",
            map=Maps.JungleJapesLobby,
            logicregion=Regions.JungleJapesLobby,
            location=[647.565, 0.0, 791.912, 183.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Diddy Door
        DoorData(
            name="Japes Lobby - Close Right",
            map=Maps.JungleJapesLobby,
            logicregion=Regions.JungleJapesLobby,
            location=[156.565, 10.833, 494.73, 98.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
        ),  # Lanky Door
        DoorData(
            name="Japes Lobby - Far Right",
            map=Maps.JungleJapesLobby,
            logicregion=Regions.JungleJapesLobby,
            location=[252.558, 0.0, 760.733, 163.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
            dos_door=True,
        ),  # Tiny Door
        DoorData(
            name="Japes Lobby - Close Left",
            map=Maps.JungleJapesLobby,
            logicregion=Regions.JungleJapesLobby,
            location=[821.85, 0.0, 615.167, 264.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
        ),  # Chunky Door
        DoorData(
            name="Diddy Cave",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondPeanutGate,
            location=[2489.96, 280.0, 736.892, 179.0],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Door in Diddy Cave
        DoorData(
            name="Near Painting Room",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesTnSAlcove,
            location=[722.473, 538.0, 2386.608, 141.0],
            group=3,
            placed=DoorType.boss,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),  # TnS Door in Near Painting Room. Ironically cannot be a TnS because the indicator is weird
        DoorData(
            name="Fairy Cave",
            map=Maps.JungleJapes,
            logicregion=Regions.BeyondRambiGate,
            location=[901.203, 279.0, 3795.889, 202.0],
            group=4,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Door in Fairy Cave
        DoorData(
            name="Next to Diddy Cage - right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesHillTop,
            location=[896.0, 852.0, 2427.0, 90.75],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Alcove Above Diddy Tunnel - right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesTnSAlcove,
            location=[703.0, 538.0, 2293.0, 54.0],
            group=3,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Alcove Above Diddy Tunnel - left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesTnSAlcove,
            location=[817.0, 538.0, 2372.0, 232.0],
            group=3,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Next to Minecart Exit -right",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesMain,
            location=[1029.0, 287.0, 2032.0, 251.5],
            rx=-10,
            group=3,
        ),
        DoorData(
            name="Across From Minecart Exit",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesMain,
            location=[958.5, 288.0, 1616.0, 45.0],
            group=3,
        ),
        DoorData(
            name="Main Area - Next to Tunnel to Tiny Gate",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[2563.0, 286.0, 1567.0, 253.0],
            rx=-8,
            rz=9,
            group=5,
        ),
        DoorData(
            name="Beehive Area - Next to Beehive - far left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondFeatherGate,
            location=[1904.5, 539.0, 3369.0, 134.25],
            group=6,
            moveless=False,
        ),
        DoorData(
            name="Beehive Area - Next to Beehive - left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondFeatherGate,
            location=[1857.0, 539.0, 3196.0, 79.5],
            group=6,
            moveless=False,
            dos_door=True,
        ),
        DoorData(
            name="Behind Rambi Door - watery room - left",
            map=Maps.JungleJapes,
            logicregion=Regions.BeyondRambiGate,
            location=[611.0, 240.0, 3164.0, 201.75],
            group=4,
            moveless=False,
        ),
        DoorData(
            name="Behind Rambi Door - watery room - right",
            map=Maps.JungleJapes,
            logicregion=Regions.BeyondRambiGate,
            location=[803.0, 240.0, 2957.0, 280.0],
            group=4,
            moveless=False,
        ),
        DoorData(
            name="Top of Lanky's Useless Slope - left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesUselessSlope,
            location=[2299.0, 338.0, 3135.0, 296.0],
            kong_lst=[Kongs.lanky],
            group=7,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Top of Lanky's Useless Slope - right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesUselessSlope,
            location=[2095.5, 338.0, 3227.0, 118.7],
            kong_lst=[Kongs.lanky],
            group=7,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Underwater by Warp 2",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[1475.0, 160.0, 1605.0, 351.0],
            group=5,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            logic=lambda l: l.swim,
        ),
        DoorData(
            name="Underwater by Chunky's underground",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[2151.0, 160.0, 1587.0, 350.0],
            group=5,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            logic=lambda l: l.swim,
        ),
        DoorData(
            name="Next to Funky - right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesHill,
            location=[1928.0, 520.0, 2283.4, 140.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Next to Lanky's Painting Room - left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesPaintingRoomHill,
            location=[538.0, 370.0, 1991.0, 179.5],
            kong_lst=[Kongs.lanky],
            group=3,
            moveless=False,
        ),
        DoorData(
            name="Next to Lanky's Painting Room - right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesPaintingRoomHill,
            location=[551.0, 370.0, 1752.0, 6.5],
            kong_lst=[Kongs.lanky],
            group=3,
            moveless=False,
        ),
        DoorData(
            name="Outside Diddy Cave Switch - left",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[2133.0, 280.0, 421.0, 1.0],
            group=2,
        ),
        DoorData(
            name="Outside Diddy Cave Switch - right",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[2119.0, 280.0, 599.0, 180.0],
            group=2,
        ),
        DoorData(
            name="Entrance Tunnel - Near Diddy Cave - back left",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[1891.0, 280.0, 879.0, 180.0],
            group=2,
            door_type=[DoorType.wrinkly],  # Causes the Painting Room Gate's script to run incorrectly when Japes is first entered through this portal.
        ),
        DoorData(
            name="Entrance Tunnel - Near Diddy Cave - front left",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[2022.0, 280.0, 357.0, 295.6],
            group=2,
        ),
        DoorData(
            name="Entrance Tunnel - Near Warppad 1 and 2",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[1432.8, 280.0, 1056.0, 89.2],
            group=2,
        ),
        DoorData(
            name="Diddy Tunnel - next to hole - river side",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1329.0, 281.0, 2686.5, 183.5],
            group=2,
            moveless=False,
        ),
        DoorData(
            name="Diddy Tunnel - river side",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[683.5, 288.0, 2348.0, 61.0],
            rx=6,
            group=2,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Near Warp 4 and Tunnel Threeway crossing",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1570.0, 280.0, 2522.0, 242.0],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Tunnel - Crossroad",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1754.4, 210.0, 3102.0, 279.7],
            group=7,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Cranky Area - front-right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1414.0, 280.0, 3646.0, 55.0],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Area - front left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1955.5, 280.0, 3646.0, 314.5],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Area - center left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[2126.5, 280.0, 4082.0, 253.0],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Area - center right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1278.0, 280.0, 4114.0, 106.0],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Area - back left",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1930.0, 280.0, 4401.7, 147.8],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Area - back right",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBeyondCoconutGate2,
            location=[1405.0, 280.0, 4416.2, 175.5],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Beehive Room 2 - left",
            map=Maps.JapesTinyHive,
            logicregion=Regions.TinyHive,
            location=[1248.75, 186.0, 336.0, 34.5],
            rx=8,
            rz=-1.4,
            scale=2,
            kong_lst=[Kongs.tiny],
            group=8,
            moveless=False,
            logic=lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Beehive Room 2 - right",
            map=Maps.JapesTinyHive,
            logicregion=Regions.TinyHive,
            location=[1589.7, 195.5, 463.0, 289.7],
            rx=1,
            rz=7,
            scale=2,
            kong_lst=[Kongs.tiny],
            group=8,
            moveless=False,
            logic=lambda l: l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Painting Room - Next to the Entrance",
            map=Maps.JapesLankyCave,
            logicregion=Regions.JapesLankyCave,
            location=[305.0, 25.0, 63.0, 311.5],
            kong_lst=[Kongs.lanky],
            group=9,
            moveless=False,
        ),
        DoorData(
            name="Diddy Mountain - Next to Conveyor Controls",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[331.9, 100.0, 1451.0, 60.0],
            kong_lst=[Kongs.diddy],
            group=10,
            moveless=False,
            logic=lambda l: (l.charge and l.isdiddy) or l.CanPhase(),
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Diddy Mountain - between River and GB switch",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[643.0, 40.0, 148.0, 323.0],
            kong_lst=[Kongs.diddy],
            group=10,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Diddy Mountain - between River and Peanut Switch",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[801.0, 39.0, 268.0, 322.0],
            kong_lst=[Kongs.diddy],
            group=10,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Japes Vanilla Level Entry",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[903.167, 280, 1044.455, 180],
            group=11,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="Diddy Mountain - Next to the slam switch",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[480, 134, 66, 0],
            group=10,
            logic=lambda l: l.peanut and l.isdiddy,
            moveless=False,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Diddy Mountain - River grate 1",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[725, 30, 203.5, 322.5],
            group=10,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Diddy Mountain - River grate 2",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[927, 30, 783, 278.87],
            group=10,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Diddy Mountain - Minecart room",
            map=Maps.JapesMountain,
            logicregion=Regions.Mine,
            location=[606.7, 100, 965.7, 330],
            group=10,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Painting room - Left of painting",
            map=Maps.JapesLankyCave,
            logicregion=Regions.JapesLankyCave,
            location=[340, 80, 374, 222],
            group=9,
            kong_lst=[Kongs.lanky],
            far_enough_from_wall=True,
        ),
        DoorData(
            name="Painting room - Right of painting",
            map=Maps.JapesLankyCave,
            logicregion=Regions.JapesLankyCave,
            location=[82, 80, 374, 142.38],
            group=9,
            kong_lst=[Kongs.lanky],
            far_enough_from_wall=True,
        ),
        DoorData(
            name="Chunky underground - left wall",
            map=Maps.JapesUnderGround,
            logicregion=Regions.JapesCatacomb,
            location=[800, 20, 96, 315.6],
            group=12,
        ),
        DoorData(
            name="Chunky underground - right wall",
            map=Maps.JapesUnderGround,
            logicregion=Regions.JapesCatacomb,
            location=[726, 20, 325, 85],
            group=12,
        ),
        DoorData(
            name="Chunky underground - Kasplat platform",
            map=Maps.JapesUnderGround,
            logicregion=Regions.JapesCatacomb,
            location=[422, 20, 390.9, 3],
            group=12,
            door_type=[DoorType.boss, DoorType.wrinkly],
            logic=lambda l: l.can_use_vines and l.pineapple and l.ischunky,
            moveless=False,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Next to the baboon blast pad",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesBlastPadPlatform,
            location=[2433, 530, 1076.25, 333.5],
            group=11,
            moveless=False,
        ),
        DoorData(
            name="Entrance door switch",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[1498.8, 438.167, 299, 270],
            group=11,
            logic=lambda l: l.can_use_vines and l.climbing,
            moveless=False,
        ),
        DoorData(
            name="Next to level entrance",
            map=Maps.JungleJapes,
            logicregion=Regions.JungleJapesStart,
            location=[714, 288, 830, 90],
            group=11,
            dos_door=True,
        ),
        DoorData(
            name="Against the mountain",
            map=Maps.JungleJapes,
            logicregion=Regions.JapesHillTop,
            location=[1702, 789, 2354, 134.65],
            rx=-12,
            group=5,
        ),
    ],
    Levels.AngryAztec: [
        DoorData(
            name="Aztec Lobby - Pillar Wall",
            map=Maps.AngryAztecLobby,
            logicregion=Regions.AngryAztecLobby,
            location=[499.179, 0.0, 146.628, 0.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
        ),  # DK Door
        DoorData(
            name="Aztec Lobby - Lower Right",
            map=Maps.AngryAztecLobby,
            logicregion=Regions.AngryAztecLobby,
            location=[441.456, 0.0, 614.029, 180.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Diddy Door
        DoorData(
            name="Aztec Lobby - Left of Portal",
            map=Maps.AngryAztecLobby,
            logicregion=Regions.AngryAztecLobby,
            location=[628.762, 80.0, 713.93, 177.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
        ),  # Lanky Door
        DoorData(
            name="Aztec Lobby - Right of Portal",
            map=Maps.AngryAztecLobby,
            logicregion=Regions.AngryAztecLobby,
            location=[377.124, 80.0, 712.484, 179.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
            dos_door=True,
        ),  # Tiny Door
        DoorData(
            name="Aztec Lobby - Behind Feather Door",
            map=Maps.AngryAztecLobby,
            logicregion=Regions.AngryAztecLobby,
            location=[1070.018, 0.0, 738.609, 190.0],
            group=1,
            moveless=False,
            logic=lambda l: l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase(),
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
        ),  # Custom Chunky Door
        DoorData(
            name="Near Funky's",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2801.765, 121.333, 4439.293, 66.0],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal by Funky
        DoorData(
            name="Near Cranky's",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecConnectorTunnel,
            location=[2787.908, 120.0, 2674.299, 198.0],
            group=3,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal by Cranky
        DoorData(
            name="Near Candy's",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[2268.343, 120.0, 448.669, 59.0],
            group=4,
            placed=DoorType.boss,
        ),  # TnS Portal by Candy
        DoorData(
            name="Near Snide's",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[3573.712, 120.0, 4456.399, 285.0],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal by Snide
        DoorData(
            name="Behind 5DT",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[1968.329, 180.0, 3457.189, 244.0],
            group=5,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal behind 5DT
        DoorData(
            name="Next to Candy - right",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[2468.0, 120.0, 473.5, 298.75],
            group=4,
        ),
        DoorData(
            name="Under Diddy's Tiny Temple Switch",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[3053.0, 214.0, 605.5, 217.5],
            group=4,
            door_type=[DoorType.boss, DoorType.dk_portal],
        ),
        DoorData(
            name="Under Chunky's Tiny Temple Switch",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[3149.0, 212.0, 532.0, 217.5],
            group=4,
            door_type=[DoorType.boss, DoorType.dk_portal],
        ),
        DoorData(
            name="Under Tiny's Tiny Temple Switch",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[3183.0, 213.0, 773.0, 37.5],
            group=4,
            door_type=[DoorType.boss, DoorType.dk_portal],
        ),
        DoorData(
            name="Under Lanky's Tiny Temple Switch",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[3282.0, 213.0, 697.0, 37.5],
            group=4,
            door_type=[DoorType.boss, DoorType.dk_portal],
        ),
        DoorData(
            name="Diddy Tower Stairs - left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[4206.0, 80.0, 3367.0, 240.0],
            group=6,
            moveless=False,
        ),
        DoorData(
            name="Next to Tag Barrel near Snides",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[4067.0, 190.0, 4050.0, 263.0],
            group=2,
            moveless=False,
        ),
        DoorData(
            name="Under the Vulture Cage",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[4005.0, 120.0, 4598.0, 155.0],
            group=2,
            moveless=False,
        ),
        DoorData(
            name="5Door Temple's 6th Door",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2212.0, 180.0, 3687.3, 62.9],
            scale=1.47,
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Cranky Tunnel - Near Chunky Barrel - left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecConnectorTunnel,
            location=[3182.5, 120.0, 1440.0, 41.0],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Tunnel - Near Chunky Barrel - right",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecConnectorTunnel,
            location=[3358.0, 120.0, 1445.5, 318.5],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Tunnel - Near Road to Cranky - left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecConnectorTunnel,
            location=[3366.8, 120.0, 2032.0, 241.43],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="Cranky Tunnel - Near Road to Cranky - right",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecConnectorTunnel,
            location=[3166.25, 120.0, 2028.0, 118.5],
            group=7,
            moveless=False,
        ),
        DoorData(
            name="5Door Temple Staircase - front",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2031.0, 180.0, 3826.0, 63.5],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="5Door Temple Staircase - back",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[1921.0, 180.0, 3770.0, 244.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Entrance Tunnel - next to Coconut Switch",
            map=Maps.AngryAztec,
            logicregion=Regions.AztecTunnelBeforeOasis,
            location=[1514.0, 120.0, 1107.8, 4.8],
            group=8,
        ),
        DoorData(
            name="Entrance Tunnel - left (near the oasis end)",
            map=Maps.AngryAztec,
            logicregion=Regions.AztecTunnelBeforeOasis,
            location=[1820.0, 120.0, 816.5, 19.0],
            group=8,
        ),
        DoorData(
            name="In the sealed quicksand tunnel",
            map=Maps.AngryAztec,
            logicregion=Regions.AztecDonkeyQuicksandCave,
            location=[3208.25, 118.0, 4752.0, 225.0],
            kong_lst=[Kongs.donkey],
            group=2,
            moveless=False,
            logic=lambda l: l.isdonkey and l.strongKong,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Near Tag Barrel near Snides - strong kong",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[3940.0, 112.0, 4099.0, 323.5],
            kong_lst=[Kongs.donkey],
            group=2,
            moveless=False,
            logic=lambda l: l.isdonkey and l.strongKong,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="In Face Matching Game - right",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTempleMatching,
            location=[1074.0, 641.0, 2086.0, 0.26],
            kong_lst=[Kongs.lanky],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="In Face Matching Game - left",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTempleMatching,
            location=[1074.0, 641.0, 2683.7, 179.74],
            kong_lst=[Kongs.lanky],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Next to Tiny Temple - front left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[2893.0, 153.0, 478.0, 28.0],
            group=4,
        ),
        DoorData(
            name="Next to Tiny Temple - back left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[3209.2, 153.0, 312.2, 307.0],
            group=4,
        ),
        DoorData(
            name="Oasis - Next to Tunnel - far left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[2923.0, 120.0, 1205.0, 243.5],
            group=4,
        ),
        DoorData(
            name="Oasis - Next to Tunnel - left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[2836.0, 120.0, 1370.0, 237.5],
            group=4,
        ),
        DoorData(
            name="Between Snides and Diddy Gong Tower",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[4183.0, 120.0, 3830.0, 239.5],
            group=6,
            moveless=False,
        ),
        DoorData(
            name="Next to Llama Temple - left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2794.75, 120.0, 3566.0, 64.0],
            group=10,
            moveless=False,
        ),
        DoorData(
            name="Llama Temple's switchless side",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2997.6, 250.0, 2906.0, 105.0],
            group=10,
            moveless=False,
            door_type=[DoorType.boss, DoorType.dk_portal],
        ),
        DoorData(
            name="Tiny Temple - Main Room - left",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleStart,
            location=[1571.0, 289.0, 610.9, 0.0],
            group=11,
            moveless=False,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Main Room - back",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleStart,
            location=[1789.0, 287.0, 813.0, 270.0],
            group=11,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Across from Slope to Tiny Cage - left",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleUnderwater,
            location=[1672.5, 122.0, 1359.0, 270.0],
            group=11,
            moveless=False,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Across from Slope to Tiny Cage - right",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleUnderwater,
            location=[1672.5, 122.0, 1571.0, 270.0],
            group=11,
            moveless=False,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Next to Opening to Underwater Room",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleUnderwater,
            location=[1375.0, 145.0, 949.5, 180.0],
            group=11,
            moveless=False,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Across from Opening to Underwater Room",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleUnderwater,
            location=[1450.0, 145.0, 751.1, 0.0],
            group=11,
            moveless=False,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Llama Temple Stairs - left",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2902.0, 160.0, 3214.8, 285.1],
            scale=0.95,
            group=9,
            moveless=False,
        ),
        DoorData(
            name="Llama Temple Stairs - right",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[3020.0, 160.0, 3183.0, 105.1],
            scale=0.95,
            group=9,
            moveless=False,
        ),
        DoorData(
            name="Llama Temple - Entrance Staircase - left",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[2694.9, 371.0, 2310.0, 270.0],
            group=9,
            moveless=False,
        ),
        DoorData(
            name="Llama Temple - Entrance Staircase - right",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[2694.9, 371.0, 2546.0, 270.0],
            group=9,
            moveless=False,
        ),
        DoorData(
            name="Llama Temple - Across from the Spit Gate",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[2224.0, 203.0, 2704.0, 180.0],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly],
            logic=lambda l: Events.AztecLlamaSpit in l.Events and l.swim,
        ),
        DoorData(
            name="Aztec Vanilla Level Entry",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecStart,
            location=[781.846, 120, 150.3, 0],
            group=12,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="Donkey 5DT - First right branch",
            map=Maps.AztecDonkey5DTemple,
            logicregion=Regions.DonkeyTempleDeadEndRight,
            location=[180, 20, 376, 221],
            group=13,
            moveless=False,
            kong_lst=[Kongs.donkey],
        ),
        # DoorData(
        #     name="Donkey 5DT - Second left branch",
        #     map=Maps.AztecDonkey5DTemple,
        #     logicregion=Regions.DonkeyTemple,
        #     location=[970, 57, 894, 140],
        #     group=13,
        #     logic=lambda l: l.coconut and l.isdonkey,
        #     moveless=False,
        #     kong_lst=[Kongs.donkey],
        # ),  # Removed due to being too close to an enemy - will need to rework regions to uncomment this
        # DoorData(
        #     name="Diddy 5DT - First left branch",
        #     map=Maps.AztecDiddy5DTemple,
        #     logicregion=Regions.DiddyTemple,
        #     location=[982, 20, 378, 140],
        #     group=14,
        #     logic=lambda l: l.peanut and l.isdiddy,
        #     moveless=False,
        #     kong_lst=[Kongs.diddy],
        # ),  # Removed due to being too close to an enemy - will need to rework regions to uncomment this
        DoorData(
            name="Diddy 5DT - Second right branch",
            map=Maps.AztecDiddy5DTemple,
            logicregion=Regions.DiddyTempleDeadEndRight,
            location=[193, 57, 891, 221],
            group=14,
            moveless=False,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Lanky 5DT - Left side",
            map=Maps.AztecLanky5DTemple,
            logicregion=Regions.LankyTemple,
            location=[834, 47, 655, 270],
            group=15,
            moveless=False,
            kong_lst=[Kongs.lanky],
        ),
        DoorData(
            name="Lanky 5DT - Right side",
            map=Maps.AztecLanky5DTemple,
            logicregion=Regions.LankyTemple,
            location=[86, 47, 653, 90],
            group=15,
            moveless=False,
            kong_lst=[Kongs.lanky],
        ),
        DoorData(
            name="Tiny 5DT - Left side",
            map=Maps.AztecTiny5DTemple,
            logicregion=Regions.TinyTemple,
            location=[759, 47, 749, 180],
            group=16,
            moveless=False,
            kong_lst=[Kongs.tiny],
        ),
        DoorData(
            name="Tiny 5DT - Second center tunnel",
            map=Maps.AztecTiny5DTemple,
            logicregion=Regions.TinyTemple,
            location=[581, 85, 1009, 90],
            group=16,
            moveless=False,
            kong_lst=[Kongs.tiny],
        ),
        DoorData(
            name="Chunky 5DT - Intersection",
            map=Maps.AztecChunky5DTemple,
            logicregion=Regions.ChunkyTemple,
            location=[640, 85, 1264, 180],
            group=17,
            moveless=False,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Chunky 5DT - Left side",
            map=Maps.AztecChunky5DTemple,
            logicregion=Regions.ChunkyTemple,
            location=[1014, 20, 335, 270],
            group=17,
            moveless=False,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Llama Temple - Down the stairs - right",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[2564, 371, 1897, 0],
            group=9,
        ),
        DoorData(
            name="Llama Temple - Down the stairs - left",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[2566, 371, 2901, 185],
            group=9,
        ),
        DoorData(
            name="Llama Temple - Near top stairs - left",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[1613, 472, 2613, 138],  # Fun fact: This wall is slanted by ~5 degrees for whatever reason. The right side stairs, on the other hand...
            group=9,
            far_enough_from_wall=True,
        ),
        DoorData(
            name="Llama Temple - Near top stairs - right",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[1630.7, 472, 2186, 45],
            group=9,
        ),
        DoorData(
            name="Llama Temple - Center torch below entrance",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[2695, 469, 2393.6, 270],
            scale=0.8,
            group=9,
        ),
        DoorData(
            name="Llama Temple - Next to mini tunnel",
            map=Maps.AztecLlamaTemple,
            logicregion=Regions.LlamaTemple,
            location=[1725, 433, 3177, 217.5],
            group=9,
        ),
        DoorData(
            name="Tiny Temple - Behind the guitar pad",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleGuitarPad,
            location=[1370, 530, 531, 0],
            group=11,
            moveless=False,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Tiny Temple - Little alcove above mini barrel",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleStart,
            location=[1828.7, 389, 1126.7, 225],
            scale=0.8,
            group=11,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Next to triangle pad",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleStart,
            location=[1626, 215, 262.7, 15],
            group=11,
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        ),
        DoorData(
            name="Tiny Temple - Vulture room back wall",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleUnderwater,
            location=[1462, 305, 2429, 180],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.aztec_tiny_temple_ice),
        ),
        DoorData(
            name="Tiny Temple - Tiny room right wall",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleKONGRoom,
            location=[701, 344, 1147, 315],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            kong_lst=[Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.aztec_tiny_temple_ice),
        ),
        DoorData(
            name="Tiny Temple - Tiny room - on the K",
            map=Maps.AztecTinyTemple,
            logicregion=Regions.TempleKONGRoom,
            location=[87, 412.833, 1569.2, 86.04],  # Forwards is higher X (88.2), if I'd want to align it to the switch, instead of the wall
            scale=0.79,
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            kong_lst=[Kongs.diddy, Kongs.tiny],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.aztec_tiny_temple_ice),
        ),
        DoorData(
            name="Behind the llama cage",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecOasis,
            location=[2093, 216, 1597, 312.5],
            group=4,
        ),
        DoorData(
            name="In the quicksand near 5-door temple",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2273, 119, 3263, 346.5],
            group=2,
            door_type=[DoorType.wrinkly],
            logic=lambda l: l.strongKong and l.isdonkey,
            moveless=False,
            kong_lst=[Kongs.donkey],
        ),
        DoorData(
            name="On top of llama temple",
            map=Maps.AngryAztec,
            logicregion=Regions.AngryAztecMain,
            location=[2920, 380, 3047.2, 15],
            group=2,
            door_type=[DoorType.wrinkly],
            logic=lambda l: l.jetpack and l.diddy,
            moveless=False,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Behind the start of beetle race",
            map=Maps.AztecTinyRace,
            logicregion=Regions.AztecTinyRace,
            location=[1110, 5126, 3598, 90],
            group=18,
            door_type=[DoorType.wrinkly],
            kong_lst=[Kongs.tiny],
        ),
    ],
    Levels.FranticFactory: [
        DoorData(
            name="Factory Lobby - Low Left",
            map=Maps.FranticFactoryLobby,
            logicregion=Regions.FranticFactoryLobby,
            location=[544.362, 0.0, 660.802, 182.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
            dos_door=True,
        ),  # DK Door
        DoorData(
            name="Factory Lobby - Top Left",
            map=Maps.FranticFactoryLobby,
            logicregion=Regions.FranticFactoryLobby,
            location=[660.685, 133.5, 660.774, 182.0],
            group=1,
            moveless=False,
            logic=lambda l: (l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy)),
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Diddy Door
        DoorData(
            name="Factory Lobby - Top Center",
            map=Maps.FranticFactoryLobby,
            logicregion=Regions.FranticFactoryLobby,
            location=[468.047, 85.833, 662.907, 180.0],
            group=1,
            moveless=False,
            logic=lambda l: (l.grab and l.donkey) or l.CanMoonkick() or l.advanced_platforming,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
        ),  # Lanky Door
        DoorData(
            name="Factory Lobby - Top Right",
            map=Maps.FranticFactoryLobby,
            logicregion=Regions.FranticFactoryLobby,
            location=[275.533, 133.5, 661.908, 180.0],
            group=1,
            moveless=False,
            logic=lambda l: (l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy)),
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
        ),  # Tiny Door
        DoorData(
            name="Factory Lobby - Low Right",
            map=Maps.FranticFactoryLobby,
            logicregion=Regions.FranticFactoryLobby,
            location=[393.114, 0.0, 662.562, 182.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
        ),  # Chunky Door
        DoorData(
            name="Arcade Room",
            map=Maps.FranticFactory,
            logicregion=Regions.FactoryArcadeTunnel,
            location=[1778.702, 1106.667, 1220.515, 357.0],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal in Arcade Room
        DoorData(
            name="Production Room",
            map=Maps.FranticFactory,
            logicregion=Regions.UpperCore,
            location=[381.573, 605.0, 1032.929, 45.0],
            group=3,
            placed=DoorType.boss,
        ),  # TnS Portal in Production Room
        DoorData(
            name="R and D",
            map=Maps.FranticFactory,
            logicregion=Regions.RandD,
            location=[3827.127, 1264.0, 847.458, 222.0],
            group=4,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal in R and D
        DoorData(
            name="Block Tower",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2259.067, 1126.824, 1614.609, 182.0],
            group=5,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal in Block Tower Room
        DoorData(
            name="Storage Room",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[1176.912, 6.5, 472.114, 1.0],
            group=6,
            placed=DoorType.boss,
        ),  # TnS Portal in Storage Room
        DoorData(
            name="Behind Chunky's Toy Box - big",
            map=Maps.FranticFactory,
            logicregion=Regions.RandDUpper,
            location=[5016.0, 1336.0, 1780.0, 236.0],
            scale=2,
            kong_lst=[Kongs.chunky],
            group=4,
            moveless=False,
            logic=lambda l: (l.ischunky and l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom(),
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Next to Hatch with Tall Pole - left",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[489.5, 804.0, 1867.0, 49.0],
            group=7,
        ),
        DoorData(
            name="Next to Hatch with Tall Pole - right",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[800.0, 804.0, 1867.0, 310.0],
            group=7,
        ),
        DoorData(
            name="Bottom of the Tall Pole",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[528.0, 167.0, 1770.8, 35.0],
            group=7,
        ),
        DoorData(
            name="Production Room - Under Tiny Conveyors",
            map=Maps.FranticFactory,
            logicregion=Regions.UpperCore,
            location=[860.0, 605.0, 1011.0, 314.5],
            group=3,
        ),
        DoorData(
            name="Kong Cage Room - Behind Tag Barrel",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[1633.0, 6.0, 845.0, 270.0],
            group=6,
        ),
        DoorData(
            name="Under Cranky's Lab",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[267.7, 165.0, 805.0, 90.0],
            group=6,
        ),
        DoorData(
            name="Under Candy's Store",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[267.0, 165.0, 649.0, 90.0],
            group=6,
        ),
        DoorData(
            name="Next to DK's Count to 16 Puzzle",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2526.0, 1002.0, 1990.6, 180.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="R and D Room - Next to Tunnel to Car Race",
            map=Maps.FranticFactory,
            logicregion=Regions.RandD,
            location=[4006.7, 1264.0, 1454.0, 253.7],
            group=4,
            moveless=False,
        ),
        DoorData(
            name="Block Tower Room - Under Tunnel to Funky's",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2044.0, 1026.0, 978.0, 0.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="R and D Room - Dead End",
            map=Maps.FranticFactory,
            logicregion=Regions.RandD,
            location=[3824.0, 1264.0, 528.8, 340.5],
            group=4,
            moveless=False,
        ),
        DoorData(
            name="R and D Room - Blind Corner Next to Tunnel to Car Race",
            map=Maps.FranticFactory,
            logicregion=Regions.RandD,
            location=[3790.0, 1264.0, 1476.0, 52.5],
            group=4,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Funky's Room - Across from Melon Crate",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[1589.0, 1113.0, 816.2, 182.0],
            group=5,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Block Tower Room - Air Vent Under Arcade Window",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2002.5, 1027.0, 1180.5, 90.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Block Tower Room - Under Arcade Window - left",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[1957.1, 1026.0, 1448.0, 90.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Block Tower Room - Behind Tag Barrel",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2717.0, 1106.0, 838.0, 0.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="R and D Room - Next to Diddy's Pincode Room",
            map=Maps.FranticFactory,
            logicregion=Regions.RandDUpper,
            location=[4046.0, 1336.0, 608.0, 340.0],
            group=4,
            moveless=False,
        ),
        DoorData(
            name="Tiny's Race Entry Area",
            map=Maps.FranticFactory,
            logicregion=Regions.FactoryTinyRaceLobby,
            location=[3540.25, 1264.0, 1413.0, 141.0],
            kong_lst=[Kongs.tiny],
            group=4,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Kong Cage Room - Next to Tag Barrel",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[1421.0, 6.0, 927.3, 180.0],
            group=6,
        ),
        DoorData(
            name="Production Room - in Alcove Next to Tiny's Barrel",
            map=Maps.FranticFactory,
            logicregion=Regions.UpperCore,
            location=[215.0, 858.0, 1444.5, 90.0],
            scale=0.84,
            kong_lst=[Kongs.tiny],
            group=3,
            moveless=False,
            logic=lambda l: l.istiny and l.twirl,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Production Room - Next to Diddy's Switch",
            map=Maps.FranticFactory,
            logicregion=Regions.LowerCore,
            location=[430.6, 0.0, 980.6, 45.0],
            group=3,
        ),
        DoorData(
            name="Arcade Room - in a corner",
            map=Maps.FranticFactory,
            logicregion=Regions.FactoryArcadeTunnel,
            location=[1652.5, 1106.0, 1253.75, 43.0],
            scale=0.8669,
            group=2,
            moveless=False,
        ),
        DoorData(
            name="Block Tower Room - Next to Tiny Barrel",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2237.0, 1106.0, 943.0, 90.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Block Tower Room - at the Base of the Block Tower",
            map=Maps.FranticFactory,
            logicregion=Regions.Testing,
            location=[2517.0, 1026.0, 1315.0, 90.0],
            group=5,
            moveless=False,
        ),
        DoorData(
            name="Clock Room - Under Clock",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[1262.0, 867.0, 2025.0, 0.0],
            scale=0.48,
            group=7,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Clock Room - front left",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[1044.65, 842.0, 2223.0, 90.0],
            group=7,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Clock Room - back left",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[1044.65, 842.0, 2105.0, 90.0],
            group=7,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Clock Room - front right",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[1447.0, 842.0, 2283.5, 180.0],
            group=7,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Top of Pipe Near Kong-freeing Switch",
            map=Maps.FranticFactory,
            logicregion=Regions.FactoryStoragePipe,
            location=[1632.8, 197.0, 488.0, 270.0],
            scale=0.82,
            kong_lst=[Kongs.lanky],
            group=6,
            moveless=False,
            door_type=[DoorType.wrinkly, DoorType.dk_portal],
        ),
        DoorData(
            name="Pin Code Room - front-right",
            map=Maps.FranticFactory,
            logicregion=Regions.RandDUpper,
            location=[4386.2, 1336.0, 771.0, 124.0],
            kong_lst=[Kongs.diddy],
            group=4,
            moveless=False,
            logic=lambda l: (l.isdiddy and l.guitar) or l.CanAccessRNDRoom(),
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Lanky's Piano Room - right",
            map=Maps.FranticFactory,
            logicregion=Regions.RandD,
            location=[3610.0, 1264.0, 306.2, 325.0],
            kong_lst=[Kongs.lanky],
            group=4,
            moveless=False,
            logic=lambda l: (l.islanky and l.trombone) or l.CanAccessRNDRoom(),
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Lanky's Piano Room - left",
            map=Maps.FranticFactory,
            logicregion=Regions.RandD,
            location=[3320.0, 1264.0, 662.0, 145.25],
            kong_lst=[Kongs.lanky],
            group=4,
            moveless=False,
            logic=lambda l: (l.islanky and l.trombone) or l.CanAccessRNDRoom(),
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Chunky's Dark Room",
            map=Maps.FranticFactory,
            logicregion=Regions.BeyondHatch,
            location=[2149.6, 6.0, 598.0, 270.0],
            kong_lst=[Kongs.chunky],
            group=6,
            moveless=False,
            logic=lambda l: (l.chunky and l.punch) or l.CanPhase() or l.generalclips,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Crusher Room - start",
            map=Maps.FactoryCrusher,
            logicregion=Regions.InsideCore,
            location=[475.0, 0.0, 539.0, 180.0],
            group=3,
        ),
        DoorData(
            name="Factory Vanilla Level Entry",
            map=Maps.FranticFactory,
            logicregion=Regions.FranticFactoryStart,
            location=[1263.536, 827.31, 2787.292, 180],
            group=7,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="In the power hut",
            map=Maps.FactoryPowerHut,
            logicregion=Regions.PowerHut,
            location=[41, 0, 108, 90],
            group=8,
            kong_lst=[Kongs.donkey],
        ),
    ],
    Levels.GloomyGalleon: [
        DoorData(
            name="Galleon Lobby - Far Left",
            map=Maps.GloomyGalleonLobby,
            logicregion=Regions.GloomyGalleonLobby,
            location=[1022.133, 139.667, 846.41, 276.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
        ),  # DK Door
        DoorData(
            name="Galleon Lobby - Far Right",
            map=Maps.GloomyGalleonLobby,
            logicregion=Regions.GloomyGalleonLobby,
            location=[345.039, 139.667, 884.162, 92.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Diddy Door
        DoorData(
            name="Galleon Lobby - Close Right",
            map=Maps.GloomyGalleonLobby,
            logicregion=Regions.GloomyGalleonLobby,
            location=[464.68, 159.667, 1069.446, 161.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
        ),  # Lanky Door
        DoorData(
            name="Galleon Lobby - Near DK Portal",
            map=Maps.GloomyGalleonLobby,
            logicregion=Regions.GloomyGalleonLobby,
            location=[582.36, 159.667, 1088.258, 180.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
            dos_door=True,
        ),  # Tiny Door
        DoorData(
            name="Galleon Lobby - Close Left",
            map=Maps.GloomyGalleonLobby,
            logicregion=Regions.GloomyGalleonLobby,
            location=[876.388, 178.667, 1063.828, 192.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
        ),  # Chunky Door
        DoorData(
            name="Near Cranky's",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GalleonPastVines,
            location=[3423.707, 1890.471, 3098.15, 243.0],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Door Near Cranky's
        DoorData(
            name="Deep Hole",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthouseUnderwater,
            location=[1975.898, 100.0, 4498.375, 256.0],
            group=3,
            moveless=False,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),  # TnS Door in meme hole
        DoorData(
            name="Behind 2DS",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[803.636, 1053.997, 1955.268, 92.0],
            group=4,
            moveless=False,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),  # TnS Door behind 2DS
        DoorData(
            name="Behind Enguarde Door",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthouseEnguardeDoor,
            location=[645.832, 1460.0, 4960.476, 133.0],
            group=5,
            moveless=False,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),  # TnS Door behind Enguarde Door
        DoorData(
            name="Cactus",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[4517.923, 1290.0, 894.527, 308.0],
            group=6,
            moveless=False,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),  # TnS Door near Cactus
        DoorData(
            name="In hallway to Shipyard - Tiny switch",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2205.0, 1620.0, 2700.0, 90.0],
            group=2,
        ),
        DoorData(
            name="In hallway to Shipyard - Lanky switch",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2615.0, 1620.0, 2844.0, 302.0],
            group=2,
        ),
        DoorData(
            name="In hallway to Primate Punch Chests",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[3007.0, 1670.0, 3866.0, 135.42],
            group=2,
        ),
        DoorData(
            name="Under Baboon Blast pad",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthousePlatform,
            location=[1674.5, 1610.0, 4042.5, 261.15],
            group=7,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Under RocketBarrel barrel",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthousePlatform,
            location=[1360.0, 1609.0, 4048.0, 86.0],
            group=7,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Next to Cannonball game",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GalleonBeyondPineappleGate,
            location=[1334.0, 1610.0, 2523.0, 0.0],
            group=8,
            moveless=False,
            logic=lambda l: l.CanGetOnCannonGamePlatform(),
            door_type=[DoorType.boss, DoorType.wrinkly],
        ),
        DoorData(
            name="Next to Coconut switch",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2065.75, 1628.0, 3418.75, 28.0],
            group=2,
        ),
        DoorData(
            name="Entrance Tunnel - near entrance",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2112.0, 1628.0, 3223.0, 135.0],
            group=2,
        ),
        DoorData(
            name="Next to Peanut switch",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2462.0, 1619.0, 2688.0, 270.0],
            group=2,
        ),
        DoorData(
            name="Music Cactus - bottom back left",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[4444.0, 1290.0, 803.0, 307.7],
            group=6,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Music Cactus - bottom front left",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[4239.0, 1289.0, 880.0, 38.31],
            group=6,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Music Cactus - bottom back right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[4587.0, 1290.0, 972.0, 307.85],
            group=6,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Music Cactus - bottom front right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[4524.0, 1290.0, 1145.0, 218.31],
            group=6,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="On top of Seal cage",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthousePlatform,
            location=[2238.0, 1837.0, 4099.0, 251.7],
            kong_lst=[Kongs.diddy],
            group=7,
            moveless=False,
            logic=lambda l: l.isdiddy and l.jetpack,
            door_type=[DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Treasure Chest Exterior",
            map=Maps.GloomyGalleon,
            logicregion=Regions.TreasureRoom,
            location=[1938.0, 1440.0, 524.0, 330.0],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Next to Warp 3 in Cranky's Area",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GalleonPastVines,
            location=[3071.0, 1890.0, 2838.0, 0.0],
            group=2,
            moveless=False,
        ),
        DoorData(
            name="In Primate Punch Chest Room - right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[3460.0, 1670.0, 4001.0, 180.0],
            group=2,
        ),
        DoorData(
            name="Behind Chunky punch gate in Cranky Area",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[3275.0, 1670.0, 2353.65, 13.65],
            kong_lst=[Kongs.chunky],
            group=2,
            moveless=False,
            logic=lambda l: (l.ischunky and l.punch) or l.CanPhase(),
            door_type=[DoorType.boss, DoorType.wrinkly],
        ),
        DoorData(
            name="Low water alcove in lighthouse area",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthouseSurface,
            location=[540.3, 1564.0, 4094.0, 110.0],
            group=7,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Behind boxes in Cranky Area",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2891.5, 1688.0, 3493.0, 124.0],
            group=2,
        ),
        DoorData(
            name="Mech Fish Gate - far left",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[2651.0, 140.5, 503.0, 92.0],
            group=10,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Mech Fish Gate - left",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[2792.0, 175.0, 299.3, 15.9],
            rz=7.3,
            group=10,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Mech Fish Gate - middle",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[3225.0, 205.0, 303.0, 329.0],
            rz=-4.7,
            group=10,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Mech Fish Gate - right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[3406.0, 166.0, 531.0, 260.0],
            rx=290,
            rz=-290,
            group=10,
            moveless=False,
            door_type=[DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Mech Fish Gate - far right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[3310.0, 147.0, 828.0, 216.5],
            rx=16,
            rz=-16,
            group=10,
            moveless=False,
            door_type=[DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Cannonball Area Exit",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GalleonBeyondPineappleGate,
            location=[1524.1, 1461.0, 2898.0, 278.0],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.boss, DoorType.wrinkly],
        ),
        DoorData(
            name="2Dship's secret 3rd door",
            map=Maps.GloomyGalleon,
            logicregion=Regions.ShipyardUnderwater,
            location=[1109.0, 1189.9, 1978.0, 95.0],
            rz=-47,
            group=4,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Near Mermaid's Palace - right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthouseUnderwater,
            location=[1445.0, 141.0, 4859.0, 180.0],
            group=3,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Near Mermaid's Palace - left",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthouseUnderwater,
            location=[1400.0, 112.8, 4215.0, 346.5],
            rz=3,
            group=3,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Near Mermaid's Palace - Under Tag Barrel",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthouseUnderwater,
            location=[915.0, 164.0, 3967.0, 30.0],
            rx=7,
            rz=3,
            group=3,
            moveless=False,
            door_type=[DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Lighthouse - Up the ledge",
            map=Maps.GalleonLighthouse,
            logicregion=Regions.LighthouseAboveLadder,
            location=[508.0, 200.0, 409.0, 135.2],
            kong_lst=[Kongs.donkey],
            group=11,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Lighthouse - Left",
            map=Maps.GalleonLighthouse,
            logicregion=Regions.Lighthouse,
            location=[605.8, 0, 465, 90],
            kong_lst=[Kongs.donkey],
            group=11,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Lighthouse - Back",
            map=Maps.GalleonLighthouse,
            logicregion=Regions.Lighthouse,
            location=[323, 0, 586, 312],
            kong_lst=[Kongs.donkey],
            group=11,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="In Mermaid's Palace",
            map=Maps.GalleonMermaidRoom,
            logicregion=Regions.MermaidRoom,
            location=[274.0, 0.0, 481.0, 150.0],
            kong_lst=[Kongs.tiny],
            group=12,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Tiny's 5D ship",
            map=Maps.Galleon5DShipDKTiny,
            logicregion=Regions.SaxophoneShip,
            location=[735.0, 0.0, 1336.0, 270.0],
            kong_lst=[Kongs.tiny],
            group=13,
            moveless=False,
            door_type=[DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Lanky's 5D ship",
            map=Maps.Galleon5DShipDiddyLankyChunky,
            logicregion=Regions.TromboneShip,
            location=[1099.0, 0.0, 1051.0, 270.0],
            kong_lst=[Kongs.lanky],
            group=14,
            moveless=False,
            door_type=[DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Lanky's 2D ship",
            map=Maps.Galleon2DShip,
            logicregion=Regions.LankyShip,
            location=[1616.0, 0.0, 939.0, 179.5],
            kong_lst=[Kongs.lanky],
            group=15,
            moveless=False,
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Galleon Vanilla Level Entry",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[2111.065, 1620, 2678.088, 0],
            group=2,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="Pineapple gate tunnel - right",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[1994, 1609, 2924, 0],
            rz=11,
            group=2,
        ),
        DoorData(
            name="Pineapple gate tunnel - left",
            map=Maps.GloomyGalleon,
            logicregion=Regions.GloomyGalleonStart,
            location=[1992, 1609, 3041, 178],
            rz=11,
            group=2,
        ),
        DoorData(
            name="Seasick ship - start left",
            map=Maps.GalleonSickBay,
            logicregion=Regions.SickBay,
            location=[759, 20, 196, 270],
            group=20,
            kong_lst=[Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Seasick ship - start right",
            map=Maps.GalleonSickBay,
            logicregion=Regions.SickBay,
            location=[497, 20, 203, 90],
            group=20,
            kong_lst=[Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Seasick ship - after cannons front left",
            map=Maps.GalleonSickBay,
            logicregion=Regions.SickBay,
            location=[759, 20, 763, 270],
            group=20,
            kong_lst=[Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Seasick ship - after cannons front right",
            map=Maps.GalleonSickBay,
            logicregion=Regions.SickBay,
            location=[497, 20, 759, 90],
            group=20,
            kong_lst=[Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Seasick ship - after cannons center",
            map=Maps.GalleonSickBay,
            logicregion=Regions.SickBay,
            location=[622, 20, 1000, 196],
            group=20,
            kong_lst=[Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_lighthouse_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Left wall of Mech Fish",
            map=Maps.GalleonMechafish,
            logicregion=Regions.Mechafish,
            location=[554, 39, 614, 256],
            group=21,
            kong_lst=[Kongs.diddy],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Right wall of Mech Fish",
            map=Maps.GalleonMechafish,
            logicregion=Regions.Mechafish,
            location=[140, 39, 504, 105],
            group=21,
            kong_lst=[Kongs.diddy],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Chunky 5DS - Against a chest",
            map=Maps.Galleon5DShipDiddyLankyChunky,
            logicregion=Regions.TriangleShip,
            location=[1498.5, 0, 1561, 270],
            group=22,
            kong_lst=[Kongs.chunky],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Donkey 5DS - Next to the left cell bed",
            map=Maps.Galleon5DShipDKTiny,
            logicregion=Regions.BongosShip,
            location=[430, 0, 461, 0],
            group=23,
            kong_lst=[Kongs.donkey],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.galleon_shipyard_area_gate)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="On top of the lighthouse",
            map=Maps.GloomyGalleon,
            logicregion=Regions.LighthousePlatform,
            location=[1500, 2120, 4091, 329],
            scale=0.6,
            group=7,
            logic=lambda l: l.jetpack and l.isdiddy,
            moveless=False,
            door_type=[DoorType.wrinkly],
            kong_lst=[Kongs.diddy],
        ),
    ],
    Levels.FungiForest: [
        DoorData(
            name="Forest Lobby - On High Box",
            map=Maps.FungiForestLobby,
            logicregion=Regions.FungiForestLobby,
            location=[449.866, 45.922, 254.6, 270.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Forest Lobby - Near Gorilla Gone Door",
            map=Maps.FungiForestLobby,
            logicregion=Regions.FungiForestLobby,
            location=[136.842, 0.0, 669.81, 90.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Forest Lobby - Opposite Gorilla Gone Door",
            map=Maps.FungiForestLobby,
            logicregion=Regions.FungiForestLobby,
            location=[450.219, 0.0, 689.048, 270.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Forest Lobby - Near B. Locker",
            map=Maps.FungiForestLobby,
            logicregion=Regions.FungiForestLobby,
            location=[293.0, 0.0, 154.197, 0.0],
            scale=1.2,
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
            dos_door=True,
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Forest Lobby - Near Entrance",
            map=Maps.FungiForestLobby,
            logicregion=Regions.FungiForestLobby,
            location=[450.862, 0.0, 565.029, 270.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
        ),  # Custom Location (Removing Wheel)
        DoorData(
            name="Behind DK Barn",
            map=Maps.FungiForest,
            logicregion=Regions.ThornvineArea,
            location=[3515.885, 115.009, 1248.55, 31.0],
            group=2,
            moveless=False,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal in (FungiTimeSetting.dusk, FungiTimeSetting.progressive),
        ),  # TnS Portal behind DK Barn
        DoorData(
            name="Beanstalk Area",
            map=Maps.FungiForest,
            logicregion=Regions.WormArea,
            location=[3665.871, 186.833, 945.745, 252.0],
            group=3,
            moveless=False,
            logic=lambda l: Events.Night in l.Events,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal in (FungiTimeSetting.dusk, FungiTimeSetting.progressive)
            and (
                isBarrierRemoved(s, RemovedBarriersSelected.forest_green_tunnel)
                or (
                    s.settings.activate_all_bananaports == ActivateAllBananaports.all
                    and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                    and s.settings.bananaport_rando == BananaportRando.off
                )
            ),
        ),  # TnS Portal in Beanstalk Area
        DoorData(
            name="Near Snide's",
            map=Maps.FungiForest,
            logicregion=Regions.MillArea,
            location=[3240.033, 268.5, 3718.017, 178.0],
            group=4,
            moveless=False,
            logic=lambda l: Events.Day in l.Events,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal in (FungiTimeSetting.dusk, FungiTimeSetting.progressive),
        ),  # TnS Portal near Snide's
        DoorData(
            name="Top of Giant Mushroom",
            map=Maps.FungiForest,
            logicregion=Regions.MushroomUpperExterior,
            location=[1171.791, 1250.0, 1236.572, 52.0],
            group=5,
            placed=DoorType.boss,
        ),  # TnS Portal at Top of GMush
        DoorData(
            name="Owl Area",
            map=Maps.FungiForest,
            logicregion=Regions.HollowTreeArea,
            location=[203.663, 199.333, 3844.253, 92.0],
            group=6,
            moveless=False,
            placed=DoorType.boss,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.forest_yellow_tunnel)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),  # TnS Portal near Owl Race
        DoorData(
            name="On top of Cage outside Conveyor Belt",
            map=Maps.FungiForest,
            logicregion=Regions.ForestMillTopOfNightCage,
            location=[4312.0, 224.0, 3493.0, 134.82],
            group=4,
            moveless=False,
        ),
        DoorData(
            name="Watermill - front - right",
            map=Maps.FungiForest,
            logicregion=Regions.MillArea,
            location=[4261.0, 162.0, 3804.0, 314.12],
            group=4,
        ),
        DoorData(
            name="Watermill - right - left",
            map=Maps.FungiForest,
            logicregion=Regions.MillArea,
            location=[4367.0, 162.0, 3806.0, 44.0],
            group=4,
        ),
        DoorData(
            name="Watermill - right - right",
            map=Maps.FungiForest,
            logicregion=Regions.MillArea,
            location=[4450.0, 162.0, 3724.0, 44.5],
            group=4,
        ),
        DoorData(
            name="Watermill Roof - tower",
            map=Maps.FungiForest,
            logicregion=Regions.ForestTopOfMill,
            location=[4444.0, 321.0, 3628.0, 316.0],
            rx=-4,
            group=4,
        ),
        DoorData(
            name="Boxes outside of Diddy's Barn",
            map=Maps.FungiForest,
            logicregion=Regions.MillArea,
            location=[3469.0, 272.0, 4504.0, 122.5],
            group=4,
        ),
        DoorData(
            name="Outside Diddy's Barn",
            map=Maps.FungiForest,
            logicregion=Regions.MillArea,
            location=[3434.0, 271.0, 4316.0, 123.25],
            rx=-4,
            group=4,
        ),
        DoorData(
            name="Immediately Inside the Thornvine Area - right",
            map=Maps.FungiForest,
            logicregion=Regions.ThornvineArea,
            location=[4648.0, 205.0, 2836.0, 280.0],
            group=2,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal in (FungiTimeSetting.dusk, FungiTimeSetting.progressive),
        ),
        DoorData(
            name="Immediately Inside the Thornvine Area - left",
            map=Maps.FungiForest,
            logicregion=Regions.ThornvineArea,
            location=[4114.0, 202.0, 2654.5, 40.5],
            group=2,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal in (FungiTimeSetting.dusk, FungiTimeSetting.progressive),
        ),
        DoorData(
            name="Outside DK's Barn",
            map=Maps.FungiForest,
            logicregion=Regions.ThornvineArea,
            location=[4077.0, 115.0, 1954.0, 33.5],
            rx=-5,
            group=2,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal in (FungiTimeSetting.dusk, FungiTimeSetting.progressive),
        ),
        DoorData(
            name="Next to Rabbit's House",
            map=Maps.FungiForest,
            logicregion=Regions.HollowTreeArea,
            location=[2277.0, 167.3, 3500.6, 0.0],
            group=6,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.forest_yellow_tunnel)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Owl Area - Near Rocketbarrel Barrel - far left",
            map=Maps.FungiForest,
            logicregion=Regions.HollowTreeArea,
            location=[562.0, 199.0, 4147.25, 180.0],
            group=6,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.forest_yellow_tunnel)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Funky Area - Near Tiny Coins",
            map=Maps.FungiForest,
            logicregion=Regions.WormArea,
            location=[1939.0, 224.0, 261.0, 31.5],
            group=3,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.forest_green_tunnel)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Mushroom Area - Next to Tag Barrel near Cranky's",
            map=Maps.FungiForest,
            logicregion=Regions.GiantMushroomArea,
            location=[1754.2, 234.0, 972.0, 270.0],
            rx=-10,
            group=7,
        ),
        DoorData(
            name="Mushroom Area - Next to Rocketbarrel Barrel - left",
            map=Maps.FungiForest,
            logicregion=Regions.GiantMushroomArea,
            location=[67.0, 250.0, 719.0, 89.5],
            rx=-10,
            group=7,
        ),
        DoorData(
            name="Mushroom Area - Next to Rocketbarrel Barrel - right",
            map=Maps.FungiForest,
            logicregion=Regions.GiantMushroomArea,
            location=[254.0, 250.0, 386.0, 51.4],
            group=7,
        ),
        DoorData(
            name="Mushroom Area - Next to Cranky",
            map=Maps.FungiForest,
            logicregion=Regions.GiantMushroomArea,
            location=[1451.0, 179.0, 504.6, 321.5],
            group=7,
        ),
        DoorData(
            name="Clock Area - Next to Purple Tunnel - left",
            map=Maps.FungiForest,
            logicregion=Regions.FungiForestStart,
            location=[1795.7, 181.0, 2217.0, 117.6],
            group=8,
        ),
        DoorData(
            name="Clock Area - Next to Purple Tunnel - right",
            map=Maps.FungiForest,
            logicregion=Regions.FungiForestStart,
            location=[1876.0, 185.0, 1823.0, 39.5],
            group=8,
        ),
        DoorData(
            name="Clock Area - Next to Clock - left",
            map=Maps.FungiForest,
            logicregion=Regions.FungiForestStart,
            location=[2431.0, 603.0, 2410.0, 0.0],
            rx=10,
            group=8,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Clock Area - Next to Clock - right",
            map=Maps.FungiForest,
            logicregion=Regions.FungiForestStart,
            location=[2431.0, 603.0, 2238.0, 180.0],
            rx=10,
            group=8,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Funky Area - Near Beanstalk - left",
            map=Maps.FungiForest,
            logicregion=Regions.WormArea,
            location=[1830.0, 230.0, 822.0, 154.0],
            group=3,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.forest_green_tunnel)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Funky Area - Near Beanstalk - back",
            map=Maps.FungiForest,
            logicregion=Regions.WormArea,
            location=[1766.1, 228.0, 637.0, 90.5],
            group=3,
            moveless=False,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: isBarrierRemoved(s, RemovedBarriersSelected.forest_green_tunnel)
            or (
                s.settings.activate_all_bananaports == ActivateAllBananaports.all
                and s.settings.bananaport_placement_rando == ShufflePortLocations.off
                and s.settings.bananaport_rando == BananaportRando.off
            ),
        ),
        DoorData(
            name="Inside the Mushroom - All Kong Gun Switch - right",
            map=Maps.ForestGiantMushroom,
            logicregion=Regions.MushroomLower,
            location=[558.0, 74.0, 135.5, 353.0],
            rz=-5.5,
            group=5,
        ),
        DoorData(
            name="Inside the Mushroom - All Kong Gun Switch - left",
            map=Maps.ForestGiantMushroom,
            logicregion=Regions.MushroomLower,
            location=[340.0, 74.0, 135.5, 6.9],
            rz=5.5,
            group=5,
        ),
        DoorData(
            name="Inside the Mushroom - halfway along the Dead End",
            map=Maps.ForestGiantMushroom,
            logicregion=Regions.MushroomLowerBetweenLadders,
            location=[229.0, 217.0, 880.2, 147.5],
            rx=-3,
            rz=-3,
            group=5,
        ),
        # DoorData(
        #     name="Inside the Mushroom - Along the Wall near Diddy's Kasplat",
        #     map=Maps.ForestGiantMushroom,
        #     logicregion=Regions.MushroomMiddle,
        #     location=[396.0, 610.0, 929.0, 174.0],
        #     group=5,
        # ),
        DoorData(
            name="Inside the Mushroom - Along the Wall near Klump and Oranges",
            map=Maps.ForestGiantMushroom,
            logicregion=Regions.MushroomUpper,
            location=[847.25, 1169.0, 575.0, 264.0],
            group=5,
        ),
        DoorData(
            name="Chunky's Face Puzzle",
            map=Maps.ForestChunkyFaceRoom,
            logicregion=Regions.MushroomChunkyRoom,
            location=[427.4, 0.0, 182.0, 307.5],
            rx=5,
            kong_lst=[Kongs.chunky],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Lanky's 2-Mushroom Room",
            map=Maps.ForestLankyZingersRoom,
            logicregion=Regions.MushroomLankyZingersRoom,
            location=[196.0, 0.0, 484.45, 157.4],
            rx=5,
            kong_lst=[Kongs.lanky],
            group=10,
            moveless=False,
        ),
        DoorData(
            name="DK Lever puzzle Area",
            map=Maps.ForestMillFront,
            logicregion=Regions.GrinderRoom,
            location=[548.0, 45.0, 73.5, 0.0],
            scale=0.88,
            kong_lst=[Kongs.donkey],
            group=11,
            moveless=False,
            logic=lambda l: (l.isdonkey and l.CanSlamSwitch(Levels.FungiForest, 2)) or l.CanPhase() or l.generalclips,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Mill - back side - Near Chunky Coins",
            map=Maps.ForestMillBack,
            logicregion=Regions.MillChunkyTinyArea,
            location=[450.0, 0.0, 673.3, 180.0],
            kong_lst=[Kongs.tiny, Kongs.chunky],
            group=11,
            moveless=False,
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
        ),  # might be accessible by all kongs post-punch?
        DoorData(
            name="Winch Room - on the Winch",
            map=Maps.ForestWinchRoom,
            logicregion=Regions.WinchRoom,
            location=[238.0, 49.0, 124.0, 0.0],
            kong_lst=[Kongs.diddy],
            group=12,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Lanky's Attic",
            map=Maps.ForestMillAttic,
            logicregion=Regions.MillAttic,
            location=[125.0, 0.0, 453.3, 180.0],
            group=13,
        ),
        DoorData(
            name="DK's Barn - Between 2 Barrels near Switch",
            map=Maps.ForestThornvineBarn,
            logicregion=Regions.ThornvineBarn,
            location=[12.7, 4.0, 301.5, 90.0],
            kong_lst=[Kongs.donkey],
            group=14,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
            moveless=False,
        ),
        DoorData(
            name="Forest Vanilla Level Entry",
            map=Maps.FungiForest,
            logicregion=Regions.FungiForestStart,
            location=[2288.228, 181.333, 1569.101, 14],
            group=8,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="Mill - front side - Next to entrance",
            map=Maps.ForestMillFront,
            logicregion=Regions.GrinderRoom,
            location=[635.5, 0, 458, 270],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
        ),
        DoorData(
            name="Mill - front side - In the hay",
            map=Maps.ForestMillFront,
            logicregion=Regions.GrinderRoom,
            location=[22, 6, 290, 90],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
        ),
        DoorData(
            name="Mill - front side - Above the switch crate",
            map=Maps.ForestMillFront,
            logicregion=Regions.GrinderRoom,
            location=[21.3, 137, 152, 90],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
        ),
        DoorData(
            name="Mill - back side - In the hay",
            map=Maps.ForestMillBack,
            logicregion=Regions.MillChunkyTinyArea,
            location=[306, 22, 673, 180],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
        ),
        DoorData(
            name="Mill - back side - Crates near spider entrance",
            map=Maps.ForestMillBack,
            logicregion=Regions.MillChunkyTinyArea,
            location=[201, 51, 93.5, 0],
            group=11,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
        ),
        DoorData(
            name="Giant mushroom - Top towards tag barrel",
            map=Maps.ForestGiantMushroom,
            logicregion=Regions.MushroomUpper,
            location=[790, 1839, 764, 236.78],
            group=5,
        ),
        DoorData(
            name="Night door in the owl tree",
            map=Maps.FungiForest,
            logicregion=Regions.HollowTreeArea,
            location=[1275, 419, 3783, 181.5],
            group=6,
            door_type=[DoorType.boss, DoorType.wrinkly],
            logic=lambda l: l.TimeAccess(Regions.HollowTreeArea, Time.Night) and l.jetpack and l.isdiddy,
            moveless=False,
        ),
        DoorData(
            name="Lanky's colored mushrooms room",
            map=Maps.ForestLankyMushroomsRoom,
            logicregion=Regions.MushroomLankyMushroomsRoom,
            location=[450, 0, 371, 249],
            group=20,
            door_type=[DoorType.dk_portal, DoorType.wrinkly],
        ),
        DoorData(
            name="DK's Barn - Second floor",
            map=Maps.ForestThornvineBarn,
            logicregion=Regions.ThornvineBarnAboveLadder,
            location=[331, 140, 81, 0],
            group=14,
            door_type=[DoorType.boss, DoorType.wrinkly],
            dk_portal_logic=lambda s: s.settings.fungi_time_internal == FungiTimeSetting.dusk,
            moveless=False,
        ),
    ],
    Levels.CrystalCaves: [
        DoorData(
            name="Caves Lobby - Far Left",
            map=Maps.CrystalCavesLobby,
            logicregion=Regions.CrystalCavesLobby,
            location=[1103.665, 146.5, 823.872, 194.0],
            group=1,
            moveless=False,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
        ),  # DK Door
        DoorData(
            name="Caves Lobby - Top Ledge",
            map=Maps.CrystalCavesLobby,
            logicregion=Regions.CrystalCavesLobby,
            location=[731.84, 280.5, 704.935, 120.0],
            kong_lst=[Kongs.diddy],
            group=1,
            moveless=False,
            logic=lambda l: (l.isdiddy and l.jetpack) or l.CanMoonkick(),
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Diddy Door
        DoorData(
            name="Caves Lobby - Near Left",
            map=Maps.CrystalCavesLobby,
            logicregion=Regions.CrystalCavesLobby,
            location=[1046.523, 13.5, 476.611, 189.0],
            group=1,
            moveless=False,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
            dos_door=True,
        ),  # Lanky Door
        DoorData(
            name="Caves Lobby - Far Right",
            map=Maps.CrystalCavesLobby,
            logicregion=Regions.CrystalCavesLobby,
            location=[955.407, 146.664, 843.472, 187.0],
            group=1,
            moveless=False,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
        ),  # Tiny Door
        DoorData(
            name="Caves Lobby - Near Right",
            map=Maps.CrystalCavesLobby,
            logicregion=Regions.CrystalCavesLobby,
            location=[881.545, 13.466, 508.666, 193.0],
            group=1,
            moveless=False,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
        ),  # Chunky Door
        DoorData(
            name="On Rotating Room",
            map=Maps.CrystalCaves,
            logicregion=Regions.CavesRotatingCabinRoof,
            location=[2853.776, 436.949, 2541.475, 207.0],
            kong_lst=[Kongs.diddy],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal on Rotating Room
        DoorData(
            name="Near Snide's",
            map=Maps.CrystalCaves,
            logicregion=Regions.CavesSnideArea,
            location=[1101.019, 64.5, 467.76, 69.0],
            group=3,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal near Snide's
        DoorData(
            name="Giant Boulder Room",
            map=Maps.CrystalCaves,
            logicregion=Regions.BoulderCave,
            location=[1993.556, 277.108, 2795.365, 193.0],
            group=4,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal in Giant Boulder Room
        DoorData(
            name="On Sprint Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CavesSprintCabinRoof,
            location=[2196.449, 394.167, 1937.031, 93.0],
            kong_lst=[Kongs.diddy, Kongs.lanky],
            group=2,
            moveless=False,
            placed=DoorType.boss,
        ),  # TnS Portal on Sprint Cabin
        DoorData(
            name="Near 5DI",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[120.997, 50.167, 1182.974, 75.146],
            group=5,
            placed=DoorType.boss,
        ),  # TnS Portal near 5DI (Custom but treated as vanilla)
        DoorData(
            name="Outside Lanky's Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[2400.0, 276.0, 1892.5, 21.75],
            group=2,
        ),
        DoorData(
            name="Outside Chunky's Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[3515.65, 175.0, 1893.0, 273.7],
            group=2,
        ),
        DoorData(
            name="Outside Diddy's Lower Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[3697.5, 260.0, 1505.0, 291.0],
            group=2,
        ),
        DoorData(
            name="Outside Diddy's Upper Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[3666.7, 343.0, 1762.0, 273.8],
            group=2,
        ),
        DoorData(
            name="Under the Waterfall (Cabin Area)",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[2230.0, 0.0, 2178.0, 100.0],
            group=2,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Across from the 5Door Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[2970.0, 128.0, 1499.0, 68.5],
            rx=9,
            rz=11,
            group=2,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="5Door Igloo - DK's right",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[585.0, 48.0, 1396.0, 5.0],
            scale=0.95,
            group=5,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Diddy's right",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[684.9, 48.0, 1312.0, 75.0],
            scale=0.95,
            group=5,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Tiny's right",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[635.0, 48.0, 1190.0, 148.0],
            scale=0.95,
            group=5,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Chunky's right",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[504.5, 48.0, 1200.0, 220.3],
            scale=0.95,
            group=5,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Lanky's right",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[473.1, 48.0, 1327.0, 292.7],
            scale=0.95,
            group=5,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - DK's instrument pad",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[481.0, 0.0, 1444.0, 328.0],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Diddy's instrument pad",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[698.5, 0.0, 1424.5, 40.5],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Tiny's instrument pad",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[747.0, 0.0, 1212.5, 111.8],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Chunky's instrument pad",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[561.0, 0.0, 1101.0, 184.0],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="5Door Igloo - Lanky's instrument pad",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[396.0, 0.0, 1244.0, 256.0],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="Ice Castle Area - Near Rock Switch",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1349.6, 330.0, 1079.0, 86.7],
            rx=4,
            group=6,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Between Funky and Ice Castle - on land",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[2240.65, 65.8, 1185.0, 89.25],
            group=6,
        ),
        DoorData(
            name="Between Funky and Ice Castle - underwater",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[2370.0, 0.0, 1096.0, 196.0],
            group=6,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="In Water Near W4 Opposite Cranky - right",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1187.0, 0.0, 2410.0, 133.5],
            group=7,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="In Water Near W4 Opposite Cranky - left",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1441.0, 0.0, 2385.0, 208.0],
            group=7,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Under Bridge to Cranky",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1140.0, 0.0, 1704.0, 350.4],
            group=7,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Under Handstand Slope",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1263.3, 93.0, 1291.0, 73.5],
            group=8,
        ),
        DoorData(
            name="Mini Monkey Ledge",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[3112.3, 257.0, 1142.0, 262.0],
            rx=5,
            scale=0.4,
            group=6,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Across from Snide",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1818.5, 82.0, 1450.0, 218.5],
            rx=-14,
            rz=21,
            group=7,
        ),
        DoorData(
            name="Slope to Cranky with Mini Monkey Hole",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1047.0, 190.0, 2426.0, 175.0],
            rz=5.5,
            group=8,
        ),
        DoorData(
            name="Level Entrance - right",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1827.0, -29.0, 342.0, 225.0],
            group=8,
        ),
        DoorData(
            name="Level Entrance - left",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1828.0, -29.0, 91.0, 315.5],
            group=8,
        ),
        # DoorData(
        #     name="Ice Castle - left",
        #     map=Maps.CrystalCaves,
        #     logicregion=Regions.CrystalCavesMain,
        #     location=[2190.5, 343.0, 986.5, 314.2],
        #     scale=0.67,
        #     kong_lst=[Kongs.diddy, Kongs.lanky],
        #     group=6,
        #     moveless=False,
        #     logic=lambda l: l.isdiddy or (l.islanky and l.balloon) or l.advanced_platforming,
        #     door_type=[DoorType.boss],
        # ),
        # DoorData(
        #     name="Ice Castle - right",
        #     map=Maps.CrystalCaves,
        #     logicregion=Regions.CrystalCavesMain,
        #     location=[2221.0, 343.0, 957.0, 134.2],
        #     scale=0.67,
        #     kong_lst=[Kongs.diddy, Kongs.lanky],
        #     group=6,
        #     moveless=False,
        #     logic=lambda l: l.isdiddy or (l.islanky and l.balloon) or l.advanced_platforming,
        #     door_type=[DoorType.boss],
        # ),
        DoorData(
            name="Igloo Area - left of entrance",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[637.0, 0.0, 1605.0, 174.75],
            rx=-4,
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Igloo Area - Behind Tag Barrel Island",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[157.0, 0.0, 1575.0, 122.0],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Igloo Area - Behind Warp 1",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[282.5, 0.0, 892.0, 58.0],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Igloo Area - right of entrance",
            map=Maps.CrystalCaves,
            logicregion=Regions.IglooArea,
            location=[956.0, 0.0, 1222.0, 270.5],
            group=5,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Under Funky's Store",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[2868.0, 0.0, 1246.0, 113.0],
            group=6,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Next to Waterfall that's Next to Funky",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[3093.0, 0.0, 1262.0, 268.0],
            group=6,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="In Water Under Funky - left",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[3055.0, 0.0, 658.0, 1.28],
            group=6,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="In Water Under Funky - center",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[3221.0, 0.0, 820.0, 292.5],
            group=6,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="In Water Under Funky - right",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[3218.0, 0.0, 933.0, 256.3],
            group=6,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Ice Castle Interior - left",
            map=Maps.CavesFrozenCastle,
            logicregion=Regions.FrozenCastle,
            location=[340.0, 0.0, 146.0, 338.0],
            rx=6,
            kong_lst=[Kongs.lanky],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Ice Castle Interior - right",
            map=Maps.CavesFrozenCastle,
            logicregion=Regions.FrozenCastle,
            location=[202.0, 0.0, 456.5, 158.0],
            rx=6,
            kong_lst=[Kongs.lanky],
            group=9,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="In Chunky's 5Door Cabin on a Book Shelf",
            map=Maps.CavesChunkyCabin,
            logicregion=Regions.ChunkyCabin,
            location=[403.5, 44.0, 579.0, 180.0],
            kong_lst=[Kongs.chunky],
            group=10,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Cabin Area - Near Candy - right",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[2907.0, 156.0, 2279.0, 171.0],
            group=2,
        ),
        DoorData(
            name="Cabin Area - Near Candy - far right",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[2813.0, 158.0, 2291.0, 200.0],
            group=2,
        ),
        DoorData(
            name="Outside Tiny's Cabin",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[3553.0, 260.0, 1940.0, 188.0],
            group=2,
        ),
        DoorData(
            name="Cabin Area - Next to Tag Barrel on 2nd Floor",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[3603.0, 260.0, 1457.0, 345.0],
            group=2,
        ),
        DoorData(
            name="Under Cranky Slope - small",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1407.5, 95.0, 1519.0, 188.0],
            scale=0.43,
            group=8,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Caves Vanilla Level Entry",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1571.664, -29.167, 217.347, 90],
            group=8,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="Wall between Donkey cabin and waterfall",
            map=Maps.CrystalCaves,
            logicregion=Regions.CabinArea,
            location=[3177, 136, 1453, 346],
            rz=6,
            group=2,
        ),
        DoorData(
            name="Donkey 5door cabin - Right of entrance",
            map=Maps.CavesDonkeyCabin,
            logicregion=Regions.DonkeyCabin,
            location=[387, 0, 101, 0],
            group=20,
        ),
        DoorData(
            name="Donkey 5door cabin - Back wall",
            map=Maps.CavesDonkeyCabin,
            logicregion=Regions.DonkeyCabin,
            location=[101, 0, 310, 90],
            group=20,
        ),
        DoorData(
            name="Diddy upper cabin - Near right corner",
            map=Maps.CavesDiddyUpperCabin,
            logicregion=Regions.DiddyUpperCabin,
            location=[41, 0, 154, 90],
            group=21,
        ),
        DoorData(
            name="Diddy upper cabin - Far right corner",
            map=Maps.CavesDiddyUpperCabin,
            logicregion=Regions.DiddyUpperCabin,
            location=[41, 0, 553, 90],
            group=21,
        ),
        DoorData(
            name="Diddy upper cabin - Back bookshelf",
            map=Maps.CavesDiddyUpperCabin,
            logicregion=Regions.DiddyUpperCabin,
            location=[434, 42, 619, 180],
            scale=0.88,
            group=21,
        ),
        DoorData(
            name="Tiny cabin - Near corner",
            map=Maps.CavesTinyCabin,
            logicregion=Regions.TinyCabin,
            location=[101, 0, 129, 90],
            group=22,
        ),
        DoorData(
            name="Tiny cabin - Far corner",
            map=Maps.CavesTinyCabin,
            logicregion=Regions.TinyCabin,
            location=[460, 0, 499, 180],
            group=22,
        ),
        DoorData(
            name="Chunky cabin - Near corner",
            map=Maps.CavesChunkyCabin,
            logicregion=Regions.ChunkyCabin,
            location=[495, 0, 101, 0],
            group=23,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Chunky cabin - Back shelf",
            map=Maps.CavesChunkyCabin,
            logicregion=Regions.ChunkyCabin,
            location=[404, 45, 579, 180],
            group=23,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Donkey igloo - Under the swords",
            map=Maps.CavesDonkeyIgloo,
            logicregion=Regions.DonkeyIgloo,
            location=[228.5, 0, 791, 138.4],
            group=24,
        ),
        DoorData(
            name="Tiny igloo - Back wall",
            map=Maps.CavesTinyIgloo,
            logicregion=Regions.TinyIgloo,
            location=[117, 0, 416, 126.47],
            group=25,
        ),
        DoorData(
            name="Near ice castle tag barrel",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[2200, 280, 1347.65, 177],
            scale=0.868,
            group=8,
        ),
        # DoorData(
        #     name="Left small platform towards baboon blast",
        #     map=Maps.CrystalCaves,
        #     logicregion=Regions.CrystalCavesMain,
        #     location=[1562.4, 166, 1983, 284],  # It is not possible to properly rotate this door to match the slope, due to how DK64 works.
        #     group=8,
        # ),
        DoorData(
            name="Near Cranky",
            map=Maps.CrystalCaves,
            logicregion=Regions.CrystalCavesMain,
            location=[1027, 294, 1640, 58.25],
            rx=-11,
            rz=-12,
            group=8,
        ),
        DoorData(
            name="Behind giant boulder ice wall",
            map=Maps.CrystalCaves,
            logicregion=Regions.BoulderCave,
            location=[1523, 287, 2790, 193.5],
            group=4,
        ),
        DoorData(
            name="Behind gorilla gone ice wall",
            map=Maps.CrystalCaves,
            logicregion=Regions.CavesGGRoom,
            location=[2630.5, 13, 165, 274],
            group=8,
            moveless=False,
        ),
        DoorData(
            name="Starting room of beetle race",
            map=Maps.CavesLankyRace,
            logicregion=Regions.CavesLankyRace,
            location=[1118, 5110, 387.5, 63.5],
            group=26,
            door_type=[DoorType.wrinkly],
        ),
    ],
    Levels.CreepyCastle: [
        DoorData(
            name="Castle Lobby - Central Pillar (1)",
            map=Maps.CreepyCastleLobby,
            logicregion=Regions.CreepyCastleLobby,
            location=[499.978, 71.833, 634.25, 240.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.donkey,
        ),  # DK Door
        DoorData(
            name="Castle Lobby - Central Pillar (2)",
            map=Maps.CreepyCastleLobby,
            logicregion=Regions.CreepyCastleLobby,
            location=[499.545, 71.833, 725.653, 300.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.diddy,
        ),  # Diddy Door
        DoorData(
            name="Castle Lobby - Central Pillar (3)",
            map=Maps.CreepyCastleLobby,
            logicregion=Regions.CreepyCastleLobby,
            location=[661.738, 71.833, 726.433, 60.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.lanky,
        ),  # Lanky Door
        DoorData(
            name="Castle Lobby - Central Pillar (4)",
            map=Maps.CreepyCastleLobby,
            logicregion=Regions.CreepyCastleLobby,
            location=[660.732, 71.833, 635.288, 118.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.tiny,
        ),  # Tiny Door
        DoorData(
            name="Castle Lobby - Central Pillar (5)",
            map=Maps.CreepyCastleLobby,
            logicregion=Regions.CreepyCastleLobby,
            location=[581.215, 71.833, 588.444, 182.0],
            group=1,
            placed=DoorType.wrinkly,
            door_type=[DoorType.wrinkly],
            default_kong=Kongs.chunky,
            dos_door=True,
        ),  # Chunky Door
        DoorData(
            name="Near Greenhouse",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1543.986, 1381.167, 1629.089, 3.0],
            group=2,
            placed=DoorType.boss,
        ),  # TnS Portal by Greenhouse
        DoorData(
            name="Small Plateau",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1759.241, 903.75, 1060.8, 138.0],
            group=3,
            placed=DoorType.boss,
        ),  # TnS Portal by W2
        DoorData(
            name="Back of Castle",
            map=Maps.CreepyCastle,
            logicregion=Regions.CastleVeryBottom,
            location=[1704.55, 368.026, 1896.767, 4.0],
            group=4,
            placed=DoorType.boss,
        ),  # TnS Portal around back
        DoorData(
            name="Near Funky's",
            map=Maps.CastleLowerCave,
            logicregion=Regions.LowerCave,
            location=[1619.429, 200.0, 313.484, 299.0],
            group=5,
            placed=DoorType.boss,
        ),  # TnS Portal in Crypt Hub
        DoorData(
            name="Near Candy's",
            map=Maps.CastleUpperCave,
            logicregion=Regions.UpperCave,
            location=[1025.262, 300.0, 1960.308, 359.0],
            group=6,
            placed=DoorType.boss,
        ),  # TnS Portal in Dungeon Tunnel
        DoorData(
            name="Next to Small Pool outside of the Big Tree",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1020.0, 391.0, 181.0, 270.0],
            group=7,
            door_type=[DoorType.boss],
        ),
        DoorData(
            name="Against the Big Tree",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1200.0, 471.0, 254.0, 261.5],
            rx=-6,
            group=7,
        ),
        DoorData(
            name="Next to Tag Barrel at the Warp Pad Hub",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1545.0, 673.0, 944.0, 168.0],
            group=8,
        ),
        DoorData(
            name="Next to Cranky's",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[557.0, 1136.0, 1379.5, 273.0],
            group=9,
        ),
        DoorData(
            name="Outside Lanky's Greenhouse",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1606.0, 1391.0, 1906.0, 205.0],
            scale=0.95,
            group=2,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="On Stairs to Tag Barrel at the Warp Pad Hub",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1724.0, 728.0, 874.0, 203.46],
            scale=0.5,
            group=8,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Next to Castle Moat - Above Tiny's Kasplat",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[296.0, 548.0, 1014.5, 230.0],
            group=8,
        ),
        DoorData(
            name="Snide's Battlement - left",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[792.0, 1794.0, 1535.5, 224.7],
            scale=0.75,
            group=10,
        ),
        DoorData(
            name="Snide's Battlement - center",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[593.0, 1794.0, 1449.0, 118.0],
            scale=0.75,
            group=10,
        ),
        DoorData(
            name="Snide's Battlement - right",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[684.0, 1794.0, 1192.0, 28.5],
            scale=0.75,
            group=10,
        ),
        DoorData(
            name="Next to Stairs to Drawing Drawbridge",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[738.25, 548.0, 549.0, 239.5],
            group=8,
        ),
        DoorData(
            name="Battlement with Rocketbarrel Barrel - left",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[160.0, 548.0, 654.0, 325.0],
            group=8,
        ),
        DoorData(
            name="Battlement with Rocketbarrel Barrel - right",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[280.0, 548.0, 460.0, 145.0],
            group=8,
        ),
        DoorData(
            name="Moat - Underwater by Diddy Barrel",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[532.0, 424.0, 844.0, 210.0],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Moat - Under Drawing Drawbridge",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[766.0, 424.0, 663.0, 323.0],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Moat - Next to Tunnel Entrance - left",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1328.0, 424.0, 956.0, 188.5],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Moat - Next to Tunnel Entrance - right",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[969.0, 424.0, 1008.5, 188.5],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Moat - Next to Ladder - left",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1075.0, 424.0, 647.0, 3.5],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Moat - Next to Ladder - right",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1329.0, 424.0, 659.7, 337.2],
            group=8,
            moveless=False,
            logic=lambda l: l.swim,
            door_type=[DoorType.wrinkly, DoorType.boss],
        ),
        DoorData(
            name="Inside the Tree",
            map=Maps.CastleTree,
            logicregion=Regions.CastleTree,
            location=[1124.0, 400.0, 963.0, 247.3],
            rx=-3,
            group=11,
            moveless=False,
        ),
        DoorData(
            name="Library - Room with Big Books - left",
            map=Maps.CastleLibrary,
            logicregion=Regions.Library,
            location=[287.0, 190.0, 624.0, 180.0],
            kong_lst=[Kongs.donkey],
            group=12,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Library - Room with big Books - back",
            map=Maps.CastleLibrary,
            logicregion=Regions.Library,
            location=[103.4, 190.0, 209.0, 90.0],
            kong_lst=[Kongs.donkey],
            group=12,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Library - Next to Exit - left",
            map=Maps.CastleLibrary,
            logicregion=Regions.LibraryPastBooks,
            location=[2817.0, 180.0, 201.0, 0.0],
            kong_lst=[Kongs.donkey],
            group=12,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Library - Next to Exit - right",
            map=Maps.CastleLibrary,
            logicregion=Regions.LibraryPastBooks,
            location=[2826.0, 180.0, 549.0, 180.0],
            kong_lst=[Kongs.donkey],
            group=12,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Ballroom - Left Candle - left",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[113.7, 40.0, 692.0, 90.0],
            group=13,
            moveless=False,
        ),
        DoorData(
            name="Ballroom - Left Candle - right",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[113.7, 40.0, 497.0, 90.0],
            group=13,
            moveless=False,
        ),
        DoorData(
            name="Ballroom - Back Candle - left",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[455.0, 40.0, 107.4, 0.0],
            group=13,
            moveless=False,
        ),
        DoorData(
            name="Ballroom - Back Candle - right",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[652.0, 40.0, 107.4, 0.0],
            group=13,
            moveless=False,
        ),
        DoorData(
            name="Ballroom - Right Candle - left",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[987.0, 40.0, 501.0, 270.0],
            group=13,
            moveless=False,
        ),
        DoorData(
            name="Ballroom - Right Candle - right",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[987.0, 40.0, 705.0, 270.0],
            group=13,
            moveless=False,
        ),
        DoorData(
            name="Trash Can - Cheese",
            map=Maps.CastleTrashCan,
            logicregion=Regions.TrashCan,
            location=[592.0, 15.0, 576.6, 180.0],
            kong_lst=[Kongs.tiny],
            group=14,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Inside Chunky's Shed",
            map=Maps.CastleShed,
            logicregion=Regions.Shed,
            location=[397.0, 0.0, 160.0, 0.0],
            kong_lst=[Kongs.chunky],
            group=15,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Lower Tunnel - Under Peanut Switch",
            map=Maps.CastleLowerCave,
            logicregion=Regions.LowerCave,
            location=[120.0, 90.0, 1375.0, 88.75],
            group=16,
        ),
        DoorData(
            name="Lower Tunnel - Under Coconut and Pineapple Switches",
            map=Maps.CastleLowerCave,
            logicregion=Regions.LowerCave,
            location=[119.5, 90.0, 1149.0, 88.75],
            group=16,
        ),
        DoorData(
            name="Crypt - Under Lanky's Switch",
            map=Maps.CastleMausoleum,
            logicregion=Regions.Mausoleum,
            location=[803.6, 240.0, 1068.0, 270.0],
            scale=0.79,
            kong_lst=[Kongs.lanky, Kongs.tiny],
            group=17,
            moveless=False,
            door_type=[DoorType.wrinkly],
        ),
        # DoorData(
        #     name="Dungeon - Diddy's Chain Swinging Room - Behind Throne",
        #     map=Maps.CastleDungeon,
        #     logicregion=Regions.Dungeon,
        #     location=[535.0, 93.0, 3580.0, 180.0],
        #     scale=0.64,
        #     kong_lst=[Kongs.diddy],
        #     group=18,
        #     moveless=False,
        #     logic=lambda l: l.isdiddy and l.CanSlamSwitch(Levels.CreepyCastle, 3),
        #     door_type=[DoorType.wrinkly],
        # ),  # Disabled until we find a way to make it only activate when the throne is rotated away
        DoorData(
            name="Castle Vanilla Level Entry",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[314.006, 391.472, 414.279, 209],
            group=7,
            placed=DoorType.dk_portal,
        ),
        DoorData(
            name="Lanky wind tower - Right of Entrance",
            map=Maps.CastleTower,
            logicregion=Regions.Tower,
            location=[630, 225, 519.3, 240],
            group=20,
            kong_lst=[Kongs.lanky],
        ),
        DoorData(
            name="Lanky wind tower - Left of Entrance",
            map=Maps.CastleTower,
            logicregion=Regions.Tower,
            location=[170, 225, 519, 120],
            group=20,
            kong_lst=[Kongs.lanky],
        ),
        DoorData(
            name="Greenhouse - Dead end",
            map=Maps.CastleGreenhouse,
            logicregion=Regions.Greenhouse,
            location=[751, 0, 125.5, 90],
            group=21,
            door_type=[DoorType.wrinkly, DoorType.boss],
            kong_lst=[Kongs.lanky],
        ),
        DoorData(
            name="Greenhouse - Also dead end",
            map=Maps.CastleGreenhouse,
            logicregion=Regions.Greenhouse,
            location=[101, 0, 625, 90],
            group=21,
            door_type=[DoorType.wrinkly, DoorType.boss],
            kong_lst=[Kongs.lanky],
        ),
        DoorData(
            name="Ballroom - In Front of Monkeyport Pad",
            map=Maps.CastleBallroom,
            logicregion=Regions.Ballroom,
            location=[552, 40, 1093, 180],
            group=13,
            kong_lst=[Kongs.diddy, Kongs.tiny],
        ),
        # DoorData(
        #     name="Ballroom - Far Right Corner",
        #     map=Maps.CastleBallroom,
        #     logicregion=Regions.Ballroom,
        #     location=[915.7, 40, 200, 305],  # Invisible at these coordinates for some reason
        #     group=13,
        #     kong_lst=[Kongs.diddy, Kongs.tiny],
        # ),
        # DoorData(
        #     name="Ballroom - Far Left Corner",
        #     map=Maps.CastleBallroom,
        #     logicregion=Regions.Ballroom,
        #     location=[185.4, 40, 200, 54.5],  # Invisible at these coordiantes for some reason
        #     group=13,
        #     kong_lst=[Kongs.diddy, Kongs.tiny],
        # ),
        DoorData(
            name="Museum - Far Left Side",
            map=Maps.CastleMuseum,
            logicregion=Regions.Museum,
            location=[401, 100, 395, 90],
            group=22,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Museum - Far Right Side",
            map=Maps.CastleMuseum,
            logicregion=Regions.Museum,
            location=[1149, 100, 395, 270],
            group=22,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Museum - Tiny side - near the statue",
            map=Maps.CastleMuseum,
            logicregion=Regions.MuseumBehindGlass,
            location=[1137, 200, 1330, 0],
            group=23,
            door_type=[DoorType.boss, DoorType.wrinkly],
            logic=lambda l: l.monkeyport,
            moveless=False,
            kong_lst=[Kongs.tiny],
        ),
        DoorData(
            name="Museum - Tiny side - on the factory",
            map=Maps.CastleMuseum,
            logicregion=Regions.MuseumBehindGlass,
            location=[451.9, 200, 1512, 90],
            scale=0.87,
            group=23,
            door_type=[DoorType.boss, DoorType.wrinkly],
            kong_lst=[Kongs.tiny],
        ),
        DoorData(
            name="Tree - Near Coconut Gate",
            map=Maps.CastleTree,
            logicregion=Regions.CastleTree,
            location=[824, 400, 1032.8, 133],
            group=11,
            kong_lst=[Kongs.donkey, Kongs.chunky],
        ),
        DoorData(
            name="Tree - Past Punch Gate",
            map=Maps.CastleTree,
            logicregion=Regions.CastleTreePastPunch,
            location=[1033.8, 400, 582, 270],
            group=11,
            moveless=False,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Library - Strong Kong Alcove",
            map=Maps.CastleLibrary,
            logicregion=Regions.LibraryPastSlam,
            location=[2073, 180, 201, 0],
            group=12,
            kong_lst=[Kongs.donkey],
        ),
        DoorData(
            name="Library - Left wing",
            map=Maps.CastleLibrary,
            logicregion=Regions.Library,
            location=[1028, 100, 651, 0],
            group=12,
            kong_lst=[Kongs.donkey],
            door_type=[DoorType.wrinkly],  # Enemy spawn nearby. Can be a ground enemy in combination with Enemy Rando filtering
        ),
        DoorData(
            name="Chunky crypt - between right coffins",
            map=Maps.CastleCrypt,
            logicregion=Regions.CryptChunkyRoom,
            location=[752.8, 160, 2855, 90],
            group=24,
            moveless=False,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Chunky crypt - between left coffins",
            map=Maps.CastleCrypt,
            logicregion=Regions.CryptChunkyRoom,
            location=[1387, 160, 2851, 270],
            group=24,
            moveless=False,
            kong_lst=[Kongs.chunky],
        ),
        DoorData(
            name="Donkey crypt - behind the levers",
            map=Maps.CastleCrypt,
            logicregion=Regions.CryptDonkeyRoom,
            location=[1708.2, 80, 2340, 270],
            group=24,
            moveless=False,
            kong_lst=[Kongs.donkey],
        ),
        DoorData(
            name="Diddy crypt - right of the tomb",
            map=Maps.CastleCrypt,
            logicregion=Regions.CryptDiddyRoom,
            location=[2239.2, 0, 596, 270],
            group=24,
            moveless=False,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Diddy crypt - left of the tomb",
            map=Maps.CastleCrypt,
            logicregion=Regions.CryptDiddyRoom,
            location=[2239.2, 0, 194, 270],
            group=24,
            moveless=False,
            kong_lst=[Kongs.diddy],
        ),
        DoorData(
            name="Crypt - Second intersection",
            map=Maps.CastleCrypt,
            logicregion=Regions.Crypt,
            location=[1147.6, 160, 1285, 270],
            group=24,
            door_type=[DoorType.wrinkly],
            kong_lst=[Kongs.donkey, Kongs.diddy, Kongs.chunky],
        ),
        DoorData(
            name="Near the crypt staircase",
            map=Maps.CastleLowerCave,
            logicregion=Regions.LowerCave,
            location=[744, 90, 1263, 270],
            group=16,
        ),
        DoorData(
            name="Behind the mausoleum",
            map=Maps.CastleLowerCave,
            logicregion=Regions.LowerCave,
            location=[1768, 320, 1260.25, 90],
            scale=0.69,
            group=16,
            door_type=[DoorType.wrinkly],
        ),
        DoorData(
            name="Mausoleum - sprint corridor",
            map=Maps.CastleMausoleum,
            logicregion=Regions.Mausoleum,
            location=[1146, 160, 645, 188.5],
            group=17,
            kong_lst=[Kongs.lanky, Kongs.tiny],
        ),
        DoorData(
            name="Dungeon - Lanky side",
            map=Maps.CastleDungeon,
            logicregion=Regions.Dungeon,
            location=[694, 115, 1377.5, 315.5],
            group=18,
        ),
        DoorData(
            name="Dungeon - Diddy side",
            map=Maps.CastleDungeon,
            logicregion=Regions.Dungeon,
            location=[687, 115, 2625, 223.5],
            group=18,
        ),
        DoorData(
            name="Dungeon - DK side",
            map=Maps.CastleDungeon,
            logicregion=Regions.Dungeon,
            location=[899, 195, 2152.5, 225.5],
            group=18,
        ),
        DoorData(
            name="Candy intersection",
            map=Maps.CastleUpperCave,
            logicregion=Regions.UpperCave,
            location=[477, 218.5, 2143, 90],
            rx=-26,
            group=6,
            door_type=[DoorType.wrinkly],  # Too big of an X-rotation to guarantee an exit without re-entry. Feel free to test for 5.0
        ),
        DoorData(
            name="Next to dungeon door",
            map=Maps.CastleUpperCave,
            logicregion=Regions.UpperCave,
            location=[126.8, 198.5, 1509, 90],
            rx=-26,
            group=6,
            door_type=[DoorType.wrinkly],  # Enemy spawn nearby. Can be a ground enemy in combination with Enemy Rando filtering
        ),
        DoorData(
            name="Next to the chasm",
            map=Maps.CastleUpperCave,
            logicregion=Regions.UpperCave,
            location=[476.8, 198.5, 852, 90],
            rx=-26,
            group=6,
            door_type=[DoorType.wrinkly],  # Too big of an X-rotation to guarantee an exit without re-entry. Feel free to test for 5.0
        ),
        DoorData(
            name="Tombstone near lower door",
            map=Maps.CreepyCastle,
            logicregion=Regions.CastleVeryBottom,
            location=[811, 366, 2046.5, 19],
            rx=-3,
            group=4,
            door_type=[DoorType.boss, DoorType.wrinkly],
        ),
        DoorData(
            name="Behind the shed",
            map=Maps.CreepyCastle,
            logicregion=Regions.CreepyCastleMain,
            location=[1719, 1391, 1935, 27.5],
            group=7,
        ),
    ],
}
