# from pgzero.game import screen  # game won't start with this import line
# from dummy_enemies import *
from enemy_gen import spawn_dummy_enemies

from gui.main_menu import MainMenu
from gui.selection_screen import SelectionScreen
from gui.battle_screen import BattleScreen
from gui.party_screen import PartyScreen
from gui.result_screen import ResultScreen

from config import *
from init_game import init_game

MODE = "menu"
gui = MainMenu(WIDTH, HEIGHT)

aliens, inv = init_game()

party = []
enemies = []
everyone = party + enemies

active_skill = 1
cur_actor = None

target_list = []


def check_end():
    global party, enemies
    global MODE, gui
    all_dead = True
    for hero in party:
        if hero.dead is not True:
            all_dead = False
    if all_dead:
        MODE = "result"
        gui = ResultScreen(screen, PADDING, False)

    all_dead = True
    for enemy in enemies:
        if enemy.dead is not True:
            all_dead = False
    if all_dead:
        MODE = "result"
        gui = ResultScreen(screen, PADDING, True)


def next_turn():
    global cur_actor, everyone
    if cur_actor < (len(everyone) - 1):
        cur_actor += 1
    else:
        cur_actor = 0


def perform(author, targets, skill):
    global cur_actor, active_skill, everyone
    global gui
    global enemies  # DEBUG

    targets = [x for x in targets if x is not None]

    if author.mp >= skill.mp_cost:
        author.mp -= skill.mp_cost
        # TODO: compute "value" based on hero stats and current weapon
        skill.affect_target(30, *targets)

        active_skill = 1
        gui.skill_panel.set_active_skill(1)

        next_turn()

        gui.highlight(everyone[cur_actor])
        gui.update_skill_panel(everyone[cur_actor])

        message = f"{author} targets {targets} using {skill}. Now it's {everyone[cur_actor]}'s turn"
    else:
        message = f"Not enough MP!"
    gui.info_panel.print(message)


def draw():
    screen.clear()
    background.draw()

    if MODE in ("menu", "party", "battle", "result"):
        gui.render()
    elif MODE == "choice":
        gui.render(party)


def on_mouse_down(pos):
    global party, enemies, everyone
    global MODE, gui
    global active_skill, cur_actor
    global target_list

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

        if gui.next_btn.actor.collidepoint(pos):
            print("Starting new game")
            for hero in party:
                hero.set_stand()
            ####### DEBUG:
            party[0].equip_weapon(inv[0])
            party[1].equip_weapon(inv[1])
            party[2].equip_weapon(inv[2])
            ##############
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
            enemies = spawn_dummy_enemies()
            MODE = "battle"
            active_skill = 1

            everyone = party + enemies
            everyone = sorted(everyone, key=lambda x: x.dex, reverse=True)
            cur_actor = 0  # who makes a turn now

            gui = BattleScreen(screen, PADDING, SKILL_PANEL_HEIGHT, INFO_PANEL_HEIGHT, QUEUE_PANEL_WIDTH,
                               party, enemies, everyone, active_skill, everyone[cur_actor])

    elif MODE == "battle":
        # 1) Handling the player's turns:
        if everyone[cur_actor] in party:
            if everyone[cur_actor].dead:
                next_turn()
                message = f"Now it's {everyone[cur_actor]}'s turn"
                gui.info_panel.print(message)
                check_end()
            else:
                if len(target_list):
                    perform(everyone[cur_actor], target_list, everyone[cur_actor].skills[active_skill - 1])
                    check_end()

        # 2) Handling the enemies' turns:
        elif everyone[cur_actor] in enemies:
            # TODO: to be replaced with the automated enemy attacks
            if everyone[cur_actor].dead:
                next_turn()
                message = f"Now it's {everyone[cur_actor]}'s turn"
                gui.info_panel.print(message)
                check_end()
            else:
                target_list = [max(party, key=lambda x: x.hp)]  # AI will always choose a hero with max HP
                # however, if some of the heroes activated the only_target skill, then AI chooses him:
                for hero in party:
                    if hero.only_target:
                        target_list = [hero]
                perform(everyone[cur_actor], target_list, everyone[cur_actor].skills[active_skill - 1])
                check_end()

    elif MODE == "result":
        if gui.next_btn.actor.collidepoint(pos):
            gui = PartyScreen(screen, PADDING, party, inv)
            MODE = "party"


def on_mouse_move(pos):
    global active_skill, cur_actor
    global gui
    global everyone, target_list
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
                        target_list = [selection.hero]
                elif aim == "single":
                    if selection.hero is not None:
                        highlight = (selection.no, )
                        target_list = [selection.hero]
                    else:
                        target_list = []
                elif aim == "row":
                    if selection.no in (1, 2, 3):
                        highlight = (1, 2, 3)
                        target_list = [panel.slots[0].hero, panel.slots[1].hero, panel.slots[2].hero]
                    else:  # if selection.no in (4, 5, 6):
                        highlight = (4, 5, 6)
                        target_list = [panel.slots[3].hero, panel.slots[4].hero, panel.slots[5].hero]
                elif aim == "column":
                    if selection.no in (1, 4):
                        highlight = (1, 4)
                        target_list = [panel.slots[0].hero, panel.slots[3].hero]
                    elif selection.no in (2, 5):
                        highlight = (2, 5)
                        target_list = [panel.slots[1].hero, panel.slots[4].hero]
                    else:  # if s.no in (3, 6):
                        highlight = (3, 6)
                        target_list = [panel.slots[2].hero, panel.slots[5].hero]

                for s in panel.slots:
                    if s.no in highlight:
                        s.set_target()
                    else:
                        s.set_untarget()

                for s in inactive_panel.slots:
                    s.set_untarget()
            else:
                target_list = []
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
