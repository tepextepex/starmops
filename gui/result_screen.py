from pygame import Rect
from gui.base import c_red, c_blue, Panel


class ResultScreen:
    def __init__(self, screen, win):
        self.screen = screen
        if win:
            self.message = "Your party won the battle!"
        else:
            self.message = "Your party sucks."

    def render(self):
        self.screen.draw.text(self.message,
                              center=(self.screen.width / 2, self.screen.height / 2))
