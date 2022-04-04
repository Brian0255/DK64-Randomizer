"""Functions and data for setting and calculating prices."""

import random

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Items import Items
from randomizer.ItemPool import (
    ChunkyMoveLocations,
    DiddyMoveLocations,
    DonkeyMoveLocations,
    LankyMoveLocations,
    SharedMoveLocations,
    TinyMoveLocations,
)
from randomizer.Lists.Location import LocationList

VanillaPrices = {
    Items.BaboonBlast: 3,
    Items.StrongKong: 5,
    Items.GorillaGrab: 7,
    Items.ChimpyCharge: 3,
    Items.RocketbarrelBoost: 5,
    Items.SimianSpring: 7,
    Items.Orangstand: 3,
    Items.BaboonBalloon: 5,
    Items.OrangstandSprint: 7,
    Items.MiniMonkey: 3,
    Items.PonyTailTwirl: 5,
    Items.Monkeyport: 7,
    Items.HunkyChunky: 3,
    Items.PrimatePunch: 5,
    Items.GorillaGone: 7,
    Items.Coconut: 3,
    Items.Peanut: 3,
    Items.Grape: 3,
    Items.Feather: 3,
    Items.Pineapple: 3,
    Items.HomingAmmo: 5,
    Items.SniperSight: 7,
    Items.Bongos: 3,
    Items.Guitar: 3,
    Items.Trombone: 3,
    Items.Saxophone: 3,
    Items.Triangle: 3,
    Items.ProgressiveSlam: [5, 7],
    Items.ProgressiveAmmoBelt: [3, 5],
    Items.ProgressiveInstrumentUpgrade: [5, 7, 9],
}

ProgressiveMoves = {
    Items.ProgressiveSlam: 2,
    Items.ProgressiveAmmoBelt: 2,
    Items.ProgressiveInstrumentUpgrade: 3,
}


def RandomizePrices(weight):
    """Generate randomized prices based on given weight (low, medium, or high)."""
    prices = VanillaPrices.copy()
    # Each kong can buy up to 14 items
    # Vanilla: Can spend up to 74 coins, avg. price per item 5.2857
    # Low: Want average max to be around 40, avg. price per item 2.8571
    # Medium: Want average max to be around vanilla, use 5.3571 so it's midway between other 2
    # High: Want average max to be around 110, avg. price per item 7.8571
    avg = 5.3571
    stddev = avg * 0.25
    if weight == "high":
        avg = 7.8571
        stddev = avg * 0.2  # Lowered relative deviation for high so variance isn't so large
    elif weight == "low":
        avg = 2.8571
        stddev = avg * 0.25
    # Generate random prices using normal distribution with avg and std. deviation
    # Round each price to nearest int
    for item in prices.keys():
        # Special Case for progressive moves, supply an array of prices, one for each time it appears
        if item in ProgressiveMoves.keys():
            prices[item] = []
            for i in range(ProgressiveMoves[item]):
                prices[item].append(round(random.normalvariate(avg, stddev)))
        else:
            prices[item] = round(random.normalvariate(avg, stddev))
    return prices


def GetMaxForKong(settings, kong):
    """Get the maximum amount of coins the given kong can spend."""
    total = sum([value for key, value in settings.prices.items() if key in SharedMoveLocations])
    if kong == Kongs.donkey:
        total += sum([value for key, value in settings.prices.items() if key in DonkeyMoveLocations])
    elif kong == Kongs.diddy:
        total += sum([value for key, value in settings.prices.items() if key in DiddyMoveLocations])
    elif kong == Kongs.lanky:
        total += sum([value for key, value in settings.prices.items() if key in LankyMoveLocations])
    elif kong == Kongs.tiny:
        total += sum([value for key, value in settings.prices.items() if key in TinyMoveLocations])
    else:  # chunky
        total += sum([value for key, value in settings.prices.items() if key in ChunkyMoveLocations])
    return total


SlamProgressiveSequence = [Locations.SuperSimianSlam, Locations.SuperDuperSimianSlam]
FunkySequence = [
    [Locations.CoconutGun, Locations.PeanutGun, Locations.GrapeGun, Locations.FeatherGun, Locations.PineappleGun],
    Locations.AmmoBelt1,
    Locations.HomingAmmo,
    Locations.AmmoBelt2,
    Locations.SniperSight,
]
CandySequence = [
    [Locations.Bongos, Locations.Guitar, Locations.Trombone, Locations.Saxophone, Locations.Triangle],
    Locations.MusicUpgrade1,
    Locations.ThirdMelon,
    Locations.MusicUpgrade2,
]
DonkeySequence = [
    Locations.BaboonBlast,
    Locations.StrongKong,
    Locations.GorillaGrab,
]
DiddySequence = [
    Locations.ChimpyCharge,
    Locations.RocketbarrelBoost,
    Locations.SimianSpring,
]
LankySequence = [
    Locations.Orangstand,
    Locations.BaboonBalloon,
    Locations.OrangstandSprint,
]
TinySequence = [
    Locations.MiniMonkey,
    Locations.PonyTailTwirl,
    Locations.Monkeyport,
]
ChunkySequence = [
    Locations.HunkyChunky,
    Locations.PrimatePunch,
    Locations.GorillaGone,
]
Sequences = [
    SlamProgressiveSequence,
    FunkySequence,
    CandySequence,
    DonkeySequence,
    DiddySequence,
    LankySequence,
    TinySequence,
    ChunkySequence,
]

"""
So for coin logic, we want to make sure the player can't spend coins incorrectly and lock themselves out.
This means every buyable item has to account for, potentially, buying every other possible item first.
So each price will be inflated by a lot for logic purposes.
Total prices are as follows, in vanilla:
Cranky generic: 12
Cranky specific: 15
Candy generic: 21
Candy specific: 3
Funky generic: 20
Funky specific: 3
Total one kong can possibly spend: 74

The following only applies if move locations are not decoupled, meaning certain locations must be bought in sequence:
So basically, whatever "line" the kong is buying from, need to subtract prices
from future entries in that line from 74 (or whatever the max is if prices are random).
So since Cranky's upgrades cost 3, 5, and 7, the logical price of his
first upgrade will be 74 - 7 - 5 = 62.
Since prices can be randomized, we will dynamically subtract the prices of future purchases
in any given sequence.

If moves are decoupled so that they don't need be bought in sequence, then any location could be the final location,
meaning we just must consider the maximum price for every location.
"""


def GetPriceOfMoveItem(item, settings, slamLevel, ammoBelts, instUpgrades):
    """Get price of a move item. Needs to know current level of owned progressive moves to give correct price for progressive items."""
    if item == Items.ProgressiveSlam:
        if slamLevel in [1, 2]:
            return settings.prices[item][slamLevel - 1]
        else:
            # If already have max slam, there's move to buy
            return None
    elif item == Items.ProgressiveAmmoBelt:
        if ammoBelts in [0, 1]:
            return settings.prices[item][ammoBelts]
        else:
            # If already have max ammo belt, there's move to buy
            return None
    elif item == Items.ProgressiveInstrumentUpgrade:
        if instUpgrades in [0, 1, 2]:
            return settings.prices[item][instUpgrades]
        else:
            # If already have max instrument upgrade, there's move to buy
            return None
    else:
        return settings.prices[item]


def KongCanBuy(location, coins, settings, kong, slamLevel, ammoBelts, instUpgrades):
    """Check if given kong can logically purchase the specified location."""
    # If nothing is sold here, return true
    if LocationList[location].item is None or LocationList[location].item == Items.NoItem:
        return True
    price = GetPriceOfMoveItem(LocationList[location].item, settings, slamLevel, ammoBelts, instUpgrades)

    # Simple price check - combination of purchases will be considered outside this method
    if price is not None:
        # print("KongCanBuy checking item: " + str(LocationList[location].item))
        # print("for kong: " + kong.name + " with " + str(coins[kong]) + " coins")
        # print("has price: " + str(price))
        return coins[kong] >= price
    else:
        return False


def AnyKongCanBuy(location, coins, settings, slamLevel, ammoBelts, instUpgrades):
    """Check if any kong can logically purchase this location."""
    for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]:
        if KongCanBuy(location, coins, settings, kong, slamLevel, ammoBelts, instUpgrades):
            return True
    return False


def EveryKongCanBuy(location, coins, settings, slamLevel, ammoBelts, instUpgrades):
    """Check if any kong can logically purchase this location."""
    for kong in [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]:
        if not KongCanBuy(location, coins, settings, kong, slamLevel, ammoBelts, instUpgrades):
            return False
    return True


def CanBuy(location, coins, settings, slamLevel, ammoBelts, instUpgrades):
    """Check if an appropriate kong can logically purchase this location."""
    if location in DonkeyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.donkey, slamLevel, ammoBelts, instUpgrades)
    elif location in DiddyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.diddy, slamLevel, ammoBelts, instUpgrades)
    elif location in LankyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.lanky, slamLevel, ammoBelts, instUpgrades)
    elif location in TinyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.tiny, slamLevel, ammoBelts, instUpgrades)
    elif location in ChunkyMoveLocations:
        return KongCanBuy(location, coins, settings, Kongs.chunky, slamLevel, ammoBelts, instUpgrades)
    else:  # Shared locations
        return EveryKongCanBuy(location, coins, settings, slamLevel, ammoBelts, instUpgrades)