# Escape from the Glacial Catacombs - A Python RPG

An ASCII dungeon-crawler written in Python, based entirely in the command prompt.

The basic gameplay loop is as follows:
>Choose a name and class for your character, and explore a variety of caves through the use of portals.
>
>Inside these caves are monsters that will randomly appear (think Pokémon-style battles).
>
>Defeating these monsters provides you with XP.
>
>As you progress through some caves, you will encounter chests guarded by mini-bosses, these contain a key.
>
>Obtain 2 keys, and you may progress to the final boss via a secret door located in the main room.
>
>Become powerful enough to defeat him through the use of items, spells, and stats acquired on your journey.  


This was a final project for my CSI111 class, and allowed me to practice a variety of introductory concepts, including but not limited to:
* Data structure navigation
* List comprehensions
* Saving/Loading Objects as files
* Cleaning input buffer
* Parsing data from files
* Basic animation and game design

Highlights of some game features:
* Level system with both player and enemy scaling
* Random item generation with options for more specific rolls
* Varied spells for each class, each with unique passive bonus
* Transition screen between adventuring and battles
* Two-handed weapons or 1-handed/shield combos


## Getting Started

Check [here](https://github.com/mdverity/TextRPG/releases/tag/v1.0.0) for the most recent executable. Download the `.zip`, extract it, and run `TextRPG.exe`.  
Continue reading for instructions on running the scripts locally and additional documentation.


### Prerequisites

This project only utilizes one external Python library:

```
Pygame
```


### Installing

This set of scripts utilizes Pygame's Mixer to load and play music files.

To install Pygame, use pip to install it via CMD/Terminal:

```
pip install pygame
```

Check Pygame's installation [documentation](https://www.pygame.org/wiki/GettingStarted) for additional assitance if necessary.


## To-Do:

* Dual wielding of some sort, maybe:
  * totalDamage = weaponDamageOne + (weaponDamageTwo / 2)
  * Reduced durability for both weapons
* Increased monster variety
* Improved transition performance
* Add additional comments


## Authors

* **Matt Verity** - [mdverity](https://github.com/mdverity)
* **Luc Poirier**


## Acknowledgments

All credit for music goes to [**lespaulcustom311**](https://www.youtube.com/user/lespaulcustom311).  
Thank you for allowing me to use your awesome content.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.