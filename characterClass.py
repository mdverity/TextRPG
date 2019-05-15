import intro
import itemGen
from msvcrt import getch, kbhit
from time import sleep
from random import randint

profList = ["Warrior", "Mage", "Thief", "Innkeeper", "Baker", "Fisherman", "Doctor"]


class Character(object):
    totalChars = 0

    # Static method to keep track of total number of characters.
    @staticmethod
    def totalCount():
        return Character.totalChars

    def __init__(self, name, hp, mp, prof):
        self.__name = name
        self.__hp = hp
        self.__mp = mp
        self.__profession = prof
        Character.totalChars += 1

    # toString
    def __str__(self):
        result = ""
        result += "{}\n".format(self.__name)
        result += "HP: {}\n".format(str(self.__hp))
        result += "MP: {}\n".format(str(self.__mp))
        return result

    def getName(self):
        return self.__name

    def getHP(self):
        return self.__hp

    def getMP(self):
        return self.__mp

    def getProf(self):
        return self.__profession

    def setName(self, newName):
        # Input validation: 1-15 characters.
        if 0 < len(newName) < 15:
            self.__name = newName
        else:
            print("Try again, names must be between 1 - 15 characters.")

    def setProf(self, newProf):
        if newProf in profList[:3]:
            self.__profession = newProf
        else:
            print("Invalid profession.")

    def setHP(self, newHP):
        from time import sleep

        # Input validation: health above 0.
        if newHP > 0:
            self.__hp = newHP
            if isinstance(self, Player) and newHP > self.getMaxHP():
                self.__hp = self.getMaxHP()
        elif newHP <= 0:
            self.__hp = newHP
            if self.getProf() == "Monster":
                intro.slow_type(["\n\tThe " + self.__name.lower() + " has died.\n"])
            else:
                intro.slow_type(["\n\t" + self.__name + " has died.\n"])
            sleep(.5)

            if isinstance(self, Player):
                sleep(1)
                Player.callDeath()

    def setMP(self, newMP):
        self.__mp = newMP
        if isinstance(self, Player) and self.getMP() > self.getMaxMP():
            self.__mp = self.getMaxMP()


class Player(Character):

    # Constructor
    def __init__(self, name, hp, mp, prof, xMap=18, yMap=13, location=0):
        super().__init__(name, hp, mp, prof)
        self.__xMap = xMap
        self.__yMap = yMap
        self.__location = location
        self.__maxHP = self.getHP()
        self.__maxMP = self.getMP()
        self.__inv = []
        self.armor = []
        self.dodgeChance = 0
        self.didBattle = False
        self.__didAction = False
        self.__stopCombat = False
        self.__keyCount = 0
        self.__buffs = {}
        self.__level = 1
        self.__exp = 0
        self.__expRequired = 100
        Character.totalChars += 1

    def __str__(self):
        result = ""
        result += "{} the {}\n".format(self.__name, self.__profession)
        result += "HP: {}\n".format(str(self.__hp))
        result += "MP: {}\n".format(str(self.__mp))
        return result

    @staticmethod
    def callDeath():
        from os import system
        from pygame import mixer
        mixer.music.fadeout(5000)
        sleep(2)
        system('cls')
        intro.slow_type(["\n\n\tThanks for playing!",
                         "\n", "\tPlay again?:"])
        ans = input("\t >> ")
        if "y" in ans:
            from TextRPG import main
            main()
        else:
            quit()

    # Getters
    def getLevel(self):
        return self.__level

    def getMaxHP(self):
        return self.__maxHP

    def getMaxMP(self):
        return self.__maxMP

    def getX(self):
        return self.__xMap

    def getY(self):
        return self.__yMap

    def getLoc(self):
        return self.__location

    def getInv(self):
        return self.__inv

    def getKeys(self):
        return self.__keyCount

    def getExp(self):
        return self.__exp

    def getExpReq(self):
        return self.__expRequired

    def getArmor(self):
        return self.armor[0].getDam()

    def actionCheck(self):
        return self.__didAction

    def isCombatStopped(self):
        return self.__stopCombat

    # Setters
    def setMaxHP(self, newMax):
        self.__maxHP = newMax

    def didAction(self, action):
        self.__didAction = action

    def stopCombat(self):
        self.__stopCombat = True

    def resetCombat(self):
        self.__stopCombat = False

    def addKey(self):
        self.__keyCount += 1

    def removeKey(self):
        self.__keyCount -= 1

    def setLoc(self, newLoc):
        self.__location = newLoc

    def setX(self, newX):
        self.__xMap = newX

    def setY(self, newY):
        self.__yMap = newY

    def addItem(self, item):
        if "Potion" in item.getName():
            self.__inv.append(item)
        else:
            self.__inv.insert(1, item)

    def addBuff(self, buff, length):
        self.__buffs[buff] = length

    def getBuffs(self):
        return self.__buffs

    def clearBuffs(self):
        self.__buffs.clear()

    def removeBuff(self, buff):
        del self.__buffs[buff]

    def buffDown(self):
        if len(self.__buffs) > 0:
            for buffLength in self.__buffs.values():
                buffLength -= 1

            for i in self.__buffs:
                if self.__buffs[i] == 0:
                    self.__buffs.pop(i)
                    if i == "Shadow":
                        if self.getLevel() == 5:
                            self.dodgeChance = 30
                        else:
                            self.dodgeChance = 15

    def levelUp(self):
        self.__level += 1
        intro.slow_type(["You leveled up! You are now Level {}!".format(self.getLevel()),
                         "\nYou regained half your missing HP & MP!"])
        if self.getLevel() == 5:
            intro.slow_type(["You've reached the maximum level of 5, your passive trait has doubled."])
            self.dodgeChance = 30
        self.__maxHP += 20
        self.__maxMP += 10
        self.setHP(self.getHP() + ((self.__maxHP - self.getHP()) // 2))
        self.setMP(self.getMP() + ((self.__maxMP - self.getMP()) // 2))
        sleep(.5)

    def addExp(self, target):
        if self.getLevel() < 5:
            intro.slow_type(["You gained {} experience.".format(target.expValue)])
            sleep(.5)
            self.__exp += target.expValue
            if self.__exp >= self.__expRequired:
                self.levelUp()
                overflow = self.__exp - self.__expRequired
                self.__expRequired += 50
                self.__exp = overflow

    def castSpell(self, E):
        importName, importDesc = getSpellData("spellData.txt")
        spellNames = []
        spellDescs = []

        if self.getProf() == "Warrior":
            spellNames = importName[0:4]
            spellDescs = importDesc[0:4]
        elif self.getProf() == "Mage":
            if self.getLevel() > 1:
                spellNames = importName[4:7]
                spellDescs = importDesc[4:7]
            spellNames.insert(0, importName[0])
            spellDescs.insert(0, importDesc[0])
        else:
            if self.getLevel() > 1:
                spellNames = importName[7:]
                spellDescs = importDesc[7:]
            spellNames.insert(0, importName[0])
            spellDescs.insert(0, importDesc[0])

        spellNames = spellNames[:self.getLevel()]
        spellDescs = spellDescs[:self.getLevel()]

        print("\nSpells:")
        for spell in range(len(spellNames)):
            print("\t{}) {}   {}".format(spell + 1, spellNames[spell], spellDescs[spell]))
        print("\n0) Return to previous menu")

        # Practicing some list comprehension
        # This little guy cut down on a TON of lines!
        cond = [" the" if E.getProf() == "Monster" else ""]
        name = [E.getName().lower() if E.getProf() == "Monster" else E.getName().title()]

        finished = False
        while not finished:
            try:
                # Flush input
                while kbhit():
                    getch()

                ans = getch().decode()
                ans = int(ans)

                # ans = int(input(">> "))

                while ans > len(spellNames):
                    ans = int(getch().decode())

                if ans == 0:
                    return False
                elif ans == 1:
                    if self.getMP() >= 10:
                        healAmount = randint(10, 20)
                        self.setMP(self.getMP() - 10)
                        intro.slow_type(["\n\tA restorative mist begins to rise around you...",
                                         "\n\tYou cast a healing spell, restoring {} health.".format(str(healAmount))])
                        self.setHP(self.getHP() + healAmount)
                        sleep(.5)
                        self.didAction(True)
                    else:
                        print("Not enough mana!")
                        sleep(1)
                elif ans == 2:
                    if self.getMP() >= 15:
                        damage = randint(20, 30)
                        self.setMP(self.getMP() - 15)

                        if self.getProf() == "Warrior":
                            intro.slow_type(["\n\tYou wind up an attack, preparing to cut deep into your enemy...",
                                             "\n\tYou strike{} {} with expert precision, doing {} damage!"
                                             .format(cond[0], name[0], str(damage))])
                            E.setHP(E.getHP() - damage)
                            self.addBuff("Bleed", 2)

                        elif self.getProf() == "Mage":
                            intro.slow_type(["\n\tFire swirls amongst your fingertips as you begin to concentrate...",
                                             "\n\tYou cast a fireball at{} {}, doing {} damage!"
                                             .format(cond[0], name[0], str(damage))])
                            E.setHP(E.getHP() - damage)
                            self.addBuff("Burn", 2)

                        elif self.getProf() == "Thief":
                            intro.slow_type(["\n\tYou begin to sink into the shadows surrounding you...",
                                             "\n\tYou appear behind{} {} and strike, doing {} damage!"
                                             .format(cond[0], name[0], round(self.getDamage() * 1.5))])
                            E.setHP(E.getHP() - round(self.getDamage() * 1.5))

                        sleep(.5)
                        self.didAction(True)
                    else:
                        print("Not enough mana!")
                        sleep(1)
                elif ans == 3:
                    if self.getMP() >= 20:
                        self.setMP(self.getMP() - 20)

                        if self.getProf() == "Warrior":
                            intro.slow_type(["\n\tReflecting on your years of battle, your posture stiffens.",
                                             "\n\tYou brace yourself for incoming attacks."])
                            self.addBuff("Brace", 3)

                        elif self.getProf() == "Mage":
                            damage = randint(15, 25)
                            intro.slow_type(["\n\tThe cold vapor in the air around you begins to crystallize...",
                                             "\n\tIce materializes around you, barraging{} {} for {} damage."
                                            .format(cond[0], name[0], damage)])
                            E.setHP(E.getHP() - damage)
                            self.addBuff("Freeze", 2)

                        elif self.getProf() == "Thief":
                            intro.slow_type(["\n\tThe lines between your body and the light begin to fade...",
                                             "\n\tYou become seemingly invisible amongst the darkness."])
                            self.addBuff("Shadow", 3)

                        sleep(.5)
                        self.didAction(True)
                    else:
                        print("Not enough mana!")
                        sleep(1)
                elif ans == 4:
                    if self.getMP() >= 25:
                        self.setMP(self.getMP() - 25)

                        if self.getProf() == "Warrior":
                            intro.slow_type(["\n\tYour experience tells you that{} {} will soon expose itself.".format(cond[0], name[0]),
                                             "\n\tYou assume a defensive stance, preparing to counterattack."])
                            self.addBuff("Counter", 10)

                        elif self.getProf() == "Mage":
                            damage = randint(15, 25)
                            intro.slow_type(["\n\tYou conjure a slowly fading protective bubble around yourself...",
                                             "\n\tIncoming damage is reduced for the next three turns."
                                            .format(cond[0], name[0], damage)])
                            E.setHP(E.getHP() - damage)
                            self.addBuff("Bubble", 4)

                        elif self.getProf() == "Thief":
                            intro.slow_type(["\n\tYou coat your equipped weapon with a deadly poison...",
                                             "\n\tYour attacks become even more efficient and deadly."])
                            self.addBuff("Poison", 3)

                        sleep(.5)
                        self.didAction(True)
                    else:
                        print("Not enough mana!")
                        sleep(1)

                finished = True
            except ValueError:
                print("Invalid input.")

    def checkInv(self):
        print("\n\nSelect a weapon to use/equip:\n\n\tCurrently equipped weapon:")
        print("\n\t\t" + str(self.__inv[0]) + "\n")
        if len(self.armor) > 0:
            print("\tCurrently equipped shield:")
            print("\n\t\t" + str(self.armor[0]) + "\n")
        for i in range(len(self.__inv[1:])):
            print("\t{}) {}".format(i + 1, self.__inv[i + 1]))
        print("\nD: Discard Item\nU: Unequip Offhand\n0) Return to previous menu")

        finished = False
        while not finished:
            try:
                # ans = input("\t >> ")
                ans = getch().decode()

                if ans in "du0123456789":
                    if ans == "0":
                        break

                    elif ans == "d":
                        intro.slow_type(["\t\tPress number of the item to discard."])
                        print("\t  (This cannot be undone, 0 to return to previous menu.)")
                        tempAns = getch().decode()
                        if int(tempAns) != 0 and int(tempAns) <= len(self.__inv):
                            self.__inv.pop(int(tempAns))

                    elif ans == "u":
                        if len(self.__inv) <= 8:
                            self.addItem(self.armor.pop(0))

                    elif "Potion" in self.__inv[int(ans)].getName():
                        self.__inv[int(ans)].usePotion(self)
                        temp = ["HP" if "Health" in self.__inv[int(ans)].getName() else "MP"]
                        intro.slow_type(["\tYou drank a {}, restoring {} {}.".format(
                            self.__inv[int(ans)].getName().lower(), self.__inv[int(ans)].getPower(), temp[0])])
                        self.__inv.pop(int(ans))
                        sleep(.5)
                        self.didAction(True)

                    elif "Great" in self.__inv[int(ans)].getName() and len(self.armor) > 0:
                        if len(self.__inv) <= 8:
                            # Add the armor and current weapon at the beginning of the list to the end,
                            self.__inv.append(self.armor.pop(0))
                            self.__inv.append(self.__inv.pop(0))
                            # Add the chosen weapon to the front (-1 because [0] moved right, shifting list left)
                            self.__inv.insert(0, self.__inv.pop(int(ans) - 1))
                        else:
                            intro.slow_type(["Too many items in inventory!"])
                            sleep(1)

                    elif "Shield" in self.__inv[int(ans)].getName():
                        if "Great" in self.__inv[0].getName():
                            intro.slow_type(["Please equip a 1 handed weapon first."])
                            sleep(1)
                        else:
                            self.addArmor(self.__inv[int(ans)])
                            self.__inv.pop(int(ans))

                    else:
                        self.__inv.insert(0, self.__inv.pop(int(ans)))

                    self.didAction(True)

                    finished = True
            except ValueError:
                print("Invalid input.")

    def addArmor(self, armor):
        if len(self.armor) == 0:
            self.armor.append(armor)
        else:
            self.__inv.insert(1, self.__inv.pop(self.armor[0]))
            self.armor.append(armor)

    def getDamage(self):
        if self.getProf() == "Warrior" and self.getLevel() < 5:
            return self.__inv[0].getDam() + 5
        elif self.getProf() == "Warrior" and self.getLevel() == 5:
            return self.__inv[0].getDam() + 10
        else:
            return self.__inv[0].getDam()

    def attack(self, target):
        if isinstance(self.__inv[0], itemGen.Weapon):
            cond = [" the" if target.getProf() == "Monster" else ""]
            name = [target.getName().lower() if target.getProf() == "Monster" else target.getName()]

            intro.slow_type(["\n\tYou attack{} {} for {} damage!".format(cond[0], name[0], self.getDamage())])
            target.setHP(target.getHP() - self.getDamage())
            self.__inv[0].setDur(self.__inv[0].getDur() - 1)
            self.didAction(True)
            sleep(.5)
        else:
            intro.slow_type(["You try to attack, but don't have a weapon equipped!"])
            sleep(1)

    def checkBuff(self, E):
        buff = ""
        damage = 0

        cond = ["The " if E.getProf() == "Monster" else ""]
        name = [E.getName().lower() if E.getProf() == "Monster" else E.getName()]

        if "Bleed" in self.getBuffs():
            damage = randint(4, 12)
            buff += "\n\t{}{} bleeds for an additional {} damage.".format(cond[0], name[0], damage)
        if "Burn" in self.getBuffs():
            damage = randint(6, 12)
            buff += "\n\t{}{} burns for an additional {} damage.".format(cond[0], name[0], damage)
        if "Poison" in self.getBuffs():
            damage = randint(10, 15)
            buff += "\n\t{}{} suffers an additional {} poison damage.".format(cond[0], name[0], damage)
        if "Shadow" in self.getBuffs():
                if self.dodgeChance == 15 or self.dodgeChance == 30:
                    self.dodgeChance += 35
                buff += "\n\tYour chance to dodge is increased."
        if "Bubble" in self.getBuffs():
            if self.getBuffs()["Bubble"] == 4:
                buff += "\n\tYour protective bubble is at full strength"
            elif 2 <= self.getBuffs()["Bubble"] >= 3:
                buff += "\n\tYour protective bubble fades slightly."
            elif self.getBuffs()["Bubble"] == 1:
                buff += "\n\tYour protective bubble fades completely."
        if "Brace" in self.getBuffs():
            if self.getBuffs()["Brace"] > 1:
                buff += "\n\tYour defenses are increased."
            elif self.getBuffs()["Brace"] == 1:
                buff += "\n\tYour defense boost fades."

        if buff:
            intro.slow_type([buff])

        if damage:
            E.setHP(E.getHP() - damage)


class Enemy(Character):
    # Constructor
    def __init__(self, name, hp, mp, exp, prof="Monster"):
        super().__init__(name, hp, mp, prof)
        self.__buffCount = 0
        self.__maxHP = self.getHP()
        self.expValue = exp
        Character.totalChars += 1

    def attack(self, target):
        damage = self.getDamage()

        if "Brace" in target.getBuffs() and "Counter" not in target.getBuffs():
            damage = round(damage * .8)

        if "Bubble" in target.getBuffs():
            if target.getBuffs()["Bubble"] == 3:
                damage -= 15
            elif target.getBuffs()["Bubble"] == 2:
                damage -= 10
            elif target.getBuffs()["Bubble"] == 1:
                damage -= 5

        # If the player is a thief, check to see if they dodge, then calculate damage
        if target.getProf() == "Thief" and randint(1, 100) <= target.dodgeChance:
            intro.slow_type(["\n\tYou dodged the incoming attack from the {}!".format(self.getName().lower())])
        else:
            # If the player has a shield equipped, reduce damage taken and damage shield
            if "Counter" in target.getBuffs():
                intro.slow_type(["\n\tThe {} attacks you for {} damage!".format(self.getName().lower(), damage),
                                 "\n\tYou counter the attack, and reflect the {} damage back!".format(damage)])
                self.setHP(self.getHP() - damage)
                target.removeBuff("Counter")
            elif len(target.armor) > 0:
                damage -= (target.getArmor() // 2)
                intro.slow_type(["\n\tThe {} attacks you for {} damage!".format(self.getName().lower(), damage)])
                if damage < 0:
                    damage = 0
                target.setHP(target.getHP() - damage)
                target.armor[0].setDur(target.armor[0].getDur() - 1)
            else:
                intro.slow_type(["\n\tThe {} attacks you for {} damage!".format(self.getName().lower(), damage)])
                target.setHP(target.getHP() - damage)

        if "Brace" in target.getBuffs() and "Counter" not in target.getBuffs():
            reflect = round(damage * .2)
            intro.slow_type(["{} damage is reflected back to the {}!".format(reflect, self.getName().lower())])
            self.setHP(self.getHP() - reflect)

    def maxHP(self):
        return self.__maxHP

    def getDamage(self,):
        if self.getName() == "Zombie":
            return randint(5, 15)
        elif self.getName() == "Skeleton":
            return randint(1, 10)
        else:
            return randint(15, 25)

    def selfHeal(self):
        if self.getName() == "Skeleton":
            healAmount = randint(5, 10)
            intro.slow_type(["\n\tThe skeleton reaches down and grabs a bone off the floor...",
                             "\n\tAttaching a piece of itself back on, it regains {} health!".format(str(healAmount))])
            self.setHP(self.getHP() + healAmount)
        elif self.getName() == "Zombie":
            healAmount = randint(10, 15)
            intro.slow_type(["\n\tThe zombie grabs a NeuroShake\u2122 and takes a huge slurp...",
                             "\n\tEnergized with fresh brain matter, it regains {} health!".format(str(healAmount))])
            self.setHP(self.getHP() + healAmount)
        elif self.getName() == "Ogre":
            healAmount = randint(15, 20)
            intro.slow_type(["\n\tThe ogre pulls out a vial of human blood from it's belt loop...",
                             "\n\tGuzzling down the ichor, it regains {} health!".format(str(healAmount))])
            self.setHP(self.getHP() + healAmount)


class Boss(Character):
    # Constructor
    def __init__(self, name, hp, mp, exp, prof):
        super().__init__(name, hp, mp, prof)
        self.expValue = exp
        self.__buffCount = 0
        Character.totalChars += 1

    def attack(self, target, damage):
        moveChoice = randint(1, 2)

        if self.__buffCount > 0:
            damage += 5
        elif self.__buffCount < 0:
            self.__buffCount = 0

        if "Brace" in target.getBuffs() and "Counter" not in target.getBuffs():
            damage = round(damage * .8)

        if "Bubble" in target.getBuffs():
            if target.getBuffs()["Bubble"] == 3:
                damage -= 15
            elif target.getBuffs()["Bubble"] == 2:
                damage -= 10
            elif target.getBuffs()["Bubble"] == 1:
                damage -= 5

        if moveChoice == 1 and self.getMP() >= 10:
            self.castSpell(target)
        else:
            if target.getProf() == "Thief" and randint(1, 100) <= target.dodgeChance:
                intro.slow_type(["\n\tYou dodged the incoming attack from {}!".format(self.getName())])
            else:
                if "Counter" in target.getBuffs():
                    intro.slow_type(["\n\t{} attacks you for {} damage!".format(self.getName(), damage),
                                     "\n\tYou counter the attack, and reflect the {} damage back!".format(damage)])
                    self.setHP(self.getHP() - damage)
                    target.removeBuff("Counter")
                elif len(target.armor) > 0:
                    damage -= (target.getArmor() // 2)
                    intro.slow_type(["\n\t{} attacks you for {} damage!".format(self.getName(), damage)])
                    if damage < 0:
                        damage = 0
                    target.setHP(target.getHP() - damage)
                    target.armor[0].setDur(target.armor[0].getDur() - 1)
                else:
                    intro.slow_type(["\n\t{} attacks you for {} damage!".format(self.getName(), damage)])
                    target.setHP(target.getHP() - damage)

                if "Brace" in target.getBuffs() and "Counter" not in target.getBuffs():
                    reflect = round(damage * .2)
                    intro.slow_type(["{} damage is reflected back to {}!".format(reflect, self.getName())])
                    self.setHP(self.getHP() - reflect)

            self.__buffCount -= 1

        sleep(.5)

    def getDamage(self):
        if self.getProf() == "Guardian":
            return randint(25, 40)
        elif self.getProf() == "Soulkeeper":
            return randint(30, 45)

    def castSpell(self, E):
        from random import choice

        if self.getProf() == "Guardian":
            spellList = ["holy bolt",
                         "empower",
                         "ethereal blade"]

        else:
            spellList = ["demonic spear",
                         "leech",
                         "dark vortex"]

        if self.getMP() >= 20:
            moveChoice = randint(1, 15)
        elif self.getMP() >= 15:
            moveChoice = randint(1, 10)
        elif self.getMP() >= 10:
            moveChoice = randint(1, 5)
        else:
            moveChoice = 0

        hit = choice(["hitting", "grazing", "clipping", "injuring"])
        side = choice(["left", "right"])
        limb = choice(["arm", "leg"])

        if moveChoice <= 5:
            if self.getProf() == "Guardian":
                damage = randint(30, 40)
                intro.slow_type(
                    ["\n\t{} casts a {} at you, {} your {} {}.".format(self.getName(), spellList[0], hit, side, limb),
                     "\n\tYou take {} damage from the spell.".format(damage)])
                E.setHP(E.getHP() - damage)
            else:
                damage = randint(35, 45)
                intro.slow_type(
                    ["\n\t{} summons a {} and hurls it at you, {} your {} {}.".format(self.getName(), spellList[0],
                                                                                      hit, side, limb),
                     "\n\tYou take {} damage from the pike.".format(damage)])
                E.setHP(E.getHP() - damage)
            sleep(.5)
            self.setMP(self.getMP() - 15)
        elif 5 < moveChoice <= 10:
            if self.getProf() == "Guardian":
                intro.slow_type([
                    "\n\t{} casts {} on his weapon, increasing the damage of it's next attack.".format(self.getName(),
                                                                                                       spellList[1])])
                self.__buffCount += 1
            else:
                damage = randint(15, 25)
                intro.slow_type(
                    ["\n\n\t{} casts {} on you, siphoning {} health from you.".format(self.getName(), spellList[1],
                                                                                      damage)])
                E.setHP(E.getHP() - damage)
                self.setHP(self.getHP() + damage)
            sleep(.5)
            self.setMP(self.getMP() - 15)
        elif 10 < moveChoice <= 15:
            if self.getProf() == "Guardian":
                damage = randint(35, 45)
                intro.slow_type(
                    ["\n\n\t{} summons an {} from the void, it pierces your {} {} with ease.".format(
                        self.getName(), spellList[2], side, limb),
                        "\n\tYou take {} damage from the wound.".format(damage)])
                E.setHP(E.getHP() - damage)
            else:
                damage = randint(40, 50)
                intro.slow_type(
                    ["\n\n\t{} summons a {} around you, you can feel your mind begin to wither.".format(
                        self.getName(), spellList[2]),
                        "\n\tYou take {} damage from the torment.".format(damage)])
                E.setHP(E.getHP() - damage)
            sleep(.5)
            self.setMP(self.getMP() - 20)


def make_player():
    from os import system

    defaultHP = 150
    defaultMP = 50

    finished = False

    charName = ""
    charProf = ""

    while not finished:
        print("\n -== Enter your character's name: ==-")
        while charName == "":
            charName = input("\t >> ").title()
        print("\n -== Available Professions: ==-\n")
        for i in profList[:3]:
            print("\t" + i)
            if i == "Warrior":
                print("\t >  With over a dozen battles conquered, warriors deal additional damage with attacks.")
                print("\t\t  (Gain an additional 5 base damage on top of weapon.)")
            elif i == "Mage":
                print("\t >  After many years of study, magi regenerate a small amount of mana during combat.")
                print("\t\t  (Regenerate 5 MP at the beginning of every turn.)")
            elif i == "Thief":
                print("\t >  Light on their feet, thieves have a small chance to avoid damage entirely.")
                print("\t\t  (Gain a 15% chance to dodge all attack damage.)")
        print("\n -== Choose your profession: ==-")
        while charProf == "" or charProf not in profList[:3]:
            charProf = input("\t >> ").title()

        intro.slow_type(["\n Thank you, {} the {}.".format(charName, charProf)])
        intro.slow_type(["\n\n Continue with this setup? (yes/no)"])
        playerInput = input(" >> ")
        if "y" in playerInput.lower():
            finished = True
        else:
            system('cls')
            charName = ""
            charProf = ""

    return Player(charName, defaultHP, defaultMP, charProf)


def getSpellData(fileName, mode="r"):
    # open the file
    try:
        descriptions = []
        theFile = open(fileName, mode)
        # take first line split values on the ','
        names = theFile.readline().strip().split(',')
        # take rest of lines and make list with each description as a list item (trailing with '\n')
        badDesc = theFile.readlines()
        # remove the '\n'
        for line in badDesc:
            descriptions.append(line.strip())
        # close the file
        theFile.close()
        return names, descriptions
    except FileNotFoundError:
        print("File not found. Program closing.")
        quit()
