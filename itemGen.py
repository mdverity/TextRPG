import random


def randNum(x, y=1):
    return random.randint(y, x)


class Item(object):
    def __init__(self, name, value, weight):
        self.__name = name
        self.__value = value
        self.__weight = weight

    def __str__(self):
        result = ""
        result += "{}\t".format(self.__name)
        # result += "Value: {}\t".format(str(self.__value))
        # result += "Weight: {}\t".format(str(self.__weight))
        return result

    # Getters/Setters
    def getName(self):
        return self.__name

    def getValue(self):
        return self.__value

    def getWeight(self):
        return self.__weight

    def setName(self, newName):
        self.__name = newName

    def setValue(self, newValue):
        self.__value = newValue

    def setWeight(self, newWeight):
        self.__weight = newWeight


class Potion(Item):
    def __init__(self, n, power, v=5, w=1):
        super().__init__(n, v, w)
        self.__power = power

    def __str__(self):
        itemPow = super().__str__()
        if "health" in self.getName().lower():
            itemPow += "Restores: {} HP".format(str(self.__power))
        elif "mana" in self.getName().lower():
            itemPow += "\tRestores: {} MP".format(str(self.__power))
        return itemPow

    def getPower(self):
        return self.__power

    def usePotion(self, player):
        if "health" in self.getName().lower():
            player.setHP(player.getHP() + self.__power)
        elif "mana" in self.getName().lower():
            player.setMP(player.getMP() + self.__power)


class Weapon(Item):
    def __init__(self, n, v, w, dam, dur):
        super().__init__(n, v, w)
        self.__damage = dam
        self.__durability = dur

    def __str__(self):
        itemPow = super().__str__()
        if "Shield" in self.getName():
            itemPow += "\tArmor: {}".format(str(self.__damage // 2))
        else:
            itemPow += "\tDamage: {}".format(str(self.__damage))
        itemPow += "\tDurability: {}".format(str(self.__durability))
        return itemPow

    def getDur(self):
        return self.__durability

    def getDam(self):
        return self.__damage

    def setDur(self, newDur):
        self.__durability = newDur

        if self.__durability == 0:
            self.breakWep()
        if self.__durability < 0:
            self.__durability = 0

    def setDam(self, newDam):
        self.__damage = newDam

    def breakWep(self):
        from intro import slow_type
        self.__damage = 0
        slow_type(["\n\tYour {} broke!".format(self.getName())])
        self.setName("Broken " + self.getName())


# Can roll specific items by setting certain thresholds for roll_1:
#    -- Wooden: 15
#    -- Iron: 50
#    -- Bronze: 75
#    -- Steel: 90
#    -- Obsidian: 100 (default)
# You can even restrict the minimum roll by supplying an argument for min_roll:
#    new_weapon(100, 12, 90)
#    -- gives only Obsidian weapons

def new_weapon(roll_1=100, roll_2=12, min_roll=1):
    # Dict Format: {Weapon: [minDamage, maxDamage, durability, baseValue, baseWeight]}
    weaponTypes = {"Axe": [random.randint(15, 25), random.randint(25, 35), random.randint(10, 25), 10, 3],
                   "Greataxe": [random.randint(20, 30), random.randint(30, 45), random.randint(15, 25), 15, 6],
                   "Sword": [random.randint(10, 20), random.randint(20, 30), random.randint(10, 25), 10, 3],
                   "Greatsword": [random.randint(15, 25), random.randint(25, 40), random.randint(15, 25), 15, 6],
                   "Shield": [random.randint(10, 15), random.randint(20, 25), random.randint(15, 30), 10, 3]}

    # Chooses a key from the weaponTypes dictionary at random
    weaponChoice = random.choice(list(weaponTypes))

    # Stores the values of the key in a temporary list: [minDamage, maxDamage, durability]
    wepInfo = weaponTypes[weaponChoice]

    tempWeapon = Weapon(weaponChoice, wepInfo[3], wepInfo[4], random.randint(wepInfo[0], wepInfo[1]), wepInfo[2])

    # Prefix determines weapon base:
    prefix = ["Wooden ", "Iron ", "Bronze ", "Steel ", "Obsidian "]
    # Suffix determines any mods on weapon:
    suffix = [" of Unburdening", " of Durability", " of Brutality"]

    roll = randNum(roll_1, min_roll)

    if 1 <= roll < 15:
        tempWeapon.setName(prefix[0] + tempWeapon.getName())
        tempWeapon.setDam(tempWeapon.getDam() - 5)
        tempWeapon.setValue(tempWeapon.getValue() - 5)
    elif 15 <= roll < 50:
        tempWeapon.setName(prefix[1] + tempWeapon.getName())
        tempWeapon.setDam(tempWeapon.getDam() + 4)
        tempWeapon.setValue(tempWeapon.getValue() + 3)
    elif 50 <= roll < 75:
        tempWeapon.setName(prefix[2] + tempWeapon.getName())
        tempWeapon.setDam(tempWeapon.getDam() + 8)
        tempWeapon.setValue(tempWeapon.getValue() + 6)
    elif 75 <= roll < 90:
        tempWeapon.setName(prefix[3] + tempWeapon.getName())
        tempWeapon.setDam(tempWeapon.getDam() + 12)
        tempWeapon.setValue(tempWeapon.getValue() + 9)
    elif 90 <= roll <= 100:
        tempWeapon.setName(prefix[4] + tempWeapon.getName())
        tempWeapon.setDam(tempWeapon.getDam() + 16)
        tempWeapon.setValue(tempWeapon.getValue() + 12)

    # roll = randNum(roll_2)

    # other rolls are currently useless for game, maintaining 1/4 chance for enchant.  2/8=.25 and 3/12=.25?
    roll = random.randint(2, 8)

    if roll == 1:
        tempWeapon.setName(tempWeapon.getName() + suffix[0])
        tempWeapon.setWeight(tempWeapon.getWeight() - 3)
        tempWeapon.setValue(tempWeapon.getValue() + 7)
    elif roll == 2:
        tempWeapon.setName(tempWeapon.getName() + suffix[1])
        tempWeapon.setDur(tempWeapon.getDur() * 2)
        tempWeapon.setValue(tempWeapon.getValue() + 6)
    elif roll == 3:
        tempWeapon.setName(tempWeapon.getName() + suffix[2])
        tempWeapon.setDam(tempWeapon.getDam() + 8)
        tempWeapon.setValue(tempWeapon.getValue() + 8)

    return tempWeapon


def main():
    weaponList = []

    counter = 0

    while counter <= 10:
        weaponList.append(new_weapon())
        counter += 1

    for i in weaponList:
        print(i)


if __name__ == '__main__':
    main()
