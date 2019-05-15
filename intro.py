import time


def slow_type(t):
    import sys

    for i in t:
        for l in i:
            sys.stdout.write(l)
            sys.stdout.flush()
            time.sleep(.04)
        time.sleep(.4)
    print("")


def intro1():
    introLines = ["\n You awaken in a cold, dark room...\n", "",
                  " No doors...\n", "",
                  " No windows...\n", ""]

    slow_type(introLines)


def intro2():
    from os import system

    introLines = ["\n As you look up, you notice a faint shimmer in the center and a door on the far side.",
                  "\n\n Touch the center object? (yes/no)"]

    yesLines = ["\n", "",
                " The object begins to hum as your hand approaches it...", "\n",
                "\n", "",
                " As you come into contact with the device, it begins to glow...", "\n",
                "\n", "",
                " ...Portals erupt from the center!", "\n",
                "\n", "", "",
                " They seem to travel to various caves...",
                "\n", " Perhaps you should begin your escape there.",
                "\n", "\n", "", " You grab hold of the shanty training sword and small vial on the ground next to you."
                "\n", "",
                "\n", "\n", " Let us begin our journey, shall we", ".", ".", ".", "?"]

    noLines = ["\n Well, we may as well just take a nap then...",
               "\n Hmm, this pile of bones looks comfortable.",
               "\n I think I'll just make myself at home here...",
               "\n Nice", ".", ".", ".", "cozy", ".", ".", ".", "bones", ".", ".", "."]

    system('cls')

    slow_type(introLines)

    playerInput = input("\n  >> ")

    system('cls')

    if "y" in playerInput.lower():
        slow_type(yesLines)
        time.sleep(2)
    elif "n" in playerInput.lower():
        slow_type(noLines)
        time.sleep(3)
        quit()
