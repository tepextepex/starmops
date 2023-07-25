from pgzero.actor import Actor
# from pgzero.game import screen  # game won't start with this import line
from hero_skills import *
from dummy_enemies import *

from gui.main_menu import MainMenu
from gui.selection_screen import SelectionScreen
from gui.battle_screen import BattleScreen
from gui.party_screen import PartyScreen
from gui.base import c_red, c_blue
from config import *
from init_game import init_game

MODE = "menu"
gui = MainMenu(WIDTH, HEIGHT)

quit_btn = Actor("arrow_red")
quit_btn.bottomleft = 0 + PADDING, HEIGHT

next_btn = Actor("arrow_green")
next_btn.bottomright = WIDTH - PADDING, HEIGHT

aliens, inv = init_game()

party = []
enemies = []
everyone = party + enemies

active_skill = 1
cur_actor = None


def make_turn(author, target, skill):
    global cur_actor, active_skill, everyone
    global gui
    global enemies  # DEBUG

    if author.mp >= skill.mp_cost:
        author.mp -= skill.mp_cost
        # TODO: compute "value" based on hero stats and current weapon
        skill.affect_target(target, 30)

        active_skill = 1
        gui.skill_panel.set_active_skill(1)

        if cur_actor < (len(everyone) - 1):
            cur_actor += 1
        else:
            cur_actor = 0

        gui.highlight(everyone[cur_actor])
        gui.update_skill_panel(everyone[cur_actor])

        message = f"{author} targets {target} using {skill}. Now it's {everyone[cur_actor]}'s turn"
    else:
        message = f"Not enough MP!"
    gui.info_panel.print(message)


def draw():
    screen.clear()
    background.draw()

    if MODE in ("menu", "party", "battle"):
        gui.render()
    elif MODE == "choice":
        gui.render(party)


def on_mouse_down(pos):
    global desc_text
    global party, enemies, everyone
    global MODE, gui
    global active_skill, cur_actor

    if MODE == "menu":
        if gui.menu_start.collidepoint(pos):
            MODE = "choice"
            gui = SelectionScreen(screen, PADDING, aliens)
        elif gui.menu_load.collidepoint(pos):
            print("Not implemented yet! Sorry")
        elif gui.menu_credits.collidepoint(pos):
            print(gui.game_credits)

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
                gui.update_desc(f"{a.desc}\nSTR {a.str} / DEX {a.dex} / CON {a.con} / INT {a.int}")

        if next_btn.collidepoint(pos):
            print("Starting game")
            for hero in party:
                hero.set_stand()
            gui = PartyScreen(screen, PADDING, party, inv)
            MODE = "party"

    elif MODE == "party":
        for hero in party:
            if hero.actor.collidepoint(pos):
                print(hero)
                hero.funny_jump()

        if gui.next_btn.actor.collidepoint(pos):
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

            gui = BattleScreen(screen, PADDING, SKILL_PANEL_HEIGHT, INFO_PANEL_HEIGHT, QUEUE_PANEL_WIDTH,
                               party, enemies, everyone, active_skill, everyone[cur_actor])

    elif MODE == "battle":
        if everyone[cur_actor] in party:
            target_actor = None
            if everyone[cur_actor].skills[active_skill - 1].target == "foe":
                # then we should target the enemies only
                for slot in gui.enemy_panel.slots:
                    if slot.box.collidepoint(pos):
                        print(f"The enemy is on target: {slot.hero}")
                        target_actor = slot.hero
                # TODO: check what skill is active now (melee|ranged & aim-mode)
            elif everyone[cur_actor].skills[active_skill - 1].target == "friend":
                # then we are able to target only our friends
                for slot in gui.hero_panel.slots:
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
    global gui
    global everyone
    if MODE == "battle":
        if everyone[cur_actor] in party:  # highlight works only during the player's turn
            # TODO: check what skill is active now (melee|ranged & aim-mode)
            target = everyone[cur_actor].skills[active_skill - 1].target
            panel = gui.hero_panel if target == "friend" else gui.enemy_panel
            inactive_panel = gui.enemy_panel if target == "friend" else gui.hero_panel

            # checking slots of the active panel for collision:
            selection = None
            for s in panel.slots:
                if s.box.collidepoint(pos):
                    selection = s

            if selection is not None:
                # choosing which slots should be highlighted, according to the skill's target mode:
                highlight = ()
                aim = everyone[cur_actor].skills[active_skill - 1].aim
                if aim == "self":
                    if selection.hero == everyone[cur_actor]:
                        highlight = (selection.no, )
                elif aim == "single":
                    if selection.hero is not None:
                        highlight = (selection.no, )
                elif aim == "row":
                    if selection.no in (1, 2, 3):
                        highlight = (1, 2, 3)
                    else:  # if selection.no in (4, 5, 6):
                        highlight = (4, 5, 6)
                elif aim == "column":
                    if selection.no in (1, 4):
                        highlight = (1, 4)
                    elif selection.no in (2, 5):
                        highlight = (2, 5)
                    else:  # if s.no in (3, 6):
                        highlight = (3, 6)

                for s in panel.slots:
                    if s.no in highlight:
                        s.set_target()
                    else:
                        s.set_untarget()

                for s in inactive_panel.slots:
                    s.set_untarget()
            else:
                for s in panel.slots + inactive_panel.slots:
                    s.set_untarget()


def on_key_up(key):
    global active_skill
    global gui
    global everyone, cur_actor
    if MODE == "battle":
        num_keys = [f"K_{x}" for x in range(1, 10)]
        if key.name in num_keys:
            # TODO: проверять, хватает ли маны на выбранный скилл
            key_no = int(key.name.split("_")[1])
            if key_no <= len(everyone[cur_actor].skills):
                active_skill = key_no
                gui.skill_panel.set_active_skill(key_no)
