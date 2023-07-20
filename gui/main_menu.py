from pgzero.actor import Actor


class MainMenu:
    def __init__(self, WIDTH, HEIGHT):
        self.game_credits = """
            Created by Anton V. Terekhov using the ingenious
            Platformer Art Complete Pack by Kenney Vleugels (www.kenney.nl)
            and the Pygame Zero framework by Daniel Pope.
        """
        self.logo = Actor("menu_logo")

        self.menu_start = Actor("menu_start")
        self.menu_load = Actor("menu_load")
        self.menu_credits = Actor("menu_credits")

        x = WIDTH / 2
        self.logo.center = (x, HEIGHT / 3)

        self.menu_start.center = (x, HEIGHT / 2 + 40)
        self.menu_load.center = (x, HEIGHT / 2 + 80)
        self.menu_credits.center = (x, HEIGHT / 2 + 120)

    def render(self):
        self.logo.draw()
        self.menu_start.draw()
        self.menu_load.draw()
        self.menu_credits.draw()
