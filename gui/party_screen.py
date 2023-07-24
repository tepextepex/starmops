from pygame import Rect
from pgzero.actor import Actor

from gui.base import c_red, c_blue, Panel


########################################
### GUI panels for the party screen  ###
########################################

class HorBar:
    def __init__(self, screen, left, top, height, width, value, max_value, color):
        self.screen = screen
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.value = value
        self.max_value = max_value

        self.cur_width = round(value / self.max_value * self.width)
        if (self.cur_width == 0) and (self.value > 0):
            self.cur_width = 1  # should be at least 1px if hp/mp is not zero
        self.cur_left = left
        self.box = Rect((self.cur_left, self.top), (self.cur_width, self.height))

    def render(self):
        self.screen.draw.filled_rect(self.box, self.color)
        self.screen.draw.text(f"{self.value}/{self.max_value}",
                              midtop=(self.left + self.width / 2, self.top),
                              width=self.width,
                              fontsize=18)


class HeroPanel:
    def __init__(self, screen, padding, x, y, width, height, hero):
        self.screen = screen
        self.padding = padding
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hero = hero
        self.box = Panel(screen, padding, x, y, width, height, False)
        self.actor = hero.actor
        self.actor.midbottom = (self.x + self.width / 2, self.y + padding + 90)
        self.bars = []
        self.bars.append(
            HorBar(screen, x + 10, self.y + padding + 90 + 25, 12, self.width - 20, self.hero.hp, self.hero.max_hp(), c_red))
        self.bars.append(
            HorBar(screen, x + 10, self.y + padding + 90 + 40, 12, self.width - 20, self.hero.mp, self.hero.max_mp(), c_blue))

    def render(self):
        self.box.render()
        self.actor.draw()
        self.screen.draw.text(self.hero.name,
                              midtop=(self.x + self.width / 2, self.y + 105))
        for bar in self.bars:
            bar.render()
        # column 1
        self.screen.draw.text(f"STR {self.hero.str}",
                              midtop=(self.x + self.width / 4, self.y + 125 + 4 * self.padding))
        self.screen.draw.text(f"DEX {self.hero.dex}",
                              midtop=(self.x + self.width / 4, self.y + 120 + 7 * self.padding))
        # column 2
        self.screen.draw.text(f"CON {self.hero.con}",
                              midtop=(self.x + 3 * self.width / 4, self.y + 125 + 4 * self.padding))
        self.screen.draw.text(f"INT {self.hero.int}",
                              midtop=(self.x + 3 * self.width / 4, self.y + 120 + 7 * self.padding))


class InvSlot:
    def __init__(self, screen, padding, x, y, width, height, item):
        self.box = Panel(screen, padding, x, y, width, height, False)
        self.item = item
        if self.item is not None:
            item.actor.center = (x + width / 2, y + height / 2)

    def render(self):
        self.box.render()
        if self.item is not None:
            self.item.actor.draw()


class InventoryPanel:
    def __init__(self, screen, padding, x, y, width, height, inventory):
        self.box = Panel(screen, padding, x, y, width, height, False)
        self.slots = []

        cols, rows = 10, 3
        slot_width = (width - (cols + 1) * padding) / cols
        # slot_height = (height - (rows + 1) * padding) / rows
        slot_height = slot_width
        # print(slot_height)  # 51 px
        item_no = 0
        for row in range(rows):
            slot_y = y + padding + row * (padding + slot_height)
            for col in range(cols):
                slot_x = x + padding + col * (padding + slot_width)
                item = inventory[item_no] if item_no < len(inventory) else None
                # if item is not None:
                self.slots.append(InvSlot(screen, padding, slot_x, slot_y, slot_width, slot_height, item))
                item_no += 1

    def render(self):
        self.box.render()
        for slot in self.slots:
            slot.render()


class NextBtn:
    def __init__(self, screen, padding):
        self.actor = Actor("arrow_green")
        self.actor.bottomright = screen.width - 2 * padding, screen.height

    def render(self):
        self.actor.draw()


class PartyScreen:
    def __init__(self, screen, padding, party, inventory):
        self.screen = screen
        self.party = party
        self.padding = padding
        self.hero_panels = []
        width = (screen.width - self.padding * (len(party) + 1)) / len(party)
        height = (screen.height - 3 * self.padding) / 2
        for i, hero in enumerate(party):
            pan = HeroPanel(self.screen, self.padding,
                            self.padding + i * (self.padding + width), self.padding,
                            width, height, hero)
            self.hero_panels.append(pan)
        self.inv_panel = InventoryPanel(screen, padding, self.padding, height + 2 * self.padding,
                                        screen.width - 2 * padding, height, inventory)
        self.next_btn = NextBtn(self.screen, self.padding)

    def render(self):
        for p in self.hero_panels:
            p.render()
        self.inv_panel.render()
        self.next_btn.render()
