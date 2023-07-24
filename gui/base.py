from pygame import Rect
from pgzero.actor import Actor

c_white = (255, 255, 255, 128)
c_red = (255, 87, 51)
c_green = (76, 187, 23)
c_blue = (117, 194, 246)


class NextBtn:
    def __init__(self, screen, padding):
        self.actor = Actor("arrow_green")
        self.actor.bottomright = screen.width - 2 * padding, screen.height

    def render(self):
        self.actor.draw()


class Panel:
    def __init__(self, screen, padding, x, y, w, h, active=False):
        self.screen = screen
        self.padding = padding
        if active:
            self.c = c_green
            self.active = True
        else:
            self.c = c_white
            self.active = False

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.box = Rect((self.x, self.y), (self.w, self.h))

    def set_active(self):
        self.active = True
        self.c = c_green
        # self.box = Rect((self.x, self.y), (self.w, self.h))

    def set_normal(self):
        self.active = False
        self.c = c_white
        # self.box = Rect((self.x, self.y), (self.w, self.h))

    def set_target(self):
        self.c = c_red

    def set_untarget(self):
        if self.active:
            self.c = c_green
        else:
            self.c = c_white

    def render(self):
        self.box = Rect((self.x, self.y), (self.w, self.h))
        self.screen.draw.rect(self.box, self.c)
