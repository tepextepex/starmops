from pgzero.actor import Actor
from pygame import Rect
from gui.base import c_red, c_blue, Panel
from gui.base import NextBtn
from gui.party_screen import InvSlot
from potion import RevivalPotion, HealingPotion, GreaterCider
from weapon import gen_weapon


class ResultScreen:
    def __init__(self, screen, padding, win, tier):
        self.screen = screen
        self.padding = padding
        self.blood = Actor("bloody_space")
        self.loot = []
        if win:
            self.win = True
            self.message = "Your party won the battle!"
            self.loot.append(gen_weapon(tier=tier))
            self.loot.append(RevivalPotion())
            self.loot.append(HealingPotion())
            self.loot.append(GreaterCider())
        else:
            self.win = False
            self.message = "Your party sucks."
            for i in range(3):
                self.loot.append(RevivalPotion())
                self.loot.append(HealingPotion())

        # creating slots with the looted items:
        self.loot_slots = []
        slot_size = 51
        loot_count = len(self.loot)
        x_start = (self.screen.width - slot_size * loot_count - self.padding * (loot_count - 1)) / 2
        for i, item in enumerate(self.loot):
            x = x_start + i * (slot_size + self.padding)
            y = self.screen.height / 2 + 20
            self.loot_slots.append(InvSlot(self.screen, self.padding,
                                           x, y, slot_size, slot_size, item))

        self.next_btn = NextBtn(self.screen, self.padding)

    def render(self):
        if not self.win:
            self.blood.draw()
        self.screen.draw.text(self.message,
                              center=(self.screen.width / 2, self.screen.height / 2))
        for s in self.loot_slots:
            s.render()

        self.next_btn.render()
