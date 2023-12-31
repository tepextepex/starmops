# from pgzero.game import screen  # game won't start with this import line
from pgzero.clock import clock

from enemy_gen import spawn_dummy_enemies

from gui.main_menu import MainMenu
from gui.selection_screen import SelectionScreen
from gui.battle_screen import BattleScreen
from gui.party_screen import PartyScreen
from gui.result_screen import ResultScreen

from config import *
from init_game import init_game

from armor import Armor
from potion import Potion
from weapon import Weapon, Chainsaw, LaserSaber, RayGun, MagicWand

MODE = "menu"

TIER = 0

gui = MainMenu(WIDTH, HEIGHT)

aliens, inv = init_game()

party = []
enemies = []
everyone = party + enemies

active_skill = 1
cur_actor = None

target_list = []

scheduled = False
drag = None


def check_end():
    global party, enemies
    global MODE, gui, inv
    all_dead = True
    for hero in party:
        if hero.dead is not True:
            all_dead = False
    if all_dead:
        MODE = "result"
        gui = ResultScreen(screen, PADDING, False, TIER)
        inv += gui.loot.copy()

    all_dead = True
    for enemy in enemies:
        if enemy.dead is not True:
            all_dead = False
    if all_dead:
        MODE = "result"
        gui = ResultScreen(screen, PADDING, True, TIER)
        inv += gui.loot.copy()


def next_turn():
    global cur_actor, everyone, gui

    everyone[cur_actor].remove_effects()

    if cur_actor < (len(everyone) - 1):
        cur_actor += 1
    else:
        cur_actor = 0

    gui.highlight(everyone[cur_actor])
    gui.update(everyone[cur_actor])


def calc_damage(stat_value, weapon_dmg):
    value = stat_value * weapon_dmg / 4
    return value


def calc_coef(skill, author):
    if skill.name == "Melee attack":
        if isinstance(author.weapon, Chainsaw):  # Chainsaw, LaserSaber, RayGun, MagicWand
            coef = author.str
        elif isinstance(author.weapon, LaserSaber):
            coef = author.dex
        elif isinstance(author.weapon, RayGun):
            coef = author.dex
        elif isinstance(author.weapon, MagicWand):
            coef = author.int
        else:
            coef = author.str
    else:
        if skill.uses == "STR":
            coef = author.str
        elif skill.uses == "DEX":
            coef = author.dex
        elif skill.uses == "INT":
            coef = author.int

    return coef


def perform(author, targets, skill):
    global cur_actor, active_skill, everyone
    global gui
    global enemies  # DEBUG

    targets = [x for x in targets if x is not None]

    if author.mp >= skill.mp_cost:
        author.mp -= skill.mp_cost

        coef = calc_coef(skill, author)
        weapon_dmg = author.weapon.dmg if author.weapon is not None else 10

        dmg = calc_damage(coef, weapon_dmg)
        print(f"Skill effect: {dmg}")  # DEBUG
        skill.affect_target(dmg, *targets)

        active_skill = 1
        gui.skill_panel.set_active_skill(1)

        next_turn()

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
    global drag
    global inv

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
            gui = PartyScreen(screen, PADDING, party, inv)
            MODE = "party"

    elif MODE == "party":
        for hero in party:
            if hero.actor.collidepoint(pos):
                hero.funny_jump()

        # TODO: drag'n'drop for items:
        if drag is None:  # first click
            for s in gui.inv_panel.slots:
                if s.box.box.collidepoint(pos):
                    if s.item is not None:
                        drag = (s.item, s.item.actor.center)
        else:  # second click
            item = drag[0]
            if isinstance(item, Potion):  # potions should be collided with heroes themselves
                for hero in party:
                    if hero.actor.collidepoint(pos):
                        item.apply(hero)  # applying the effects of potion to the selected hero
                        inv.remove(item)  # removing the used item from inventory
                        gui.update(inv)  # updating gui
                        break  # goes to the else statement
                else:
                    item.actor.center = drag[1]  # just returning the item on its place in inventory

            elif isinstance(item, Weapon):  # weapons should be collided with the slots to the left from hero
                for panel in gui.hero_panels:
                    if panel.weapon_slot.box.box.collidepoint(pos):
                        if panel.weapon_slot.item is not None:
                            panel.weapon_slot.item.equipped = None
                        panel.weapon_slot.item = item
                        panel.weapon_slot.center_actor()
                        panel.hero.equip_weapon(item)
                        gui.update(inv)  # updating gui
                        break
                else:
                    item.actor.center = drag[1]  # just returning the item on its place in inventory

            elif isinstance(item, Armor):
                for panel in gui.hero_panels:
                    if panel.armor_slot.box.box.collidepoint(pos):
                        if panel.armor_slot.item is not None:
                            panel.armor_slot.item.equipped = None
                        panel.armor_slot.item = item
                        panel.armor_slot.center_actor()
                        panel.hero.equip_armor(item)
                        gui.update(inv)  # updating gui
                        break
                else:
                    item.actor.center = drag[1]  # just returning the item on its place in inventory

            drag = None

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
                dead_name = everyone[cur_actor].name
                next_turn()
                message = f"{dead_name} is dead. Now it's {everyone[cur_actor]}'s turn"
                gui.info_panel.print(message)
                check_end()
            elif everyone[cur_actor].stun:
                dead_name = everyone[cur_actor].name
                next_turn()
                message = f"{dead_name} is stunned. Now it's {everyone[cur_actor]}'s turn"
                gui.info_panel.print(message)
                check_end()
            else:
                if len(target_list):
                    perform(everyone[cur_actor], target_list, everyone[cur_actor].skills[active_skill - 1])
                    check_end()

        # 2) Handling enemies' turns - it happens inside the update() function using the clock()

    elif MODE == "result":
        if gui.next_btn.actor.collidepoint(pos):
            gui = PartyScreen(screen, PADDING, party, inv)
            MODE = "party"


def enemy_turn_dead():
    global everyone, cur_actor, gui
    global scheduled
    name = everyone[cur_actor].name
    next_turn()
    message = f"{name} is dead. Now it's {everyone[cur_actor]}'s turn"
    gui.info_panel.print(message)
    check_end()
    scheduled = False


def enemy_turn_stun():
    global everyone, cur_actor, gui
    global scheduled
    name = everyone[cur_actor].name
    next_turn()
    message = f"{name} is stunned and misses a turn. Now it's {everyone[cur_actor]}'s turn"
    gui.info_panel.print(message)
    check_end()
    scheduled = False


def enemy_turn_alive():
    global everyone, cur_actor, party
    global target_list, gui, active_skill
    global scheduled
    target_list = [max(party, key=lambda x: x.hp)]  # AI will always choose a hero with max HP
    # however, if some of the heroes activated the only_target skill, then AI chooses him:
    for hero in party:
        if hero.only_target:
            target_list = [hero]
    perform(everyone[cur_actor], target_list, everyone[cur_actor].skills[active_skill - 1])
    check_end()
    scheduled = False


def update():
    global everyone, cur_actor
    global gui, MODE
    global target_list
    global scheduled

    # Automated enemy turns:
    if MODE == "battle":
        if everyone[cur_actor] in enemies:
            if everyone[cur_actor].dead:
                if not scheduled:
                    clock.schedule(enemy_turn_dead, 1.5)
                    scheduled = True
            elif everyone[cur_actor].stun:
                if not scheduled:
                    clock.schedule(enemy_turn_stun, 1.5)
                    scheduled = True
            else:
                if not scheduled:
                    clock.schedule(enemy_turn_alive, 1.5)  # schedule_unique DOES NOT WORK, because it constantly postpones the execution
                    scheduled = True


def on_mouse_move(pos):
    global active_skill, cur_actor
    global gui
    global everyone, target_list
    global drag
    if MODE == "party":
        # checking collisions with the inventory slots to show pop-ups with item descriptions:
        for s in gui.inv_panel.slots:
            if s.box.box.collidepoint(pos):
                if s.item is not None:
                    s.open_popup(pos)
            else:
                s.close_popup()

        for s in gui.hero_panels:
            if s.weapon_slot.box.box.collidepoint(pos):
                if s.weapon_slot.item is not None:
                    s.weapon_slot.open_popup(pos)
            else:
                s.weapon_slot.close_popup()

        # drag'n'drop for items:
        if drag is not None:
            drag[0].actor.center = pos

    elif MODE == "battle":
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
                elif aim == "area":
                    highlight = (1, 2, 3, 4, 5, 6)
                    target_list = [panel.slots[0].hero, panel.slots[1].hero, panel.slots[2].hero,
                                   panel.slots[3].hero, panel.slots[4].hero, panel.slots[5].hero]

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

            # checking collisions with skill-slots to show pop-ups with descriptions:
            for s in gui.skill_panel.skill_slots:
                if s.box.collidepoint(pos):
                    if s.hero_skill is not None:
                        s.open_popup(pos)
                else:
                    s.close_popup()


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
