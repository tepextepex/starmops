from classes import Char
from init_skills import *


def spawn_dummy_enemies():
    spider = Char("Lord Spader", "spider",
                 "This is the boss. It is obvious",
                 7, 2, 10, 5)
    spider.learn(melee_attack)

    mouse_1 = Char("Brother Mouse", "mouse",
                 "One of the Lord Spader's minions",
                 3, 4, 5, 10)
    mouse_1.learn(melee_attack)

    mouse_2 = Char("Sister Mouse", "mouse",
                 "One of the Lord Spader's minions",
                 3, 4, 5, 10)
    mouse_2.learn(melee_attack)

    bat = Char("Pet Bat", "bat",
                 "The strangest pet I've ever seen",
                 7, 8, 3, 5)
    bat.learn(ranged_attack)

    enemies = [mouse_1, spider, mouse_2, bat]

    for e, i in zip(enemies, (1, 2, 3, 5)):
        e.slot_no = i

    return enemies
