from pgzero.actor import Actor
# from pgzero.game import screen  # game won't start with this import line
from pygame import Rect
from dummy_enemies import *

from classes import Char, Weapon, Armor
from gui import SkillsPanel, InfoPanel, QueuePanel, SlotsPanel, HeroPanel, EnemyPanel

WIDTH = 640
HEIGHT = 480
padding = 10

MODE = "menu"

background = Actor("purple_space")

quit_btn = Actor("arrow_red")
quit_btn.bottomleft = 0 + padding, HEIGHT

next_btn = Actor("arrow_green")
next_btn.bottomright = WIDTH - padding, HEIGHT

battle_btn = Actor("arrow_green")
battle_btn.bottomright = WIDTH - padding, HEIGHT

green = Char("Hodor", "alien_green",
             "Hodor is the tank. THE tank. He is a tough guy who defends his dudes",
             7, 3, 10, 5)
blue = Char("Jebediah", "alien_blue",
            "Jebediah is a jebedi knight. Wily and agile, he prefers melee combat using lasersabers",
            3, 10, 7, 5)
pink = Char("Scarface", "alien_pink",
            "Scarface is always smiling, but don't fall for this. He is fierce and adores to dismember his opponents",
            10, 5, 7, 3)
yellow = Char("Eastwood", "alien_yellow",
              "A gunslinger without a name. Everybody calls him Eastwood but we have no idea why",
              3, 10, 5, 7)
beige = Char("Pope", "alien_beige",
             "Pope is a master spellcaster. He has an essential ability to heal his allies",
             3, 5, 7, 10)

aliens = (green, blue, pink, yellow, beige)

party = []
enemies = []

dummy_gun = Weapon("ranged", "Ray gun", "raygun", 10)
dummy_sword = Weapon("melee", "Rusty sword", "sword_bronze", 15)
dummy_shield = Armor("dummy", "Wooden shield", "shield_bronze", 5)
dummy_umbrella = Armor("dummy", "Umbrella", "umbrella_open", 2)

inv = [dummy_gun, dummy_sword, dummy_shield, dummy_umbrella]

desc_text = "Select your party. You can choose three members"


def draw():
    screen.clear()

    if MODE == "menu":
        background.draw()
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
        background.draw()
        P = padding
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

        skills_panel_height = 48 + 2 * padding
        skills_panel = SkillsPanel(screen, padding, skills_panel_height)
        skills_panel.render()

        info_panel_height = skills_panel_height - 16
        info_panel = InfoPanel(screen, padding, info_panel_height, skills_panel_height)
        info_panel.render()

        q_panel_width = 150
        everyone = party + enemies
        # q_panel = QueuePanel(screen, padding, q_panel_width, skills_panel_height, info_panel_height, party)
        q_panel = QueuePanel(screen, padding, q_panel_width, skills_panel_height, info_panel_height, everyone)
        q_panel.render()

        # hero_panel = SlotsPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width)
        hero_panel = HeroPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width, party)
        hero_panel.render()

        enemy_panel = EnemyPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width, enemies)
        enemy_panel.render()


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

    if MODE == "menu":
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

"""
def update():
    alien.left += 2
    if alien.left > WIDTH:
        alien.right = 0

def on_mouse_down(pos):
    global score
    if alien.collidepoint(pos):
        set_alien_hurt()
        score += 1
"""