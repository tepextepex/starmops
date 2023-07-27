from pygame import Rect
from gui.base import c_red, c_blue, Panel
from gui.base import NextBtn


class ResultScreen:
    def __init__(self, screen, padding, win):
        self.screen = screen
        self.padding = padding
        if win:
            self.message = "Your party won the battle!"
        else:
            self.message = "Your party sucks."

        self.next_btn = NextBtn(self.screen, self.padding)

    def render(self):
        self.screen.draw.text(self.message,
                              center=(self.screen.width / 2, self.screen.height / 2))
        self.next_btn.render()
