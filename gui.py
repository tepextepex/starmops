from pygame import Rect


class Panel:
    def __init__(self, screen, padding, x, y, w, h):
        self.screen = screen
        self.padding = padding
        self.c = (255, 255, 255, 128)

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.box = Rect((self.x, self.y),
                        (self.w, self.h))

    def render(self):
        self.screen.draw.rect(self.box, self.c)

########################################
### GUI panels for the battle screen ###
########################################


class SkillSlot(Panel):
    def __init__(self, screen, padding, size_x, size_y, x, y, number):
        self.no = number
        Panel.__init__(self, screen, padding, x, y, size_x, size_y)


class SkillsPanel(Panel):
    def __init__(self, screen, padding, height):
        x = padding
        y = screen.height - (padding + height)
        w = screen.width - 2 * padding
        h = height
        Panel.__init__(self, screen, padding, x, y, w, h)

        self.skill_slots = []
        for i in range(0, 9):
            size_x = (w - 10 * padding) / 9
            size_y = height - 2 * padding
            x = 2 * padding + i * (padding + size_x)
            s = SkillSlot(screen, padding, size_x, size_y, x, y + padding, i + 1)
            self.skill_slots.append(s)

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
        # FOR DEBUG ONLY:
        party = sorted(party, key=lambda x: x.dex, reverse=True)
        # sorting should happen outside this class!
        #################
        x = padding
        y = padding
        w = width
        h = screen.height - (4 * padding + skills_panel_height + info_panel_height)
        print(f"Hi dear I am the Queue Panel, my height is {h} px")
        Panel.__init__(self, screen, padding, x, y, w, h)
        badge_size = 32
        padding = 3  # MAGIC NUMBER
        for i, hero in enumerate(party):
            hero_x = self.x + padding
            hero_y = self.y + padding + i * (padding + badge_size)
            print(hero_x, hero_y)
            hero.badge.topleft = (hero_x, hero_y)
            hero.badge.draw()
            self.screen.draw.text(f"Q {hero.dex * 10}",
                                  midleft=(hero_x + badge_size * 1.5 + padding, hero_y + badge_size / 2))


class Slot(Panel):
    def __init__(self, screen, padding, slot_x, slot_y, slot_width, slot_height, slot_no, hero):
        self.no = slot_no
        self.hero = hero
        self.slot_x = slot_x
        self.slot_y = slot_y
        self.slot_width = slot_width
        self.slot_height = slot_height
        Panel.__init__(self, screen, padding, slot_x, slot_y, slot_width, slot_height)

    def render(self):
        Panel.render(self)
        self.screen.draw.text(f"{self.no}", topleft=(self.slot_x, self.slot_y))
        if self.hero is not None:
            self.hero.actor.midbottom = (self.slot_x + self.slot_width / 2, self.slot_y + self.slot_height - 1)
            self.hero.actor.draw()


class SlotsPanel(Panel):
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, x, party, mirror=False):
        # x = 2 * padding + queue_panel_width
        y = padding
        w = screen.width - (4 * padding + queue_panel_width)
        w = w / 2
        h = screen.height - (4 * padding + skills_panel_height + info_panel_height)
        Panel.__init__(self, screen, padding, x, y, w, h)
        self.slots = []
        # TODO: if mirror...
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
            s = Slot(screen, padding, slot_x, slot_y, slot_width, slot_height, i, hero)
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
            s = Slot(screen, padding, slot_x, slot_y, slot_width, slot_height, i, hero)
            self.slots.append(s)

    def render(self):
        Panel.render(self)
        for s in self.slots:
            s.render()


class HeroPanel(SlotsPanel):
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, party):
        x = 2 * padding + queue_panel_width
        SlotsPanel.__init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, x, party,
                            mirror=True)


class EnemyPanel(SlotsPanel):
    def __init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, party):
        x = 3 * padding + queue_panel_width + (screen.width - (4 * padding + queue_panel_width)) / 2
        SlotsPanel.__init__(self, screen, padding, skills_panel_height, info_panel_height, queue_panel_width, x, party)
