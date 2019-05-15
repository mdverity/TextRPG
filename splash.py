from os import system
from msvcrt import kbhit, getch


def splashScreen():
    system('cls')

    splash = """    
    
    
                       _____                                __
                      |  ___|                              / _|
         __/  \__     | |__ ___  ___ __ _ _ __   ___      | |_ _ __ ___  _ __ ___
          _\/\/_      |  __/ __|/ __/ _` | '_ \ / _ \     |  _| '__/ _ \| '_ ` _ \\
        \_\_\/_/_/    | |__\__ \ (_| (_| | |_) |  __/     | | | | | (_) | | | | | |
        / /_/\_\ \    \____/___/\___\__,_| .__/ \___|     |_| |_|  \___/|_| |_| |_|
         __/\/\__                        | |
           \  /                          |_|
                                                                                  \__  __/
                         _   _               _____ _            _       _         /_/  \_\ 
  Press                 | | | |             |  __ \ |          (_)     | |         _\/\/_  
                        | |_| |__   ___     | |  \/ | __ _  ___ _  __ _| |    __/\_\_\/_/_/\__
     E N T E R          | __| '_ \ / _ \    | | __| |/ _` |/ __| |/ _` | |      \/ /_/\_\ \/
                        | |_| | | |  __/    | |_\ \ | (_| | (__| | (_| | |        __/\/\__ 
         to continue...  \__|_| |_|\___|     \____/_|\__,_|\___|_|\__,_|_|        \_\  /_/ 
                                                                                  /      \\
             
              /\\                 _____       _                            _
         __   \/   __           /  __ \     | |                          | |
         \_\_\/\/_/_/           | /  \/ __ _| |_ __ _  ___ ___  _ __ ___ | |__  ___
           _\_\/_/_             | |    / _` | __/ _` |/ __/ _ \| '_ ` _ \| '_ \/ __|
          __/_/\_\__            | \__/\ (_| | || (_| | (_| (_) | | | | | | |_) \__ \\
         /_/ /\/\ \_\            \____/\__,_|\__\__,_|\___\___/|_| |_| |_|_.__/|___/
              /\                  
              \/
                                                        """

    print(splash)

    input()


def startMenu():
    system('cls')
    menu = """\n\n\n\n\n\n\n\n
    \n\t\t\t\t\t 1 - New Game
    \n\t\t\t\t\t 2 - Load Game
    \n\t\t\t\t\t 3 - Music: {}
    \n\t\t\t\t\t 4 - Exit
    \n\n\n\t\t\t\t        Choose  1 - 4"""

    return menu


def menuInput():
    ans = ""

    while ans not in [1, 2, 3, 4]:
        try:
            while kbhit():
                getch()

            # ans = int(input())
            ans = int(getch().decode())
            if ans > 4:
                print("\n\t\t\t\t        Invalid input.")
        except ValueError or TypeError:
            print("\n\t\t\t\t        Invalid input.")

    return ans
