from pgzero.actor import Actor
# from pgzero.game import screen  # game won't start with this import line
from pygame import Rect
from hero_skills import *
from dummy_enemies import *

from classes import Char, Weapon, Armor
from gui.main_menu import MainMenu
from gui.battle_screen import BattleScreen, HorBar
from gui.battle_screen import c_red, c_blue
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
everyone = party + enemies

dummy_gun = Weapon("ranged", "Ray gun", "raygun", 10)
dummy_sword = Weapon("melee", "Rusty sword", "sword_bronze", 15)
dummy_shield = Armor("dummy", "Wooden shield", "shield_bronze", 5)
dummy_umbrella = Armor("dummy", "Umbrella", "umbrella_open", 2)

inv = [dummy_gun, dummy_sword, dummy_shield, dummy_umbrella]

active_skill = 1
cur_actor = None

desc_text = "Select your party. You can choose three members"


def make_turn(author, target, skill):
    global cur_actor, active_skill, everyone
    global battle_screen
    global enemies  # DEBUG

    author.mp -= 10
    target.hp -= 30

    active_skill = 1
    battle_screen.skill_panel.set_active_skill(1)

    if cur_actor < (len(everyone) - 1):
        cur_actor += 1
    else:
        cur_actor = 0

    battle_screen.highlight(everyone[cur_actor])
    battle_screen.update_skill_panel(everyone[cur_actor])

    # print(f"{author} targets {target} using {skill}")
    # print(f"Current actor: {everyone[cur_actor]}")
    message = f"{author} targets {target} using {skill}. Now it's {everyone[cur_actor]}'s turn"
    battle_screen.info_panel.print(message)


def draw():
    global active_skill
    # global hero_panel, enemy_panel

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
        bars = []
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
            # HP and MP bars:
            bars.append(HorBar(screen, x + 10, y + 4, 12, w - 20, hero.hp, hero.max_hp(), c_red))
            bars.append(HorBar(screen, x + 10, y + 20, 12, w - 20, hero.mp, hero.max_mp(), c_blue))
            # column 1
            #screen.draw.text(f"MAX HP {hero.max_hp()}", midtop=(x + w / 4, y + P))
            screen.draw.text(f"STR {hero.str}", midtop=(x + w / 4, y + 4 * P))
            screen.draw.text(f"DEX {hero.dex}", midtop=(x + w / 4, y + 7 * P))
            # column 2
            #screen.draw.text(f"MAX MP {hero.max_mp()}", midtop=(x + 3 * w / 4, y + P))
            screen.draw.text(f"CON {hero.con}", midtop=(x + 3 * w / 4, y + 4 * P))
            screen.draw.text(f"INT {hero.int}", midtop=(x + 3 * w / 4, y + 7 * P))

        for bar in bars:
            bar.render()
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
    global party, enemies, everyone
    global MODE
    global main_menu, battle_screen
    global active_skill, cur_actor

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

    elif MODE == "battle":
        if everyone[cur_actor] in party:
            target_actor = None
            if everyone[cur_actor].skills[active_skill - 1].target == "foe":
                # then we should target the enemies only
                for slot in battle_screen.enemy_panel.slots:
                    if slot.box.collidepoint(pos):
                        print(f"The enemy is on target: {slot.hero}")
                        target_actor = slot.hero
                # TODO: check what skill is active now (melee|ranged & aim-mode)
            elif everyone[cur_actor].skills[active_skill - 1].target == "friend":
                # then we are able to target only our friends
                for slot in battle_screen.hero_panel.slots:
                    if slot.box.collidepoint(pos):
                        print(f"The friend is on target: {slot.hero}")
                        target_actor = slot.hero
                # TODO: check what skill is active now (melee|ranged & aim-mode)
            if target_actor is not None:
                make_turn(everyone[cur_actor], target_actor, everyone[cur_actor].skills[active_skill - 1])

        elif everyone[cur_actor] in enemies:
            # TODO: to be replaced with the automated enemy attacks
            for slot in battle_screen.hero_panel.slots:
                if slot.box.collidepoint(pos):
                    print(f"The friend is on target: {slot.hero}")
                    target_actor = slot.hero
            make_turn(everyone[cur_actor], target_actor, everyone[cur_actor].skills[active_skill - 1])


def on_mouse_move(pos):
    global active_skill, cur_actor
    global battle_screen
    global everyone
    if MODE == "battle":
        # TODO: check whose turn is this (heroes or enemies)
        # TODO: check what skill is active now (melee|ranged & aim-mode)
        aim = everyone[cur_actor].skills[active_skill - 1].aim
        target = everyone[cur_actor].skills[active_skill - 1].target
        if target == "friend":
            for s in battle_screen.hero_panel.slots:
                if s.box.collidepoint(pos):
                    if aim == "single":
                        s.set_target()
                else:
                    s.set_untarget()

        if target == "foe":
            for s in battle_screen.enemy_panel.slots:
                if s.box.collidepoint(pos):
                    if aim == "single":
                        s.set_target()
                    elif aim == "row":
                        if s.no in (1, 2, 3):
                            battle_screen.enemy_panel.slots[0].set_target()
                            battle_screen.enemy_panel.slots[1].set_target()
                            battle_screen.enemy_panel.slots[2].set_target()
                        elif s.no in (4, 5, 6):
                            battle_screen.enemy_panel.slots[3].set_target()
                            battle_screen.enemy_panel.slots[4].set_target()
                            battle_screen.enemy_panel.slots[5].set_target()
                    elif aim == "column":
                        if s.no in (1, 4):
                            battle_screen.enemy_panel.slots[0].set_target()
                            battle_screen.enemy_panel.slots[3].set_target()
                        elif s.no in (2, 5):
                            battle_screen.enemy_panel.slots[1].set_target()
                            battle_screen.enemy_panel.slots[4].set_target()
                        elif s.no in (3, 6):
                            battle_screen.enemy_panel.slots[2].set_target()
                            battle_screen.enemy_panel.slots[5].set_target()
                else:
                    s.set_untarget()


def on_key_up(key):
    global active_skill
    global battle_screen
    global everyone, cur_actor
    if MODE == "battle":
        num_keys = [f"K_{x}" for x in range(1, 10)]
        if key.name in num_keys:
            # TODO: проверять, есть ли вообще такой скилл у текущего игрока
            key_no = int(key.name.split("_")[1])
            if key_no <= len(everyone[cur_actor].skills):
                active_skill = key_no
                battle_screen.skill_panel.set_active_skill(key_no)
