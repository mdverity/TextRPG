#   + - - - - - - - - - - - - +
#   |       Matt Verity       |
#   |  ASCII Dungeon-Crawler  |
#   |      April 3 2019       |
#   |          v 1.0          |
#   |      Python 3.7.2       |
#   + - - - - - - - - - - - - +
#   |    Updated: 05/14/19    |
#   + - - - - - - - - - - - - +

import mapList, characterClass, mapItemClass, itemGen, intro, splash
from os import system, path
from time import sleep
from msvcrt import getch, kbhit
from pygame import mixer
import pickle
import random


def make_map(importedMap):
    exportMap = []
    tempLine = []

    for j in importedMap:
        for k in j:
            tempLine.append(k)
        exportMap.append(tempLine)
        tempLine = []

    return exportMap


def map_setup():
    global portalList, chestList, bossChestList

    portalList, chestList, bossChestList = [], [], []

    counters = {'map': 1, 'regChest': 0, 'bossChest': 0}

    # Set up this way to account for multiple regular chests in map, but couldn't get that working in time.
    for i in range(len(gameMap)):
        for j in range(len(gameMap[i])):
            if gameMap[i][j] == "X":
                chestList.append(mapItemClass.Chest(i, j))
                chestList[counters['regChest']].fillChest()
                counters['regChest'] += 1
            if gameMap[i][j] == "B":
                bossChestList.append(mapItemClass.BossChest(i, j))
                bossChestList[counters['bossChest']].fillChest()
                counters['bossChest'] += 1
            if gameMap[i][j] == "O":
                portalList.append(mapItemClass.Portal(i, j, counters['map']))
                counters['map'] += 1
            if gameMap[i][j] == "=":
                portalList.append(mapItemClass.Portal(i, j, 9))

    # If mapCounter was incremented once (only one portal in the map), set the portal to Map 0.
    if counters['map'] == 2:
        portalList[0].setMap(0)


def refresh_map(player):
    global gameMap

    gameMap = make_map(mapList.maps[int(player.getLoc())])


def print_menu(menu):
    print("\u250c" + "\u2500" * 23 + "\u2510")
    for i in menu:
        print("\u2502" + i + "\u2502")
    print("\u2514" + "\u2500" * 23 + "\u2518")


def music_switch():
    global musicOn

    if musicOn:
        mixer.music.pause()
        musicOn = False
    elif not musicOn:
        mixer.music.unpause()
        musicOn = True


def flush_input():
    while kbhit():
        getch()


def transition(player, speed=2):
    if speed == 2:
        for i in range(player.getY() - 6, player.getY() + 6):
            for j in range(player.getX() - 6, player.getX() + 6):
                gameMap[j][i] = "#"
                mapList.print_map(player, gameMap)
            system('cls')
    elif speed == 1:
        for i in range(player.getX() - 6, player.getX() + 6):
            for j in range(player.getY() - 6, player.getY() + 6):
                gameMap[i][j] = "#"
            mapList.print_map(player, gameMap)
            system('cls')


def display_map(P):
    system('cls')
    print("\n")
    viewMap = ["                       ",
               "           O           ",
               "                       ",
               "       O   |   O       ",
               "         \\ | /         ",
               "          \\|/          ",
               "     O --- C --- O     ",
               "          /|\\          ",
               "         / | \\         ",
               "       O   |   O       ",
               "                       ",
               "           O           ",
               "                       "]

    totalRooms = []
    portalText = []
    mapCounter = 1

    for i in range(len(viewMap)):
        for j in range(len(viewMap[i])):
            if viewMap[i][j] == "O":
                totalRooms.append(mapCounter)
                mapCounter += 1

    for i in totalRooms:
        if i == P.getLoc():
            portalText.append("X")
        else:
            portalText.append("O")

    if P.getLoc() == 0:
        portalText.append("X")
    else:
        portalText.append("C")

    viewMap = ["                       ",
               "           {}           ".format(portalText[0]),
               "      {}    |    {}      ".format(portalText[1], portalText[2]),
               "        \\  |  /        ",
               "         \\ v /         ",
               "                       ",
               "    {} ---> {} <--- {}    ".format(portalText[3], portalText[8], portalText[4]),
               "                       ",
               "         / ^ \\         ",
               "        /  |  \\        ",
               "      {}    |    {}      ".format(portalText[5], portalText[6]),
               "           {}           ".format(portalText[7]),
               "                       "]

    print_menu(viewMap)
    print("\n O: PORTALS      C: CENTER CHAMBER")
    print("        X: YOUR LOCATION")
    print("\n Press ENTER to return.")
    input()


def combat_check(P):
    # Called every time the player moves, combat only occurs if combatRoll == 1
    # To change combat frequency, increase/decrease combatRoll's range.

    combatRoll = random.randint(1, 100)
    # combatRoll = 1

    skele = ["Skeleton", 25 + (5 * P.getLevel()), 10, 5 + (5 * P.getLevel())]
    zombie = ["Zombie", 40 + (5 * P.getLevel()), 20, 15 + (5 * P.getLevel())]
    ogre = ["Ogre", 50 + (10 * P.getLevel()), 20, 20 + (10 * P.getLevel())]

    if combatRoll <= 5:
        mobList = [skele, skele, skele, skele, skele, skele,
                   zombie, zombie, zombie,
                   ogre]

        randomMob = random.choice(mobList)

        transition(P, 1)
        system('cls')
        print("\n\n\n\n\n")
        vc = ["An" if randomMob[0][0].lower() in "aeiou" else "A"]
        encounterText = ["   {} {} appeared!".format(vc[0], randomMob[0].lower()),
                         "   {} {} rises out of the darkness...".format(vc[0], randomMob[0].lower()),
                         "   {} {} comes up from behind you!".format(vc[0], randomMob[0].lower()),
                         "   {} {}'s cry echoes throughout the cave!".format(vc[0], randomMob[0].lower())]
        intro.slow_type([random.choice(encounterText)])
        sleep(.5)
        combat_loop(P, characterClass.Enemy(randomMob[0], randomMob[1], randomMob[2], randomMob[3]))
        refresh_map(P)


def combat_loop(P, E):
    global didRegen

    playerTurn = True
    P.resetCombat()
    P.clearBuffs()
    didRegen = False
    # While player and enemy health are above 0, and the player hasn't stopped combat.

    while P.getHP() > 0 and E.getHP() > 0 and not P.isCombatStopped():

        if playerTurn:

            # Call the combat screen to perform player's turn
            combat_screen(P, E)

            # If the player did an action, flag their turn as over.
            if P.actionCheck():
                if E.getHP() > 0:
                    P.checkBuff(E)
                    P.buffDown()
                playerTurn = False

        elif not playerTurn and isinstance(E, characterClass.Enemy):
            if "Freeze" in P.getBuffs():
                intro.slow_type(["The {} is frozen solid!".format(E.getName().lower())])
            else:
                # Roll for the enemy's action: <= 3 attacks, 4 heals.
                enemyChoice = random.randint(1, 4)

                if enemyChoice <= 3:
                    E.attack(P)

                # Enemy heal
                elif enemyChoice == 4:
                    if E.getHP() != E.maxHP():
                        E.selfHeal()
                    else:
                        E.attack(P)

            sleep(1)
            playerTurn = True

        elif not playerTurn and isinstance(E, characterClass.Boss):
            if "Freeze" in P.getBuffs():
                intro.slow_type(["{} is frozen solid!".format(E.getName())])
            else:
                E.attack(P, E.getDamage())
            playerTurn = True

        if E.getHP() <= 0:
            P.addExp(E)

    P.didBattle = True


def combat_screen(P, E):
    global didRegen

    P.didAction(False)
    system('cls')

    # Check if player is a mage, if they don't have max mana, add 5.
    if P.getProf() == "Mage" and P.getMP() < P.getMaxMP() and not didRegen:
        if P.getLevel() < 5:
            P.setMP(P.getMP() + 5)
        else:
            P.setMP(P.getMP() + 10)
        didRegen = True

        # If they regenerated over maximum amount (50), set mana to 50.

    combatMenu1 = ["{}{}".format(P.getName(), " " * (23 - (len(P.getName())))),
                   "the{}{}".format(" " * (20 - len(E.getName())), E.getName()),
                   "{}{}".format(P.getProf(), " " * (23 - len(P.getProf()))),
                   "                       ",
                   "HP: {}/{}{}HP: {}".format(
                       P.getHP(), P.getMaxHP(), " " * (11 - len(str(P.getHP())) - len(str(E.getHP()))), E.getHP()),
                   "MP: {}/{}{}".format(P.getMP(), P.getMaxMP(), " " * (16 - len(str(P.getMP())))),
                   "                       ",
                   "                       ",
                   "                       ",
                   "                       ",
                   "                       ",
                   "1: Attack      3: Items",
                   "2: Spells      4:  Run "]

    combatMenu2 = ["{}{}{}".format(P.getName(), " " * (23 - len(P.getName()) - len(E.getName())), E.getName()),
                   "the                 the",
                   "{}{}{}".format(P.getProf(), " " * (23 - len(P.getProf()) - len(E.getProf())), E.getProf()),
                   "                       ",
                   "HP: {}/{}{}HP: {}".format(
                       P.getHP(), P.getMaxHP(), " " * (11 - len(str(P.getHP())) - len(str(E.getHP()))), E.getHP()),
                   "MP: {}/{}{}MP: {}".format(
                       P.getMP(), P.getMaxMP(), " " * (12 - len(str(P.getMP())) - len(str(E.getMP()))), E.getMP()),
                   "                       ",
                   "                       ",
                   "                       ",
                   "                       ",
                   "                       ",
                   "1: Attack     2: Spells",
                   "        3: Items       "]

    if E.getProf() == "Monster":
        print_menu(combatMenu1)
        acceptableAnswers = ["b'1'", "b'2'", "b'3'", "b'4'"]
    else:
        print_menu(combatMenu2)
        acceptableAnswers = ["b'1'", "b'2'", "b'3'"]

    if didRegen:
        intro.slow_type(["\n You regenerated some mana..."])

    flush_input()

    # ans = input(" >> ")
    ans = str(getch()).lower()

    while ans not in acceptableAnswers:
        ans = str(getch()).lower()

    if ans == "b'1'":
        P.attack(E)
        didRegen = False
    elif ans == "b'2'":
        if P.castSpell(E):
            didRegen = False
    elif ans == "b'3'":
        P.checkInv()
    elif ans == "b'4'" and E.getProf() == "Monster":
        escapeChance = random.randint(1, 10)
        if escapeChance <= 5:
            intro.slow_type(["\n\tYou just barely escaped!"])
            P.stopCombat()
        else:
            lines = ["\n\tAttempting to escape, you trip and fall in the darkness!",
                     "\n\tIn attempt to run away, the monster grabs you!",
                     "\n\tYou find yourself too winded to run away..."]
            intro.slow_type([random.choice(lines)])
            P.didAction(True)
            sleep(1)
        didRegen = False


def outro():
    system('cls')
    intro.slow_type(["\n\n\n\tImpossible...",
                     "\n\n\tI ", "won't ", "be", ".", ".", ".",
                     "\n\n\t   Ugh..."])
    sleep(2)
    system('cls')
    intro.slow_type(["\n\n\n\n\t  V", " ", "I", " ", "C", " ", "T", " ", "O", " ", "R", " ", "Y", " ", "!",
                     "\n\n\tThanks for playing!", "",
                     "\n\t   Play again?:"])
    ans = input("\t     >> ")
    if "y" in ans.lower():
        main()
    else:
        quit()


def player_move(P):
    bossBattle = False
    # print("\t\t\t\tLvl. {}".format(P.getLevel()))
    controls = ["\n\n W: UP\t   S: DOWN",
                "\n A: LEFT   D: RIGHT\t           HP:{}{} /{}\t\t         Lvl. {}"
                .format(" " * (5 - len(str(P.getHP()))), P.getHP(), P.getMaxHP(), P.getLevel()),
                "\n\t\t\t           MP:{}{} /{}"
                .format(" " * (5 - len(str(P.getMP()))), P.getMP(), P.getMaxMP()),
                "\n E: USE\t   B: INVENTORY\t           XP:{}{} /{}\t\t     {} the {}"
                .format(" " * (5 - len(str(P.getExp()))), P.getExp(), P.getExpReq(), P.getName(), P.getProf()),
                "\n X: MUSIC  M: MAP\t         KEYS:    {} /2  ".format(P.getKeys())]
    for i in controls:
        print(i, end="")

    # Flush input
    flush_input()

    playerInput = str(getch()).lower()
    # playerInput = input(" >> ")

    nullChars = "BXO#=-+/|\\"

    checkSpot = [gameMap[P.getX() - 1][P.getY()],
                 gameMap[P.getX() + 1][P.getY()],
                 gameMap[P.getX()][P.getY() - 1],
                 gameMap[P.getX()][P.getY() + 1]]

    # Input checking - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # getch() returns "b'<key>'" when changed to a string, unless you use .decode() on it (it usually returns bytecode)
    # I had trouble getting ESC as input once decoded, however. I decided to just use the "b'<key>'" string for checks.
    # - checkSpot refers to all the locations within 1 space of the player

    if playerInput == "b'e'":
        if "O" in checkSpot:
            print("\n\n\tTravel to the next area? (yes/no)")
            if "y" in input("\t >> "):
                for portal in portalList:
                    portal.checkPortal(P)

                transition(P)
                refresh_map(P)
                map_setup()
                for i in range(len(gameMap)):
                    for j in range(len(gameMap[i])):
                        if gameMap[i][j] == "O":
                            P.setX(i)
                            P.setY(j - 1)
                        elif gameMap[i][j] == "x":
                            P.setX(i)
                            P.setY(j)

        elif "=" in checkSpot and P.getLoc() == 0:
            intro.slow_type(["\n\tThere appears to be two keyholes on the wall here..."])
            if P.getKeys() >= 2:
                intro.slow_type(["\tInsert keys?"])
                ans = input("\t >> ")
                if "y" in ans:
                    intro.slow_type(["\n\tThe wall seemingly caves upon itself as a pathway opens..."])
                    sleep(.5)
                    for portal in portalList:
                        portal.checkPortal(P)

                    transition(P)
                    refresh_map(P)
                    for i in range(len(gameMap)):
                        for j in range(len(gameMap[i])):
                            if gameMap[i][j] == "O":
                                P.setX(i)
                                P.setY(j - 1)
                            elif gameMap[i][j] == "x":
                                P.setX(i)
                                P.setY(j)

                    for _ in range(2):
                        P.removeKey()
            else:
                intro.slow_type(["\tMaybe you should return after you've found something that fits."])
                sleep(1)

        elif "X" in checkSpot:
            print("\n\tOpen the chest? (yes/no)")
            ans = input("\t >> ")

            if "y" in ans:
                for chest in chestList:
                    chest.checkChest(P)
                    print("\n\tLoot the items? (yes/no)")
                    ans = input("\t >> ")
                    if "y" in ans:
                        if isinstance(chest, mapItemClass.Chest):
                            chest.moveItems(P)

        elif "B" in checkSpot:
            bossBattle = True
            transition(P)
            system('cls')
            if not bossChestList[0].bossDefeated():
                bossNames = ["Hadriel", "Aphaelon", "Erathol", "Asteroth"]

                randName = random.choice(bossNames)

                introLines = [
                    ["\n\n\n\tFeeble {}, you think yourself powerful enough to face me?".format(P.getProf().lower()),
                     "\n\n\tI, {}, will destroy you!".format(randName)],
                    ["\n\n\n\tFoolish {}, you feel fit to challenge the mighty {}?!".format(P.getProf().lower(), randName),
                     "\n\n\tPrepare to be crushed!"],
                    ["\n\n\n\tI will leave your body amongst this rubble, {}!".format(P.getProf().lower()),
                     "\n\n\tMy name is {}, and I take no prisoners.".format(randName)],
                    ["\n\n\n\tYou were unwise to come here, {}. I cannot allow you to progress any further.".format(
                     P.getProf().lower()),
                     "\n\n\tI am {}, and I guard this treasure with my life!".format(randName)]]

                randLines = random.choice(introLines)

                intro.slow_type(randLines)
                sleep(1)

                combat_loop(P, characterClass.Boss(randName, 65 + (P.getLevel() * 10), 50, 40 + (10 * P.getLevel()), "Guardian"))
                intro.slow_type(["You gained a KEY!"])
                P.addKey()

            print("\n\tOpen the chest? (yes/no)")
            ans = input("\t >> ")

            if "y" in ans:
                for chest in bossChestList:
                    chest.checkChest(P)
                    print("\n\tLoot the items? (yes/no)")
                    ans = input("\t >> ")
                    if "y" in ans:
                        chest.moveItems(P)

            refresh_map(P)

    elif playerInput == "b'h'":
        import helpScreen
        helpScreen.menu()
        ans = input("\n")
        if ans == "gimmiedaloot":
            P.addItem(itemGen.Weapon("Obsidian Greatsword", 150, 3, 100, 50))
            P.addItem(itemGen.Potion("Superior Health Potion", 50))
            P.addKey()
            P.addKey()
        elif ans == "theonetrueking":
            P.setMaxHP(1000)
            P.setHP(P.getMaxHP())
        elif ans == "enoughofthismadness":
            mixer.music.fadeout(6000)
            system('cls')
            intro.slow_type(["\n\n\n\tHa..", "Ha..", "Ha...",
                             "\n\n\tYou thought you could escape so easily, impudent mortal?",
                             "\n\n\tYour soul... it will be mine, like all the rest!"])
            mixer.music.load("insomnia.mp3")
            mixer.music.play()
            E = characterClass.Boss("Kilvath", 1, 0, 100, "Soulkeeper")
            combat_loop(P, E)
            if E.getHP() <= 0:
                mixer.music.fadeout(6500)
                outro()

    elif playerInput == "b'w'":
        if P.getLoc() == 9 and gameMap[P.getX()][P.getY()] == gameMap[13][6]:
            transition(P, 1)
            mixer.music.fadeout(10000)
            system('cls')
            intro.slow_type(["\n\n\n\tThose who would travel any further...",
                             "\n\n", "\tBe wary", ".", ".", "of the darkness", ".", ".", "."])
            sleep(1)
            refresh_map(P)
            P.setX(P.getX() - 1)

        elif P.getLoc() == 9 and gameMap[P.getX()][P.getY()] == gameMap[6][6]:
            system('cls')
            intro.slow_type(["\n\n\n\tHa..", "Ha..", "Ha...",
                             "\n\n\tYou thought you could escape so easily, impudent mortal?",
                             "\n\n\tYour soul... it will be mine, like all the rest!"])
            mixer.music.load("insomnia.mp3")
            if musicOn:
                mixer.music.play()
            sleep(.5)
            E = characterClass.Boss("Kilvath", 85 + (15 * P.getLevel()), 60, 100, "Soulkeeper")
            combat_loop(P, E)
            if E.getHP() <= 0:
                mixer.music.fadeout(6500)
                outro()

        elif checkSpot[0] not in nullChars:
            gameMap[P.getX()][P.getY()] = " "
            P.setX(P.getX() - 1)

    elif playerInput == "b'a'" and checkSpot[2] not in nullChars:
        gameMap[P.getX()][P.getY()] = " "
        P.setY(P.getY() - 1)

    elif playerInput == "b's'" and checkSpot[1] not in nullChars:
        gameMap[P.getX()][P.getY()] = " "
        P.setX(P.getX() + 1)

    elif playerInput == "b'd'" and checkSpot[3] not in nullChars:
        gameMap[P.getX()][P.getY()] = " "
        P.setY(P.getY() + 1)

    elif playerInput == "b'b'":
        P.checkInv()

    elif playerInput == "b'x'":
        music_switch()

    elif playerInput == "b'm'":
        display_map(P)

    elif playerInput == "b'p'":
        saveGame(P)

    elif playerInput == "b'\\x1b'":
        print("\n\n >> Thanks for playing!")
        sleep(2)
        quit()

    if P.getLoc() != 0 and P.getLoc() != 9 and not bossBattle and not P.didBattle:
        combat_check(P)

    P.didBattle = False
    sleep(.01)


def saveGame(player):
    fileName = "saves/" + player.getName().lower() + player.getProf().lower() + ".txt"
    if path.isfile(fileName):
        ans = input("\n\n Save exists. Overwrite? (yes/no) : ")
        if "y" in ans:
            saveFile = open(fileName, "wb")
            pickle.dump(player, saveFile)
            saveFile.close()
            print("\n Your progress has been saved.")
            sleep(.5)
    else:
        saveFile = open(fileName, "wb")
        pickle.dump(player, saveFile)
        saveFile.close()
        print("\n\n Your progress has been saved.")
        sleep(.5)


def loadGame():
    try:
        name = input("\n\t\t\t      Enter character's name: ").lower()
        prof = input("\n\t\t\tEnter character's profession: ").lower()
        fileName = "saves/" + name + prof + ".txt"
        saveFile = open(fileName, "rb")
        loadedData = pickle.load(saveFile)
        saveFile.close()

        return loadedData
    except FileNotFoundError:
        print("\n\n\t\t\t\t Character not found.")
        sleep(2)
        main()


def main():
    global musicOn

    system("mode con cols=95 lines=31")
    splash.splashScreen()

    mixer.init()
    mixer.music.load("racecar.mp3")
    musicOn = True
    sfx = ["ON" if musicOn else "OFF"]

    print(splash.startMenu().format(sfx[0]))
    gameChoice = splash.menuInput()
    finished = False

    while not finished:
        if gameChoice == 1:
            system('cls')

            # Introduction text
            intro.intro1()

            # Make player
            Player1 = characterClass.make_player()

            # Give starting items
            Player1.addItem(itemGen.Weapon("Wooden Sword", 10, 3, 15, 20))
            Player1.addItem(itemGen.Potion("Health Potion", 20))

            # Combat testing lines (normally commented out):
            # combat_loop(Player1, characterClass.Enemy("Zombie", 50, 20))
            # combat_loop(Player1, characterClass.Boss("Leeroy", 100, 50, "Guardian"))

            mixer.music.play(-1)
            if not musicOn:
                mixer.music.pause()

            # Introduction text #2
            intro.intro2()
            finished = True

        elif gameChoice == 2:
            Player1 = loadGame()
            mixer.music.play(-1)

            if not musicOn:
                mixer.music.pause()
            finished = True

        elif gameChoice == 3:
            music_switch()
            sfx = ["ON" if musicOn else "OFF"]
            print(splash.startMenu().format(sfx[0]))
            gameChoice = splash.menuInput()

        else:
            quit()

    # Build map
    refresh_map(Player1)
    map_setup()

    # Gameplay loop
    while True:
        mapList.print_map(Player1, gameMap)
        player_move(Player1)


if __name__ == '__main__':
    main()
