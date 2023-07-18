from pgzero.actor import Actor
from pygame import Rect

c_white = (255, 255, 255, 128)
c_red = (255, 87, 51)
c_green = (76, 187, 23)

class MainMenu:
    def __init__(self, WIDTH, HEIGHT):
        self.game_credits = """
            Created by Anton V. Terekhov using the ingenious
            Platformer Art Complete Pack by Kenney Vleugels (www.kenney.nl)
            and the Pygame Zero framework by Daniel Pope.
        """
        self.logo = Actor("menu_logo")

        self.menu_start = Actor("menu_start")
        self.menu_load = Actor("menu_load")
        self.menu_credits = Actor("menu_credits")

        x = WIDTH / 2
        self.logo.center = (x, HEIGHT / 3)

        self.menu_start.center = (x, HEIGHT / 2 + 40)
        self.menu_load.center = (x, HEIGHT / 2 + 80)
        self.menu_credits.center = (x, HEIGHT / 2 + 120)

    def render(self):
        self.logo.draw()
        self.menu_start.draw()
        self.menu_load.draw()
        self.menu_credits.draw()


class Panel:
    def __init__(self, screen, padding, x, y, w, h, active=False, target=False):
        self.screen = screen
        self.padding = padding
        self.target = target
        if active:
            self.c = c_red
        else:
            self.c = c_white
        if self.target:
            self.c = c_green

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.box = Rect((self.x, self.y), (self.w, self.h))

    def set_active(self):
        self.c = c_red
        self.box = Rect((self.x, self.y), (self.w, self.h))

    def set_normal(self):
        self.c = c_white
        self.box = Rect((self.x, self.y), (self.w, self.h))

    def render(self):
        self.screen.draw.rect(self.box, self.c)

########################################
### GUI panels for the battle screen ###
########################################


class SkillSlot(Panel):
    def __init__(self, screen, padding, size_x, size_y, x, y, number, hero_skill, active=False):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.no = number
        if hero_skill is not None:
            self.hero_skill = hero_skill
        else:
            self.hero_skill = None
        Panel.__init__(self, screen, padding, x, y, size_x, size_y, active=active)
        # print(f"Hi dear I am the skillslot, my dimensions are {size_x}x{size_y}px")

    def render(self):
        Panel.render(self)
        if self.hero_skill is not None:
            self.hero_skill.actor.center = (self.x + self.size_x / 2, self.y + self.size_y / 2)
            self.hero_skill.actor.draw()


class SkillPanel(Panel):
    def __init__(self, screen, padding, height, hero, active_skill_no):
        x = padding
        y = screen.height - (padding + height)
        w = screen.width - 2 * padding
        h = height
        Panel.__init__(self, screen, padding, x, y, w, h)

        skill_count = len(hero.skills)

        self.skill_slots = []
        for i in range(0, 9):
            size_x = (w - 10 * padding) / 9
            size_y = height - 2 * padding
            x = 2 * padding + i * (padding + size_x)
            if i < skill_count:
                hero_skill = hero.skills[i]
            else:
                hero_skill = None
            if i == active_skill_no - 1:
                active = True
            else:
                active = False
            s = SkillSlot(screen, padding, size_x, size_y, x, y + padding, i + 1, hero_skill, active=active)
            self.skill_slots.append(s)

    def set_active_skill(self, no):
        for s in self.skill_slots:
            s.set_normal()
        self.skill_slots[no - 1].set_active()

    def render(self):
        Panel.render(self)
        for s in self.skill_slots:
            s.render()
            self.screen.draw.text(f"{s.no}", topleft=(s.x + 1, s.y + 1))


class InfoPanel(Panel):
    def __init__(self, screen, padding, height, skills_panel_height):
        x = padding
        y = screen.height - (padding + height + padding + skills_panel_height)
        w = screen.width - 2 * padding
        h = height
        self.message = "This info panel will tell you about all the actions made by friends and foes during the battle"
        Panel.__init__(self, screen, padding, x, y, w, h)

    def render(self):
        Panel.render(self)
        self.screen.draw.text(self.message,
                              topleft=(self.x + self.padding, self.y + self.padding),
                              width=self.w - 2 * self.padding,
                              fontsize=20)


class QueuePanel(Panel):
    def __init__(self, screen, padding, width, skills_panel_height, info_panel_height, party):
        x = padding
        y = padding
        w = width
        h = screen.height - (4 * padding + skills_panel_height + info_panel_height)
        self.party = party
        # print(f"Hi dear I am the Queue Panel, my height is {h} px")
        Panel.__init__(self, screen, padding, x, y, w, h)
        self.badge_size = 32
        self.padding = 3  # MAGIC NUMBER

    def render(self):
        Panel.render(self)
        for i, hero in enumerate(self.party):
            hero_x = self.x + self.padding
            hero_y = self.y + self.padding + i * (self.padding + self.badge_size)
            # print(hero_x, hero_y)
            hero.badge.topleft = (hero_x, hero_y)
            hero.badge.draw()
            self.screen.draw.text(f"Q {hero.dex * 10}",
                                  midleft=(hero_x + self.badge_size * 1.5 + self.padding,
                                           hero_y + self.badge_size / 2))


class Slot(Panel):
    def __init__(self, screen, padding, slot_x, slot_y, slot_width, slot_height, slot_no, hero, active=False):
        self.no = slot_no
        self.hero = hero
        self.slot_x = slot_x
        self.slot_y = slot_y
        self.slot_width = slot_width
        self.slot_height = slot_height
        Panel.__init__(self, screen, padding, slot_x, slot_y, slot_width, slot_height, active=active)

    def render(self):
        Panel.render(self)
        # self.screen.draw.text(f"{self.no}", topleft=(self.slot_x, self.slot_y))
        if self.hero is not None:
            self.hero.actor.midbottom = (self.slot_x + self.slot_width / 2, self.slot_y + self.slot_height - 1)
            self.hero.actor.draw()


class SlotsPanel(Panel):
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, x, party,
                 active_hero, mirror=False):
        # x = 2 * padding + queue_panel_width
        y = padding
        w = screen.width - (4 * padding + queue_panel_width)
        w = w / 2
        h = screen.height - (4 * padding + skills_panel_height + info_panel_height)
        Panel.__init__(self, screen, padding, x, y, w, h)
        self.slots = []
        slot_width = (w - 3 * padding) / 2
        slot_height = (h - 4 * padding) / 3
        # left column:
        for i in (1, 2, 3):
            if mirror:
                slot_x = x + padding + slot_width + padding
            else:
                slot_x = x + padding
            slot_y = y + padding + (i - 1) * (slot_height + padding)
            hero = None
            for char in party:
                if char.slot_no == i:
                    hero = char
            if hero is active_hero:
                active = True
            else:
                active = False
            s = Slot(screen, padding, slot_x, slot_y, slot_width, slot_height, i, hero, active=active)
            self.slots.append(s)
        # right column:
        for i in (4, 5, 6):
            if mirror:
                slot_x = x + padding
            else:
                slot_x = x + padding + slot_width + padding
            slot_y = y + padding + (i - 4) * (slot_height + padding)
            hero = None
            for char in party:
                if char.slot_no == i:
                    hero = char
            if hero is active_hero:
                active = True
            else:
                active = False
            s = Slot(screen, padding, slot_x, slot_y, slot_width, slot_height, i, hero, active=active)
            self.slots.append(s)

    def render(self):
        Panel.render(self)
        for s in self.slots:
            s.render()


class HeroPanel(SlotsPanel):
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, party, active_hero):
        x = 2 * padding + queue_panel_width
        SlotsPanel.__init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, x, party,
                            active_hero, mirror=True)


class EnemyPanel(SlotsPanel):
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, party, active_hero):
        x = 3 * padding + queue_panel_width + (screen.width - (4 * padding + queue_panel_width)) / 2
        SlotsPanel.__init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, x, party,
                            active_hero)


class BattleScreen:
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, q_panel_width,
                 party, enemies, everyone, active_skill, active_char):
        self.screen = screen
        self.skill_panel = SkillPanel(screen, padding, skills_panel_height, active_char, active_skill)
        self.info_panel = InfoPanel(screen, padding, info_panel_height, skills_panel_height)
        self.queue_panel = QueuePanel(screen, padding, q_panel_width, skills_panel_height, info_panel_height, everyone)
        self.hero_panel = HeroPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width, party,
                               active_char)
        self.enemy_panel = EnemyPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width, enemies,
                                 active_char)

    def render(self):
        self.skill_panel.render()
        self.info_panel.render()
        self.queue_panel.render()
        self.hero_panel.render()
        self.enemy_panel.render()
