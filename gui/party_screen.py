from pygame import Rect

from gui.base import c_red, c_blue, c_white, Panel, NextBtn

from weapon import Weapon


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
        self.screen.draw.text(f"{round(self.value)}/{self.max_value}",
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
        self.hero_mid_y = self.y + padding + 90
        self.actor.midbottom = (self.x + self.width / 2, self.hero_mid_y)
        self.bars = []

        self.update()

        equip_slot_size = 51
        self.weapon_slot = EquipSlot(self.screen, self.padding,
                                   self.x + padding, self.hero_mid_y - equip_slot_size,
                                   equip_slot_size, equip_slot_size, self.hero.weapon, self.hero)
        self.armor_slot = EquipSlot(self.screen, self.padding,
                                  self.x + self.width - equip_slot_size - padding, self.hero_mid_y - equip_slot_size,
                                  equip_slot_size, equip_slot_size, self.hero.armor, self.hero)

    def update(self):
        self.bars = []
        self.bars.append(
            HorBar(self.screen, self.x + 10, self.hero_mid_y + 25, 12, self.width - 20, self.hero.hp, self.hero.max_hp(), c_red))
        self.bars.append(
            HorBar(self.screen, self.x + 10, self.hero_mid_y + 40, 12, self.width - 20, self.hero.mp, self.hero.max_mp(), c_blue))

    def render(self):
        self.box.render()
        self.actor.draw()
        self.screen.draw.text(self.hero.name,
                              midtop=(self.x + self.width / 2, self.y + 105))
        for bar in self.bars:
            bar.render()

        # hero stats, column 1
        self.screen.draw.text(f"STR {self.hero.str}",
                              midtop=(self.x + self.width / 4, self.y + 125 + 4 * self.padding))
        self.screen.draw.text(f"DEX {self.hero.dex}",
                              midtop=(self.x + self.width / 4, self.y + 120 + 7 * self.padding))
        # hero stats, column 2
        self.screen.draw.text(f"CON {self.hero.con}",
                              midtop=(self.x + 3 * self.width / 4, self.y + 125 + 4 * self.padding))
        self.screen.draw.text(f"INT {self.hero.int}",
                              midtop=(self.x + 3 * self.width / 4, self.y + 120 + 7 * self.padding))

        # slots with the equipped weapon and armor:
        self.weapon_slot.render()
        self.armor_slot.render()


class EquipSlot:
    def __init__(self, screen, padding, x, y, width, height, item, hero):
        self.hero = hero
        self.box = Panel(screen, padding, x, y, width, height, False)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen = screen
        self.padding = padding
        self.item = item
        self.popup = None
        if self.item is not None:
                item.actor.center = (x + width / 2, y + height / 2)

    def open_popup(self, pos):
        self.popup = pos

    def close_popup(self):
        self.popup = None

    def center_actor(self):
        self.item.actor.center = (self.x + self.width / 2, self.y + self.height / 2)

    def render(self):
        self.box.render()
        if self.item is not None:
            self.item.actor.draw()
            if self.popup:
                p_size = 120
                x, y = self.popup
                # y -= p_size
                popup_background = Rect((x, y), (p_size, p_size))
                self.screen.draw.filled_rect(popup_background, c_white)
                self.screen.draw.text(self.item.name,
                                      midtop=(x + p_size / 2, y + self.padding),
                                      width=p_size - 2 * self.padding,
                                      fontsize=20, color=(20, 20, 20))
                if self.item.description is not None:
                    desc_text = self.item.description
                    if isinstance(self.item, Weapon):
                        desc_text += f"\n \nBase DMG: {self.item.dmg}"
                    self.screen.draw.text(desc_text,
                                          midtop=(x + p_size / 2, y + self.padding + 35),
                                          width=p_size - 2 * self.padding,
                                          fontsize=20, color=(40, 40, 40))


class InvSlot:
    def __init__(self, screen, padding, x, y, width, height, item):
        self.box = Panel(screen, padding, x, y, width, height, False)
        self.screen = screen
        self.padding = padding
        self.item = item
        self.popup = None
        if self.item is not None:
            if self.item.equipped is None:
                item.actor.center = (x + width / 2, y + height / 2)

    def open_popup(self, pos):
        self.popup = pos

    def close_popup(self):
        self.popup = None

    def render(self):
        self.box.render()
        if self.item is not None:
            if self.item.equipped is None:
                self.item.actor.draw()
                if self.popup:
                    p_size = 120
                    x, y = self.popup
                    y -= p_size
                    popup_background = Rect((x, y), (p_size, p_size))
                    self.screen.draw.filled_rect(popup_background, c_white)
                    self.screen.draw.text(self.item.name,
                                          midtop=(x + p_size / 2, y + self.padding),
                                          width=p_size - 2 * self.padding,
                                          fontsize=20, color=(20, 20, 20))
                    if self.item.description is not None:
                        desc_text = self.item.description
                        if isinstance(self.item, Weapon):
                            desc_text += f"\n \nBase DMG: {self.item.dmg}"
                        self.screen.draw.text(desc_text,
                                              midtop=(x + p_size / 2, y + self.padding + 20),
                                              width=p_size - 2 * self.padding,
                                              fontsize=20, color=(40, 40, 40))


class InventoryPanel:
    def __init__(self, screen, padding, x, y, width, height, inventory):
        self.box = Panel(screen, padding, x, y, width, height, False)
        self.x = x
        self.y = y
        self.screen = screen
        self.padding = padding
        self.slots = []

        self.cols, self.rows = 10, 3
        self.slot_width = (width - (self.cols + 1) * self.padding) / self.cols
        # slot_height = (height - (rows + 1) * padding) / rows
        self.slot_height = self.slot_width
        # print(slot_height)  # 51 px
        self.update(inventory)

    def update(self, inventory):
        self.slots = []
        # filtering out the items which are already equipped:
        inventory = [x for x in inventory if x.equipped is None]
        item_no = 0
        for row in range(self.rows):
            slot_y = self.y + self.padding + row * (self.padding + self.slot_height)
            for col in range(self.cols):
                slot_x = self.x + self.padding + col * (self.padding + self.slot_width)
                item = inventory[item_no] if item_no < len(inventory) else None

                self.slots.append(InvSlot(self.screen, self.padding, slot_x, slot_y,
                                          self.slot_width, self.slot_height, item))
                item_no += 1

    def render(self):
        self.box.render()
        for slot in self.slots:
            slot.render()


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

    def update(self, inventory):
        self.inv_panel.update(inventory)
        for p in self.hero_panels:
            p.update()
