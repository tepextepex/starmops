from pgzero.actor import Actor
# from pgzero.game import screen  # game won't start with this import line
from pygame import Rect
from hero_skills import *
from dummy_enemies import *

from classes import Char, Weapon, Armor
from gui import MainMenu, BattleScreen
from config import *

MODE = "menu"
main_menu = MainMenu(WIDTH, HEIGHT)
battle_screen = None

background = Actor("purple_space")

quit_btn = Actor("arrow_red")
quit_btn.bottomleft = 0 + PADDING, HEIGHT

next_btn = Actor("arrow_green")
next_btn.bottomright = WIDTH - PADDING, HEIGHT

battle_btn = Actor("arrow_green")
battle_btn.bottomright = WIDTH - PADDING, HEIGHT

green = Char("Hodor", "alien_green",
             "Hodor is the tank. THE tank. He is a tough guy who defends his dudes",
             7, 3, 10, 5)
green.learn(melee_attack, hold)

blue = Char("Jebediah", "alien_blue",
            "Jebediah is a jebedi knight. Wily and agile, he prefers melee combat using lasersabers",
            3, 10, 7, 5)
blue.learn(melee_attack, ranged_attack)

pink = Char("Scarface", "alien_pink",
            "Scarface is always smiling, but don't fall for this. He is fierce and adores to dismember his opponents",
            10, 5, 7, 3)
pink.learn(melee_attack)

yellow = Char("Eastwood", "alien_yellow",
              "A gunslinger without a name. Everybody calls him Eastwood but we have no idea why",
              3, 10, 5, 7)
yellow.learn(ranged_attack)

beige = Char("Pope", "alien_beige",
             "Pope is a master spellcaster. He has an essential ability to heal his allies",
             3, 5, 7, 10)
beige.learn(heal, ranged_attack)

aliens = (green, blue, pink, yellow, beige)

party = []
enemies = []

dummy_gun = Weapon("ranged", "Ray gun", "raygun", 10)
dummy_sword = Weapon("melee", "Rusty sword", "sword_bronze", 15)
dummy_shield = Armor("dummy", "Wooden shield", "shield_bronze", 5)
dummy_umbrella = Armor("dummy", "Umbrella", "umbrella_open", 2)

inv = [dummy_gun, dummy_sword, dummy_shield, dummy_umbrella]

active_skill = 1

desc_text = "Select your party. You can choose three members"


def draw():
    global active_skill
    global hero_panel, enemy_panel

    screen.clear()
    background.draw()

    if MODE == "menu":
        main_menu.render()

    elif MODE == "choice":
        for i, a in enumerate(aliens):
            x = 95 + 100 * i
            y = 100
            screen.draw.text(a.name, midtop=(x + 32, y + 100))
            if a.image_base == "alien_yellow":
                y += 10
            a.actor.topleft = x, y
            a.actor.draw()

        draw_description()
        draw_buttons()

    elif MODE == "inv":
        P = PADDING
        c = (255, 255, 255, 128)

        # hero panels:
        for i, hero in enumerate(party):
            # print(i, hero)
            w = (WIDTH - P * 4) / 3
            h = HEIGHT / 2 - P
            x = P * (i + 1) + i * w
            y = P
            p_box = Rect((x, y),
                         (w, h))
            screen.draw.rect(p_box, c)
            screen.draw.text(hero.name, midtop=(x + w / 2, y + P))

            y = y + 3 * P
            if hero.image_base == "alien_yellow":
                y += 10
            hero.actor.midtop = (x + w / 2, y)
            # hero.set_stand()
            hero.actor.draw()

            # drawing hero stats:
            y = 2 * P + h / 2
            # column 1
            #screen.draw.text(f"MAX HP {hero.max_hp()}", midtop=(x + w / 4, y + P))
            screen.draw.text(f"STR {hero.str}", midtop=(x + w / 4, y + 4 * P))
            screen.draw.text(f"DEX {hero.dex}", midtop=(x + w / 4, y + 7 * P))
            # column 2
            #screen.draw.text(f"MAX MP {hero.max_mp()}", midtop=(x + 3 * w / 4, y + P))
            screen.draw.text(f"CON {hero.con}", midtop=(x + 3 * w / 4, y + 4 * P))
            screen.draw.text(f"INT {hero.int}", midtop=(x + 3 * w / 4, y + 7 * P))

        # inventory panel:
        x = P
        y = P + HEIGHT / 2
        w = WIDTH - 2 * P
        i_box = Rect((x, y),
                     (w, HEIGHT / 2 - 2 * P))
        screen.draw.rect(i_box, c)
        screen.draw.text("Inventory", midtop=(WIDTH / 2, y + P))

        # items in inventory:
        for i, item in enumerate(inv):
            x = P + i * 70
            item.actor.topleft = (x, y + 4 * P)
            item.actor.draw()
        # buttons:
        battle_btn.draw()

    elif MODE == "battle":
        background.draw()

        battle_screen.render()


def draw_description():
    screen.draw.text(desc_text,
                     midtop=(WIDTH / 2, HEIGHT / 2 + 80),
                     width=500)


def draw_buttons():
    quit_btn.draw()
    if len(party) == 3:
        next_btn.draw()


def on_mouse_down(pos):
    global desc_text
    global party
    global MODE
    global enemies
    global main_menu, battle_screen
    global active_skill

    if MODE == "menu":
        if main_menu.menu_start.collidepoint(pos):
            MODE = "choice"
        if main_menu.menu_load.collidepoint(pos):
            print("Not implemented yet! Sorry")
        if main_menu.menu_credits.collidepoint(pos):
            print(main_menu.game_credits)

    elif MODE == "choice":
        for a in aliens:
            if a.actor.collidepoint(pos):
                if a.state == "stand":
                    a.set_jump()
                    party.append(a)
                    if len(party) > 3:
                        party[0].set_stand()
                        party.pop(0)  # deletes the first chosen character
                    print(party)
                elif a.state == "jump":
                    a.set_stand()
                    party.remove(a)
                    print(party)
                desc_text = f"{a.desc}\nSTR {a.str} / DEX {a.dex} / CON {a.con} / INT {a.int}"

        if next_btn.collidepoint(pos):
            print("Starting game")
            for hero in party:
                hero.set_stand()
            MODE = "inv"

    elif MODE == "inv":
        for hero in party:
            if hero.actor.collidepoint(pos):
                print(hero)
                hero.funny_jump()

        if battle_btn.collidepoint(pos):
            print("Going into battle")
            # assigning slot numbers to the hero party:
            for i, hero in enumerate(party):
                hero.slot_no = i + 1  # + 3
            # creating enemies party:
            enemies = [mouse_1, spider, mouse_2, bat]
            for e, i in zip(enemies, (1, 2, 3, 5)):
                e.slot_no = i
            MODE = "battle"
            active_skill = 1

            everyone = party + enemies
            everyone = sorted(everyone, key=lambda x: x.dex, reverse=True)
            cur_actor = 0  # who makes a turn now

            battle_screen = BattleScreen(screen, PADDING, SKILL_PANEL_HEIGHT, INFO_PANEL_HEIGHT, QUEUE_PANEL_WIDTH,
                                         party, enemies, everyone, active_skill, everyone[cur_actor])

"""
def on_mouse_move(pos):
    global hero_panel, enemy_panel
    if MODE == "battle":
        # TODO: check whose turn is this (heros or enemies)
        for s in hero_panel.slots:
            if s.box.collidepoint(pos):
                s.target = True
                print(s)
        for s in enemy_panel.slots:
            if s.box.collidepoint(pos):
                s.target = True
                print(s)
"""


def on_key_up(key):
    global active_skill
    global battle_screen
    if MODE == "battle":
        num_keys = [f"K_{x}" for x in range(1, 10)]
        if key.name in num_keys:
            key_no = int(key.name.split("_")[1])
            active_skill = key_no
            battle_screen.skill_panel.set_active_skill(key_no)

"""
def update():
    alien.left += 2
    if alien.left > WIDTH:
        alien.right = 0
"""