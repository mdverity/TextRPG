from os import system


def menu():
    system("mode con cols=95 lines=30")
    # system("echo [4mUnderlined[0m Word")

    part1 = ["                     \u2502                \u2502             \u2502" + "               \u2502",
             "\n                     \u2502                \u2502 Help Screen \u2502" + "               \u2502",
             "\n  Per Level:         \u2502                " + "\u2514" + "\u2500" * 13 + "\u2518" + "               \u2502  Combat:",
             "\n                     \u2502                                              \u2502",
             "\n   +10 Maximum HP    \u2502                                              \u2502      - Is turn-based.",
             "\n                     \u2502                                              \u2502",
             "\n    +5 Maximum MP    \u2502                                              \u2502      - You attack first.",
             "\n                     \u2502                                              \u2502",
             "\n    +1 Additional    \u2502                                              \u2502      - Buffs don't last",
             "\n            Spell    \u2502                Your Objective:               \u2502          between fights",
             "\n                     \u2502                                              \u2502",
             "\n" + "\u2500" * 21 + "\u2518         You must collect 2 keys from         \u2514" + "\u2500" * 26,
             "\n                                within the caves (Portals).", "",
             "\n\n                              The keys are held by the mighty",
             "\n                            "]

    part2 = ["\n\n                         Two keys allows you to progress further...",
             "                                     But to where...?", "\n\n\n",
             "                                 Press ENTER to return."]

    for i in part1:
        print(i, end="")

    system("echo|set /p=[4mGuardians[0m, found at the [4mBoss Chests[0m.")

    for i in part2:
        print(i)


if __name__ == '__main__':
    menu()
