from pygame import Rect
from gui.base import c_red, c_blue, Panel
from gui.base import NextBtn
from potion import RevivalPotion, HealingPotion, GreaterCider
from weapon import gen_weapon


class ResultScreen:
    def __init__(self, screen, padding, win, tier):
        self.screen = screen
        self.padding = padding
        self.loot = []
        if win:
            self.message = "Your party won the battle!"
            self.loot.append(gen_weapon(tier=tier))
            self.loot.append(RevivalPotion())
            self.loot.append(HealingPotion())
            self.loot.append(GreaterCider())
        else:
            self.message = "Your party sucks."
            for i in range(3):
                self.loot.append(RevivalPotion())
                self.loot.append(HealingPotion())

        self.next_btn = NextBtn(self.screen, self.padding)
        print(self.loot)

    def render(self):
        self.screen.draw.text(self.message,
                              center=(self.screen.width / 2, self.screen.height / 2))
        self.next_btn.render()
