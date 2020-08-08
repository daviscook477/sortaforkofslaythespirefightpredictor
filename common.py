class InvalidRunError(Exception):
    """
    Something went wrong in processing the run file
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class ModdedDataError(Exception):
    """
    There was modded game data in the run file
    """

    def __init__(self, message):
        self.message = message
        supeR().__init__(self.message)

def upgrade_card(card_str):
    return card_str + '+1'

class StSGlobals:

    def make_character_specific_base_cards(deck, suffix):
        """
        Makes the starting deck have character specific suffixes
        :param deck: the starting deck
        :param suffix: the character-specific suffix
        """
        for index, card in enumerate(deck):
            if card == 'Strike' or card == 'Defend':
                deck[index] = card + suffix

    MIN_ASCENSION = 0

    ASCENDERS_BANE_ASCENSION = 10

    MAX_ASCENSION = 20

    ACT_ONE_BOSS_RELIC_FLOOR = 17

    ACT_TWO_BOSS_RELIC_FLOOR = 34

    ACT_THREE_BOSS_RELIC_FLOOR = 51

    ACT_FOUR_BOSS_RELIC_FLOOR = 56

    ACT_ONE_BOSSES = ['The Guardian', 'Hexaghost', 'Slime Boss']

    ACT_TWO_BOSSES = ['Automaton', 'Collector', 'Champ']

    ACT_THREE_BOSSES = ['Awakened One', 'Time Eater', 'Donu and Deca']

    BASE_GAME_STARTING_RELICS = {'Burning Blood', 'Cracked Core', 'PureWater', 'Ring of the Snake'}

    BASE_GAME_CHARACTERS = {'IRONCLAD', 'THE_SILENT', 'DEFECT', 'WATCHER'}

    BASE_GAME_STARTING_RELICS_BY_CHARACTER = {'IRONCLAD': ['Burning Blood'], 'THE_SILENT': ['Ring of the Snake'],
                                              'DEFECT': ['Cracked Core'], 'WATCHER': ['PureWater']}

    def get_starting_relics(run):
        """
        Gets the starting relic for a StS run
        :param run: the StS run
        :return: the starting relic
        """
        character = run.get('character_chosen')
        if not character in StSGlobals.BASE_GAME_CHARACTERS:
            raise ModdedDataError('%s is not a base game character' % character)
        return StSGlobals.BASE_GAME_STARTING_RELICS_BY_CHARACTER.get(character)[:]

    def get_starting_deck(run):
        """
        Gets the starting deck for a StS run
        :param run: the StS run
        :return: the starting deck
        """
        character = run.get('character_chosen')
        if not character in StSGlobals.BASE_GAME_CHARACTERS:
            raise ModdedDataError('%s is not a base game character' % character)
        ascension = run.get('ascension_level')
        if ascension and (ascension < StSGlobals.MIN_ASCENSION or ascension > StSGlobals.MAX_ASCENSION):
            raise InvalidRunError('Ascension level of %d was expected to be within [%d, %d] but it was not' % (ascension, StSGlobals.MIN_ASCENSION, StSGlobals.MAX_ASCENSION))
        basic_deck = ['Strike', 'Strike', 'Strike', 'Strike', 'Defend', 'Defend', 'Defend', 'Defend']
        if character == 'IRONCLAD':
            basic_deck.extend(['Strike', 'Bash'])
            StSGlobals.make_character_specific_base_cards(basic_deck, '_R')
        elif character == 'THE_SILENT':
            basic_deck.extend(['Strike', 'Defend', 'Survivor', 'Neutralize'])
            StSGlobals.make_character_specific_base_cards(basic_deck, '_G')
        elif character == 'DEFECT':
            basic_deck.extend(['Zap', 'Dualcast'])
            StSGlobals.make_character_specific_base_cards(basic_deck, '_B')
        elif character == 'WATCHER':
            basic_deck.extend(['Eruption', 'Vigilance'])
            StSGlobals.make_character_specific_base_cards(basic_deck, '_P')
        else:
            raise ModdedDataError('%s is not a base game character' % character)
        if ascension and ascension >= StSGlobals.ASCENDERS_BANE_ASCENSION:
            basic_deck.append('AscendersBane')
        return basic_deck

    BASE_GAME_RELICS = {'Burning Blood', 'Cracked Core', 'PureWater', 'Ring of the Snake', 'Akabeko', 'Anchor',
                        'Ancient Tea Set', 'Art of War', 'Bag of Marbles', 'Bag of Preparation', 'Blood Vial',
                        'TestModSTS:BottledPlaceholderRelic', 'Bronze Scales', 'Centennial Puzzle', 'CeramicFish',
                        'Damaru', 'DataDisk', 'Dream Catcher', 'Happy Flower', 'Juzu Bracelet', 'Lantern', 'MawBank',
                        'MealTicket', 'Nunchaku', 'Oddly Smooth Stone', 'Omamori', 'Orichalcum', 'Pen Nib',
                        'TestModSTS:PlaceholderRelic2', 'Potion Belt', 'PreservedInsect', 'Red Skull', 'Regal Pillow',
                        'TestModSTS:DefaultClickableRelic', 'Smiling Mask', 'Snake Skull', 'Strawberry', 'Boot',
                        'Tiny Chest', 'Toy Ornithopter', 'Vajra', 'War Paint', 'Whetstone', 'Blue Candle',
                        'Bottled Flame', 'Bottled Lightning', 'Bottled Tornado', 'Darkstone Periapt', 'Yang',
                        'Eternal Feather', 'Frozen Egg 2', 'Cables', 'Gremlin Horn', 'HornCleat', 'InkBottle', 'Kunai',
                        'Letter Opener', 'Matryoshka', 'Meat on the Bone', 'Mercury Hourglass', 'Molten Egg 2',
                        'Mummified Hand', 'Ninja Scroll', 'Ornamental Fan', 'Pantograph', 'Paper Crane', 'Paper Frog',
                        'Pear', 'Question Card', 'Self Forming Clay', 'Shuriken', 'Singing Bowl', 'StrikeDummy',
                        'Sundial', 'Symbiotic Virus', 'TeardropLocket', 'The Courier', 'Toxic Egg 2',
                        'White Beast Statue', 'Bird Faced Urn', 'Calipers', 'CaptainsWheel', 'Champion Belt',
                        'Charon\'s Ashes', 'CloakClasp', 'Dead Branch', 'Du-Vu Doll', 'Emotion Chip', 'FossilizedHelix',
                        'Gambling Chip', 'Ginger', 'Girya', 'GoldenEye', 'Ice Cream', 'Incense Burner', 'Lizard Tail',
                        'Magic Flower', 'Mango', 'Old Coin', 'Peace Pipe', 'Pocketwatch', 'Prayer Wheel', 'Shovel',
                        'StoneCalendar', 'The Specimen', 'Thread and Needle', 'Tingsha', 'Torii', 'Tough Bandages',
                        'TungstenRod', 'Turnip', 'Unceasing Top', 'WingedGreaves', 'Astrolabe', 'Black Blood',
                        'Black Star', 'Busted Crown', 'Calling Bell', 'Coffee Dripper', 'Cursed Key', 'Ectoplasm',
                        'Empty Cage', 'FrozenCore', 'Fusion Hammer', 'HolyWater', 'HoveringKite', 'Inserter',
                        'Mark of Pain', 'Nuclear Battery', 'Pandora\'s Box', 'Philosopher\'s Stone',
                        'Ring of the Serpent', 'Runic Cube', 'Runic Dome', 'Runic Pyramid', 'SacredBark',
                        'SlaversCollar', 'Snecko Eye', 'Sozu', 'Tiny House', 'Velvet Choker', 'VioletLotus',
                        'WristBlade', 'Bloody Idol', 'CultistMask', 'Enchiridion', 'FaceOfCleric', 'Golden Idol',
                        'GremlinMask', 'Mark of the Bloom', 'MutagenicStrength', 'Nloth\'s Gift', 'NlothsMask',
                        'Necronomicon', 'NeowsBlessing', 'Nilry\'s Codex', 'Odd Mushroom', 'Red Mask', 'Spirit Poop',
                        'SsserpentHead', 'WarpedTongs', 'Brimstone', 'Cauldron', 'Chemical X', 'ClockworkSouvenir',
                        'DollysMirror', 'Frozen Eye', 'HandDrill', 'Lee\'s Waffle', 'Medical Kit', 'Melange',
                        'Membership Card', 'OrangePellets', 'Orrery', 'PrismaticShard', 'Runic Capacitor', 'Sling',
                        'Strange Spoon', 'TheAbacus', 'Toolbox', 'TwistedFunnel'}

    BASE_GAME_POTIONS = {'BloodPotion', 'Poison Potion', 'FocusPotion', 'BottledMiracle', 'Block Potion',
                         'Dexterity Potion', 'Energy Potion', 'Explosive Potion', 'Fire Potion', 'Strength Potion',
                         'Swift Potion', 'Weak Potion', 'FearPotion', 'AttackPotion', 'SkillPotion', 'PowerPotion',
                         'ColorlessPotion', 'SteroidPotion', 'SpeedPotion', 'BlessingOfTheForge',
                         'TestModSTS:PlaceholderPotion', 'ElixirPotion', 'CunningPotion', 'PotionOfCapacity',
                         'StancePotion', 'Regen Potion', 'Ancient Potion', 'LiquidBronze', 'GamblersBrew',
                         'EssenceOfSteel', 'DuplicationPotion', 'DistilledChaos', 'LiquidMemories', 'HeartOfIron',
                         'GhostInAJar', 'EssenceOfDarkness', 'Ambrosia', 'CultistPotion', 'Fruit Juice', 'SneckoOil',
                         'FairyPotion', 'SmokeBomb', 'EntropicBrew'}

    BASE_GAME_ATTACKS = {'Immolate', 'Anger', 'Cleave', 'Reaper', 'Iron Wave', 'Reckless Charge', 'Hemokinesis',
                         'Body Slam', 'Blood for Blood', 'Clash', 'Thunderclap', 'Pummel', 'Pommel Strike',
                         'Twin Strike', 'Bash', 'Clothesline', 'Rampage', 'Sever Soul', 'Whirlwind', 'Fiend Fire',
                         'Headbutt', 'Wild Strike', 'Heavy Blade', 'Searing Blow', 'Feed', 'Bludgeon',
                         'Perfected Strike', 'Carnage', 'Dropkick', 'Sword Boomerang', 'Uppercut', 'Strike_R',
                         'Grand Finale', 'Glass Knife', 'Underhanded Strike', 'Dagger Spray', 'Bane', 'Unload',
                         'Dagger Throw', 'Choke', 'Poisoned Stab', 'Endless Agony', 'Riddle With Holes', 'Skewer',
                         'Quick Slash', 'Finisher', 'Die Die Die', 'Heel Hook', 'Eviscerate', 'Dash', 'Backstab',
                         'Slice', 'Flechettes', 'Masterful Stab', 'Strike_G', 'Neutralize', 'Sucker Punch',
                         'All Out Attack', 'Flying Knee', 'Predator', 'Go for the Eyes', 'Core Surge', 'Ball Lightning',
                         'Sunder', 'Streamline', 'Compile Driver', 'All For One', 'Blizzard', 'Barrage',
                         'Meteor Strike', 'Rebound', 'Melter', 'Gash', 'Sweeping Beam', 'FTL', 'Rip and Tear', 'Lockon',
                         'Scrape', 'Beam Cell', 'Cold Snap', 'Strike_B', 'Thunder Strike', 'Hyperbeam',
                         'Doom and Gloom', 'Consecrate', 'BowlingBash', 'WheelKick', 'FlyingSleeves', 'JustLucky',
                         'FlurryOfBlows', 'TalkToTheHand', 'WindmillStrike', 'CarveReality', 'Wallop', 'SashWhip',
                         'Eruption', 'LessonLearned', 'CutThroughFate', 'ReachHeaven', 'Ragnarok', 'FearNoEvil',
                         'SandsOfTime', 'Conclude', 'FollowUp', 'Brilliance', 'CrushJoints', 'Tantrum', 'Weave',
                         'SignatureMove', 'Strike_P', 'EmptyFist', 'Shiv', 'Dramatic Entrance', 'RitualDagger', 'Bite',
                         'Smite', 'Expunger', 'HandOfGreed', 'Flash of Steel', 'ThroughViolence', 'Swift Strike',
                         'Mind Blast'}

    BASE_GAME_ATTACKS_AND_UPGRADES = BASE_GAME_ATTACKS | {upgrade_card(x) for x in BASE_GAME_ATTACKS} | {'Searing Blow+2', 'Searing Blow+3',
                         'Searing Blow+4', 'Searing Blow+5', 'Searing Blow+6', 'Searing Blow+7', 'Searing Blow+8',
                         'Searing Blow+9', 'Searing Blow+10', 'Searing Blow+11', 'Searing Blow+12', 'Searing Blow+13',
                         'Searing Blow+14', 'Searing Blow+15', 'Searing Blow+16', 'Searing Blow+17'}

    BASE_GAME_TEMP_ATTACKS = {'Shiv', 'Smite', 'Expunger', 'ThroughViolence'}

    BASE_GAME_TEMP_ATTACKS_AND_UPGRADES = BASE_GAME_TEMP_ATTACKS | {upgrade_card(x) for x in BASE_GAME_TEMP_ATTACKS}

    BASE_GAME_DECK_ATTACKS = BASE_GAME_ATTACKS - BASE_GAME_TEMP_ATTACKS

    BASE_GAME_DECK_ATTACKS_AND_UPGRADES = BASE_GAME_ATTACKS_AND_UPGRADES - BASE_GAME_TEMP_ATTACKS_AND_UPGRADES

    BASE_GAME_SKILLS = {'Spot Weakness', 'Warcry', 'Offering', 'Exhume', 'Power Through', 'Dual Wield', 'Flex',
                        'Infernal Blade', 'Intimidate', 'True Grit', 'Impervious', 'Shrug It Off', 'Flame Barrier',
                        'Burning Pact', 'Shockwave', 'Seeing Red', 'Disarm', 'Armaments', 'Havoc', 'Rage',
                        'Limit Break', 'Entrench', 'Defend_R', 'Sentinel', 'Battle Trance', 'Second Wind',
                        'Bloodletting', 'Ghostly Armor', 'Double Tap', 'Crippling Poison', 'Cloak And Dagger',
                        'Storm of Steel', 'Deadly Poison', 'Leg Sweep', 'Bullet Time', 'Catalyst', 'Tactician',
                        'Blade Dance', 'Deflect', 'Night Terror', 'Expertise', 'Blur', 'Setup', 'Burst', 'Acrobatics',
                        'Doppelganger', 'Adrenaline', 'Calculated Gamble', 'Escape Plan', 'Terror', 'Phantasmal Killer',
                        'Malaise', 'Reflex', 'Survivor', 'Defend_G', 'Corpse Explosion', 'Venomology', 'Bouncing Flask',
                        'Backflip', 'Outmaneuver', 'Concentrate', 'Prepared', 'PiercingWail', 'Distraction',
                        'Dodge and Roll', 'Genetic Algorithm', 'Zap', 'Steam Power', 'Fission', 'Glacier', 'Consume',
                        'Redo', 'Fusion', 'Amplify', 'Reboot', 'Aggregate', 'Chaos', 'Stack', 'Seek', 'Rainbow',
                        'Chill', 'BootSequence', 'Coolheaded', 'Tempest', 'Turbo', 'Undo', 'Force Field', 'Darkness',
                        'Double Energy', 'Reinforced Body', 'Conserve Battery', 'Defend_B', 'Dualcast', 'Auto Shields',
                        'Reprogram', 'Hologram', 'Leap', 'Recycle', 'Skim', 'White Noise', 'Multi-Cast', 'Steam',
                        'DeusExMachina', 'Vengeance', 'Sanctity', 'Halt', 'Protect', 'Indignation', 'ThirdEye',
                        'ForeignInfluence', 'Crescendo', 'SpiritShield', 'ClearTheMind', 'EmptyBody', 'WreathOfFlame',
                        'Collect', 'InnerPeace', 'Omniscience', 'Wish', 'DeceiveReality', 'Alpha', 'Vault', 'Scrawl',
                        'Blasphemy', 'Defend_P', 'WaveOfTheHand', 'Meditate', 'Perseverance', 'Swivel', 'Worship',
                        'Vigilance', 'PathToVictory', 'Evaluate', 'EmptyMind', 'Prostrate', 'ConjureBlade', 'Judgement',
                        'Pray', 'Beta', 'Dark Shackles', 'J.A.X.', 'PanicButton', 'Trip', 'FameAndFortune',
                        'Impatience', 'The Bomb', 'Insight', 'Miracle', 'Blind', 'Bandage Up', 'Secret Technique',
                        'Deep Breath', 'Violence', 'Secret Weapon', 'Apotheosis', 'Forethought', 'Enlightenment',
                        'Purity', 'Panacea', 'Transmutation', 'Ghostly', 'Chrysalis', 'Discovery', 'Finesse',
                        'Master of Strategy', 'Good Instincts', 'Jack Of All Trades', 'Safety', 'Metamorphosis',
                        'Thinking Ahead', 'Madness'}

    BASE_GAME_SKILLS_AND_UPGRADES = BASE_GAME_SKILLS | {upgrade_card(x) for x in BASE_GAME_SKILLS}

    BASE_GAME_TEMP_SKILLS = {'Beta' 'Insight', 'Miracle', 'Safety'}

    BASE_GAME_TEMP_SKILLS_AND_UPGRADES = BASE_GAME_TEMP_SKILLS | {upgrade_card(x) for x in BASE_GAME_TEMP_SKILLS}

    BASE_GAME_DECK_SKILLS = BASE_GAME_SKILLS - BASE_GAME_TEMP_SKILLS

    BASE_GAME_DECK_SKILLS_AND_UPGRADES = BASE_GAME_SKILLS_AND_UPGRADES - BASE_GAME_TEMP_SKILLS_AND_UPGRADES

    BASE_GAME_POWERS = {'Inflame', 'Brutality', 'Juggernaut', 'Berserk', 'Metallicize', 'Combust', 'Dark Embrace',
                        'Barricade', 'Feel No Pain', 'Corruption', 'Rupture', 'Demon Form', 'Fire Breathing', 'Evolve',
                        'A Thousand Cuts', 'After Image', 'Tools of the Trade', 'Caltrops', 'Wraith Form v2', 'Envenom',
                        'Well Laid Plans', 'Noxious Fumes', 'Infinite Blades', 'Accuracy', 'Footwork', 'Storm',
                        'Hello World', 'Creative AI', 'Echo Form', 'Self Repair', 'Loop', 'Static Discharge',
                        'Heatsinks', 'Buffer', 'Electrodynamics', 'Machine Learning', 'Biased Cognition', 'Capacitor',
                        'Defragment', 'Wireheading', 'BattleHymn', 'DevaForm', 'LikeWater', 'Establishment', 'Fasting2',
                        'Adaptation', 'MentalFortress', 'Study', 'Devotion', 'Nirvana', 'MasterReality',
                        'Sadistic Nature', 'LiveForever', 'BecomeAlmighty', 'Panache', 'Mayhem', 'Magnetism', 'Omega'}

    BASE_GAME_POWERS_AND_UPGRADES = BASE_GAME_POWERS | {upgrade_card(x) for x in BASE_GAME_POWERS}

    BASE_GAME_TEMP_POWERS = {'Omega'}

    BASE_GAME_TEMP_POWERS_AND_UPGRADES = BASE_GAME_TEMP_POWERS | {upgrade_card(x) for x in BASE_GAME_TEMP_POWERS}

    BASE_GAME_DECK_POWERS = BASE_GAME_POWERS - BASE_GAME_TEMP_POWERS

    BASE_GAME_DECK_POWERS_AND_UPGRADES = BASE_GAME_POWERS_AND_UPGRADES - BASE_GAME_TEMP_POWERS_AND_UPGRADES

    BASE_GAME_CURSES = {'Regret', 'Writhe', 'AscendersBane', 'Decay', 'Necronomicurse', 'Pain', 'Parasite', 'Doubt',
                        'Injury', 'Clumsy', 'CurseOfTheBell', 'Normality', 'Pride', 'Shame'}

    BASE_GAME_STATUSES = {'Burn', 'Dazed', 'Slimed', 'Void', 'Wound'}

    BASE_GAME_STATUSES_AND_UPGRADES = {'Burn', upgrade_card('Burn'), 'Dazed', 'Slimed', 'Void', 'Wound'}

    BASE_GAME_DECK_AND_UPGRADES = BASE_GAME_DECK_ATTACKS_AND_UPGRADES | BASE_GAME_DECK_SKILLS_AND_UPGRADES | BASE_GAME_DECK_POWERS_AND_UPGRADES

    BASE_GAME_CARDS_AND_UPGRADES = BASE_GAME_ATTACKS_AND_UPGRADES | BASE_GAME_SKILLS_AND_UPGRADES | BASE_GAME_POWERS_AND_UPGRADES | BASE_GAME_CURSES | BASE_GAME_STATUSES_AND_UPGRADES
