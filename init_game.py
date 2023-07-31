from init_skills import *
from classes import Char, Weapon, Armor


def init_game():
    Hodor = Char("Hodor", "alien_green",
                 "Hodor is the tank. THE tank. He is a tough guy who defends his dudes",
                 7, 3, 10, 5)
    Hodor.learn(melee_attack, ranged_attack, hold)

    Jeb = Char("Jebediah", "alien_blue",
                "Jebediah is a jebedi knight. Wily and agile, he prefers melee combat using lasersabers",
               3, 10, 7, 5)
    Jeb.learn(melee_attack, ranged_attack, swing, stun)

    Scar = Char("Scarface", "alien_pink",
                "Scarface is always smiling, but don't fall for this. He is fierce and adores to dismember his opponents",
                10, 5, 7, 3)
    Scar.learn(melee_attack, ranged_attack, rage)

    East = Char("Eastwood", "alien_yellow",
                  "A gunslinger without a name. Everybody calls him Eastwood but we have no idea why",
                3, 10, 5, 7)
    East.learn(melee_attack, ranged_attack, piercing_shot)

    Pope = Char("Pope", "alien_beige",
                 "Pope is a master spellcaster. He has an essential ability to heal his allies",
                3, 5, 7, 10)
    Pope.learn(melee_attack, ranged_attack, heal, revive)

    aliens = (Hodor, Jeb, Scar, East, Pope)

    dummy_gun = Weapon("ranged", "Ray gun", "blaster", 10)
    dummy_sword = Weapon("melee", "Rusty sword", "sword_bronze", 15)
    dummy_saw = Weapon("melee", "Rusty chainsaw", "chainsaw", 15)
    dummy_saber = Weapon("melee", "Rusty lasersaber", "lasersaber", 15)
    dummy_shield = Armor("dummy", "Wooden shield", "shield_bronze", 5)
    dummy_umbrella = Armor("dummy", "Umbrella", "umbrella_open", 2)

    inventory = [dummy_gun, dummy_sword, dummy_saber, dummy_saw, dummy_shield, dummy_umbrella]

    Hodor.equip_weapon(dummy_sword)
    Jeb.equip_weapon(dummy_saber)
    Scar.equip_weapon(dummy_saw)
    East.equip_weapon(dummy_gun)

    return aliens, inventory
