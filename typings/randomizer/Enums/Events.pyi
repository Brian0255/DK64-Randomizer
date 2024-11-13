from enum import IntEnum

class Events(IntEnum):
    IslesDiddyBarrelSpawn = 1
    IslesChunkyBarrelSpawn = 2
    KLumsyTalkedTo = 3
    JapesKeyTurnedIn = 4
    AztecKeyTurnedIn = 5
    FactoryKeyTurnedIn = 6
    GalleonKeyTurnedIn = 7
    ForestKeyTurnedIn = 8
    CavesKeyTurnedIn = 9
    CastleKeyTurnedIn = 10
    HelmKeyTurnedIn = 11
    TrainingBarrelsSpawned = 12
    Rambi = 13
    JapesFreeKongOpenGates = 14
    JapesDonkeySwitch = 15
    JapesDiddySwitch1 = 16
    JapesLankySwitch = 17
    JapesTinySwitch = 18
    JapesChunkySwitch = 19
    JapesDiddySwitch2 = 20
    FedTotem = 21
    LlamaFreed = 22
    AztecGuitarPad = 23
    AztecDonkeySwitch = 24
    AztecLlamaSpit = 25
    AztecIceMelted = 26
    HatchOpened = 27
    DartsPlayed = 28
    MainCoreActivated = 29
    ArcadeLeverSpawned = 30
    TestingGateOpened = 31
    DiddyCoreSwitch = 32
    LankyCoreSwitch = 33
    TinyCoreSwitch = 34
    ChunkyCoreSwitch = 35
    GalleonLankySwitch = 36
    GalleonTinySwitch = 37
    LighthouseGateOpened = 38
    ShipyardGateOpened = 39
    WaterRaised = 40
    WaterLowered = 41
    LighthouseEnguarde = 42
    SealReleased = 43
    MechafishSummoned = 44
    GalleonDonkeyPad = 45
    GalleonDiddyPad = 46
    GalleonLankyPad = 47
    GalleonTinyPad = 48
    GalleonChunkyPad = 49
    ActivatedLighthouse = 50
    ShipyardEnguarde = 51
    ShipyardTreasureRoomOpened = 52
    PearlsCollected = 53
    GalleonCannonRoomOpened = 54
    Day = 55
    Night = 56
    WormGatesOpened = 57
    HollowTreeGateOpened = 58
    MushroomCannonsSpawned = 59
    DonkeyMushroomSwitch = 60
    Bean = 61
    GrinderActivated = 62
    MillBoxBroken = 63
    ConveyorActivated = 64
    WinchRaised = 65
    CavesSmallBoulderButton = 66
    CavesLargeBoulderButton = 67
    GiantKoshaDefeated = 68
    CavesMonkeyportAccess = 69
    CastleTreeOpened = 70
    HelmDoorsOpened = 71
    HelmGatesPunched = 72
    HelmDonkeyDone = 73
    HelmChunkyDone = 74
    HelmTinyDone = 75
    HelmLankyDone = 76
    HelmDiddyDone = 77
    HelmFinished = 78
    KRoolDonkey = 79
    KRoolDiddy = 80
    KRoolLanky = 81
    KRoolTiny = 82
    KRoolChunky = 83
    KRoolDillo1 = 84
    KRoolDog1 = 85
    KRoolJack = 86
    KRoolPufftoss = 87
    KRoolDog2 = 88
    KRoolDillo2 = 89
    KRoolKKO = 90
    KRoolDefeated = 91
    DonkeyVerse = 92
    DiddyVerse = 93
    LankyVerse = 94
    TinyVerse = 95
    ChunkyVerse = 96
    FridgeVerse = 97
    JapesEntered = 98
    AztecEntered = 99
    FactoryEntered = 100
    GalleonEntered = 101
    ForestEntered = 102
    CavesEntered = 103
    CastleEntered = 104
    JapesW1aTagged = 105
    JapesW1bTagged = 106
    JapesW2aTagged = 107
    JapesW2bTagged = 108
    JapesW3aTagged = 109
    JapesW3bTagged = 110
    JapesW4aTagged = 111
    JapesW4bTagged = 112
    JapesW5aTagged = 113
    JapesW5bTagged = 114
    AztecW1aTagged = 115
    AztecW1bTagged = 116
    AztecW2aTagged = 117
    AztecW2bTagged = 118
    AztecW3aTagged = 119
    AztecW3bTagged = 120
    AztecW4aTagged = 121
    AztecW4bTagged = 122
    AztecW5aTagged = 123
    AztecW5bTagged = 124
    LlamaW1aTagged = 125
    LlamaW1bTagged = 126
    LlamaW2aTagged = 127
    LlamaW2bTagged = 128
    FactoryW1aTagged = 129
    FactoryW1bTagged = 130
    FactoryW2aTagged = 131
    FactoryW2bTagged = 132
    FactoryW3aTagged = 133
    FactoryW3bTagged = 134
    FactoryW4aTagged = 135
    FactoryW4bTagged = 136
    FactoryW5aTagged = 137
    FactoryW5bTagged = 138
    GalleonW1aTagged = 139
    GalleonW1bTagged = 140
    GalleonW2aTagged = 141
    GalleonW2bTagged = 142
    GalleonW3aTagged = 143
    GalleonW3bTagged = 144
    GalleonW4aTagged = 145
    GalleonW4bTagged = 146
    GalleonW5aTagged = 147
    GalleonW5bTagged = 148
    ForestW1aTagged = 149
    ForestW1bTagged = 150
    ForestW2aTagged = 151
    ForestW2bTagged = 152
    ForestW3aTagged = 153
    ForestW3bTagged = 154
    ForestW4aTagged = 155
    ForestW4bTagged = 156
    ForestW5aTagged = 157
    ForestW5bTagged = 158
    CavesW1aTagged = 159
    CavesW1bTagged = 160
    CavesW2aTagged = 161
    CavesW2bTagged = 162
    CavesW3aTagged = 163
    CavesW3bTagged = 164
    CavesW4aTagged = 165
    CavesW4bTagged = 166
    CavesW5aTagged = 167
    CavesW5bTagged = 168
    CastleW1aTagged = 169
    CastleW1bTagged = 170
    CastleW2aTagged = 171
    CastleW2bTagged = 172
    CastleW3aTagged = 173
    CastleW3bTagged = 174
    CastleW4aTagged = 175
    CastleW4bTagged = 176
    CastleW5aTagged = 177
    CastleW5bTagged = 178
    CryptW1aTagged = 179
    CryptW1bTagged = 180
    CryptW2aTagged = 181
    CryptW2bTagged = 182
    CryptW3aTagged = 183
    CryptW3bTagged = 184
    IslesW1aTagged = 185
    IslesW1bTagged = 186
    IslesW2aTagged = 187
    IslesW2bTagged = 188
    IslesW3aTagged = 189
    IslesW3bTagged = 190
    IslesW4aTagged = 191
    IslesW4bTagged = 192
    IslesW5aTagged = 193
    IslesW5bTagged = 194
    JapesLobbyAccessed = 195
    AztecLobbyAccessed = 196
    FactoryLobbyAccessed = 197
    GalleonLobbyAccessed = 198
    ForestLobbyAccessed = 199
    CavesLobbyAccessed = 200
    CastleLobbyAccessed = 201
    HelmLobbyAccessed = 202
    HelmLobbyTraversable = 203
