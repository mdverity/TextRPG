class MapItem(object):

    def __init__(self, xLoc, yLoc):
        self.__xLoc = xLoc
        self.__yLoc = yLoc

    def __str__(self):
        return "X"

    def getX(self):
        return self.__xLoc

    def getY(self):
        return self.__yLoc


class Portal(MapItem):
    def __init__(self, x, y, gameMap):
        super().__init__(x, y)
        self.__gameMap = gameMap

    def __str__(self):
        result = super().__str__()
        result += "Map: {}\n".format(str(self.__gameMap))
        return result

    def getMap(self):
        return self.__gameMap

    def setMap(self, mapInList):
        self.__gameMap = mapInList

    def checkPortal(self, player):
        if self.getY() == player.getY() - 1 or self.getY() == player.getY() + 1:
            if self.getX() == player.getX():
                player.setLoc(self.getMap())
        elif self.getX() == player.getX() - 1 or self.getX() == player.getX() + 1:
            if self.getY() == player.getY():
                player.setLoc(self.getMap())


class Chest(MapItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__chestLoot = []

    def checkChest(self, player):
        if self.getY() == player.getY() - 1 or self.getY() == player.getY() + 1:
            if self.getX() == player.getX():
                print()
                if len(self.__chestLoot) > 0:
                    itemCount = 1
                    for i in self.__chestLoot:
                        print("{}) {}".format(itemCount, i))
                        itemCount += 1
                # print(self.checkLoot())
                else:
                    print("<EMPTY>")
            return self.__chestLoot

        elif self.getX() == player.getX() - 1 or self.getX() == player.getX() + 1:
            if self.getY() == player.getY():
                print()
                if len(self.__chestLoot) > 0:
                    itemCount = 1
                    for i in self.__chestLoot:
                        print("{}) {}".format(itemCount, i))
                        itemCount += 1
                # print(self.checkLoot())
                else:
                    print("<EMPTY>")
            return self.__chestLoot

    def fillChest(self):
        import itemGen
        from random import randint

        self.__chestLoot.append(itemGen.new_weapon())

        for i in range(2):
            potionChance = randint(1, 2)
            if i == 0:
                if potionChance == 1:
                    self.__chestLoot.append(itemGen.Potion("Health Potion", randint(10, 30)))
            elif i == 1:
                if potionChance == 1:
                    self.__chestLoot.append(itemGen.Potion("Mana Potion", randint(10, 20)))

    def moveItems(self, P):
        moveCounter = 0

        for i in self.__chestLoot:
            if len(P.getInv()) < 9:
                P.addItem(i)
                moveCounter += 1
            else:
                print("Too many items in inventory.")

        for _ in range(moveCounter):
            self.__chestLoot.pop(0)


class BossChest(MapItem):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__chestLoot = []
        self.__bossBeaten = False

    def bossDefeated(self):
        return self.__bossBeaten

    def checkChest(self, player):
        if self.getY() == player.getY() - 1 or self.getY() == player.getY() + 1:
            if self.getX() == player.getX():
                print()
                if len(self.__chestLoot) > 0:
                    itemCount = 1
                    for i in self.__chestLoot:
                        print("{}) {}".format(itemCount, i))
                        itemCount += 1
                # print(self.checkLoot())
                else:
                    print("<EMPTY>")
            return self.__chestLoot

        elif self.getX() == player.getX() - 1 or self.getX() == player.getX() + 1:
            if self.getY() == player.getY():
                print()
                if len(self.__chestLoot) > 0:
                    itemCount = 1
                    for i in self.__chestLoot:
                        print("{}) {}".format(itemCount, i))
                        itemCount += 1
                # print(self.checkLoot())
                else:
                    print("<EMPTY>")
            return self.__chestLoot

    def fillChest(self):
        import itemGen
        from random import randint

        self.__chestLoot.append(itemGen.new_weapon(100, 12, 75))
        self.__chestLoot.append(itemGen.new_weapon())

        for i in range(2):
            potionChance = randint(1, 2)
            if potionChance == 1 and i == 0:
                self.__chestLoot.append(itemGen.Potion("Superior Health Potion", randint(30, 60)))
            if potionChance == 1 and i == 1:
                self.__chestLoot.append(itemGen.Potion("Superior Mana Potion", randint(20, 40)))

    def moveItems(self, P):
        moveCounter = 0

        for i in self.__chestLoot:
            if len(P.getInv()) < 9:
                P.addItem(i)
                moveCounter += 1
            else:
                print("Too many items in inventory.")

        for _ in range(moveCounter):
            self.__chestLoot.pop(0)
