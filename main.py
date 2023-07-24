from pgzero.actor import Actor
# from pgzero.game import screen  # game won't start with this import line
from pygame import Rect

from gui.selection_screen import SelectionScreen
from hero_skills import *
from dummy_enemies import *

from classes import Char, Weapon, Armor
from gui.main_menu import MainMenu
from gui.battle_screen import BattleScreen
from gui.party_screen import HorBar, PartyScreen
from gui.base import c_red, c_blue
from config import *

MODE = "menu"
main_menu = MainMenu(WIDTH, HEIGHT)
battle_screen = None
party_screen = None
selection_screen = None

background = Actor("purple_space")

quit_btn = Actor("arrow_red")
quit_btn.bottomleft = 0 + PADDING, HEIGHT

next_btn = Actor("arrow_green")
next_btn.bottomright = WIDTH - PADDING, HEIGHT

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
pink.learn(melee_attack, rage)

yellow = Char("Eastwood", "alien_yellow",
              "A gunslinger without a name. Everybody calls him Eastwood but we have no idea why",
              3, 10, 5, 7)
yellow.learn(ranged_attack, piercing_shot)

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

    if author.mp >= skill.mp_cost:
        author.mp -= skill.mp_cost
        # TODO: compute "value" based on hero stats and current weapon
        skill.affect_target(target, 30)

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
    else:
        message = f"Not enough MP!"
    battle_screen.info_panel.print(message)


def draw():
    global active_skill

    screen.clear()
    background.draw()

    if MODE == "menu":
        main_menu.render()

    elif MODE == "choice":
        selection_screen.render(party)

    elif MODE == "party":
        party_screen.render()

    elif MODE == "battle":
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
    global main_menu, battle_screen, party_screen, selection_screen
    global active_skill, cur_actor

    if MODE == "menu":
        if main_menu.menu_start.collidepoint(pos):
            MODE = "choice"
            selection_screen = SelectionScreen(screen, PADDING, aliens)
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
            party_screen = PartyScreen(screen, PADDING, party, inv)
            MODE = "party"

    elif MODE == "party":
        for hero in party:
            if hero.actor.collidepoint(pos):
                print(hero)
                hero.funny_jump()

        if party_screen.next_btn.actor.collidepoint(pos):
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
            target_actor = max(party, key=lambda x: x.hp)  # AI will always choose a hero with max HP
            # however, if some of the heroes activated the only_target skill, then AI chooses him:
            for hero in party:
                if hero.only_target:
                    target_actor = hero
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
            # TODO: untarget all the foe slots
            for s in battle_screen.hero_panel.slots:
                if s.box.collidepoint(pos):
                    if aim == "single":
                        s.set_target()
                    elif aim == "self":
                        if s.hero == everyone[cur_actor]:
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
            # TODO: проверять, хватает ли маны на выбранный скилл
            key_no = int(key.name.split("_")[1])
            if key_no <= len(everyone[cur_actor].skills):
                active_skill = key_no
                battle_screen.skill_panel.set_active_skill(key_no)
