from pygame import Rect

from gui.base import c_red, c_blue, Panel, NextBtn


###########################################
### GUI panels for the party selection  ###
###########################################


class SelectionScreen:
    def __init__(self, screen, padding, chars):
        self.screen = screen
        self.chars = chars

        for i, a in enumerate(chars):
            x = 95 + 100 * i + 33
            y = 190
            a.actor.midbottom = x, y

        self.desc_text = "Select your party. You can choose three members"
        self.next_btn = NextBtn(self.screen, padding)

    def update_desc(self, new_desc):
        self.desc_text = new_desc

    def render(self, party):
        for c in self.chars:
            c.actor.draw()
            p = c.actor.midbottom
            self.screen.draw.text(c.name, midtop=(p[0], p[1] + 10))

        self.screen.draw.text(self.desc_text,
                              center=(self.screen.width / 2, self.screen.height / 2 + 80),
                              width=500)
        if len(party) == 3:
            self.next_btn.render()
