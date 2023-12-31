import pygame
from pygame import Rect

from gui.base import c_red, c_blue, c_white, c_green, Panel


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
        self.popup = None
        if hero_skill is not None:
            self.hero_skill = hero_skill
        else:
            self.hero_skill = None
        Panel.__init__(self, screen, padding, x, y, size_x, size_y, active=active, fill=True)

    def update(self, hero_skill):
        self.hero_skill = hero_skill

    def open_popup(self, pos):
        self.popup = pos

    def close_popup(self):
        self.popup = None

    def render(self):
        Panel.render(self)
        if self.hero_skill is not None:
            self.hero_skill.actor.center = (self.x + self.size_x / 2, self.y + self.size_y / 2)
            self.hero_skill.actor.draw()
        if self.popup:
            p_size = 120
            x, y = self.popup
            y -= p_size
            popup_background = Rect((x, y), (p_size, p_size))
            self.screen.draw.filled_rect(popup_background, c_white)
            self.screen.draw.text(self.hero_skill.name,
                                  midtop=(x + p_size / 2, y + self.padding),
                                  width=p_size - 2 * self.padding,
                                  fontsize=20, color=(20, 20, 20))
            self.screen.draw.text(self.hero_skill.description,
                                  midtop=(x + p_size / 2, y + self.padding + 20),
                                  width=p_size - 2 * self.padding,
                                  fontsize=20, color=(40, 40, 40))


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

    def update_all(self, hero):
        skill_count = len(hero.skills)
        for i in range(0, 9):
            if i < skill_count:
                hero_skill = hero.skills[i]
            else:
                hero_skill = None
            self.skill_slots[i].update(hero_skill)

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

    def print(self, message):
        self.message = message

    def render(self):
        Panel.render(self)
        self.screen.draw.text(self.message,
                              topleft=(self.x + self.padding, self.y + self.padding),
                              width=self.w - 2 * self.padding,
                              fontsize=20)


class QueuePanel(Panel):
    def __init__(self, screen, padding, width, skills_panel_height, info_panel_height, party, active_char):
        self.padding = padding
        self.x = padding
        self.y = padding
        self.w = width
        self.h = screen.height - (4 * padding + skills_panel_height + info_panel_height)
        self.party = party
        Panel.__init__(self, screen, padding, self.x, self.y, self.w, self.h)
        self.badge_size = 32
        self.v_int = 3  # MAGIC NUMBER
        self.cur_actor = active_char

    def update(self, active_char):
        self.cur_actor = active_char

    def render(self):
        Panel.render(self)
        for i, hero in enumerate(self.party):
            hero_x = self.x + self.padding
            hero_y = self.y + self.padding + i * (self.v_int + self.badge_size)
            hero.badge.topleft = (hero_x, hero_y)
            hero.badge.draw()
            self.screen.draw.text(f"Q {hero.dex * 10}",
                                  midleft=(hero_x + self.badge_size * 1.5 + self.padding,
                                           hero_y + self.badge_size / 2))
            if hero is self.cur_actor:
                highlight = pygame.Surface((self.w - 2 * self.padding, self.badge_size))
                highlight.set_alpha(40)
                highlight.fill(c_green)
                self.screen.blit(highlight, (hero_x, hero_y))

                self.box = Rect((hero_x, hero_y),
                                (self.w - 2 * self.padding, self.badge_size))
                self.screen.draw.rect(self.box, c_green)


class VertBar:
    def __init__(self, screen, left, top, height, width, value, max_value, color):
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.value = value
        self.max_value = max_value

        self.cur_height = round(value / self.max_value * self.height)
        if (self.cur_height == 0) and (self.value > 0):
            self.cur_height = 1  # should be at least 1px if hp/mp is not zero
        # print(f"cur height is {self.cur_height} out of {self.height}")
        self.cur_top = self.top + self.height - self.cur_height
        self.box = Rect((self.left, self.cur_top), (self.width, self.cur_height))

    def update(self, value):
        self.value = value
        self.cur_height = round(value / self.max_value * self.height)
        if (self.cur_height == 0) and (self.value > 0):
            self.cur_height = 1  # should be at least 1px if hp/mp is not zero
        self.cur_top = self.top + self.height - self.cur_height
        self.box = Rect((self.left, self.cur_top), (self.width, self.cur_height))

    def render(self):
        self.screen.draw.filled_rect(self.box, self.color)


class Slot(Panel):
    def __init__(self, screen, padding, slot_x, slot_y, slot_width, slot_height, slot_no, hero, active=False):
        self.no = slot_no
        self.hero = hero
        self.slot_x = slot_x
        self.slot_y = slot_y
        self.slot_width = slot_width
        self.slot_height = slot_height
        self.hp_bar = None
        self.mp_bar = None
        if self.hero is not None:
            bar_w = 9
            bar_h = slot_height - 6
            self.hp_bar = VertBar(screen, slot_x + 3, slot_y + 3, bar_h, bar_w,
                                  hero.hp, hero.max_hp(), c_red)
            self.mp_bar = VertBar(screen, slot_x + slot_width - bar_w - 3, slot_y + 3, bar_h, bar_w,
                                  hero.mp, hero.max_mp(), c_blue)
        Panel.__init__(self, screen, padding, slot_x, slot_y, slot_width, slot_height, active=active, fill=True)

    def render(self):
        Panel.render(self)
        # self.screen.draw.text(f"{self.no}", topleft=(self.slot_x, self.slot_y))
        if self.hero is not None:
            self.hero.actor.midbottom = (self.slot_x + self.slot_width / 2, self.slot_y + self.slot_height - 1)
            self.hero.actor.draw()

            self.hp_bar.update(self.hero.hp)
            self.mp_bar.update(self.hero.mp)

            self.hp_bar.render()
            self.mp_bar.render()


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
        self.queue_panel = QueuePanel(screen, padding, q_panel_width, skills_panel_height, info_panel_height,
                                      everyone, active_char)
        self.hero_panel = HeroPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width, party,
                               active_char)
        self.enemy_panel = EnemyPanel(screen, padding, skills_panel_height, info_panel_height, q_panel_width, enemies,
                                 active_char)

    def highlight(self, char):
        for slot in self.hero_panel.slots:
            if slot.hero is char:
                slot.set_active()
            else:
                slot.set_normal()
        for slot in self.enemy_panel.slots:
            if slot.hero is char:
                slot.set_active()
            else:
                slot.set_normal()

    def update(self, char):
        self.skill_panel.update_all(char)
        self.queue_panel.update(char)

    def render(self):
        self.info_panel.render()
        self.queue_panel.render()
        self.hero_panel.render()
        self.enemy_panel.render()
        self.skill_panel.render()
