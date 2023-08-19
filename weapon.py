from random import seed, choices, choice

from pgzero.actor import Actor


def gen_weapon(tier=0):
    w = [Chainsaw(tier=tier), LaserSaber(tier=tier), RayGun(tier=tier), MagicWand(tier=tier)]
    seed()
    return choice(w)


class Weapon:
    def __init__(self, type, name, description, image, dmg, tier=0):
        self.type = type
        self.tier = tier
        # self.name = name
        self.name = f"{self.name_prefix()} {name}"
        self.description = description
        self.image = image
        self.actor = Actor(image)
        if self.tier is None:
            self.dmg = dmg
        else:
            self.dmg = self.random_damage()
        self.equipped = None

    def name_prefix(self):
        line_no = self.tier if self.tier <= 39 else 39
        with open("random/xbzht") as fp:
            for i, line in enumerate(fp):
                if i == line_no:
                    print(line.rstrip())
                    return line.rstrip()  # eliminates all the trailing whitespaces including newline chars

    def random_damage(self):
        min_dmg = 10 + self.tier * 3
        weights = (10, 20, 40, 20, 10)
        seed()
        dmg = choices(
            range(min_dmg, min_dmg + 5),
            weights
        )
        return dmg[0]


class Chainsaw(Weapon):
    def __init__(self, tier=0):
        t = "melee"
        name = "Chainsaw"  # TODO: generate names according to the tier
        description = "Uses STR for melee attacks"
        image = "chainsaw"
        Weapon.__init__(self, t, name, description, image, None, tier)


class LaserSaber(Weapon):
    def __init__(self, tier=0):
        t = "melee"
        name = "Lasersaber"  # TODO: generate names according to the tier
        description = "Uses DEX for melee attacks"
        image = "lasersaber"
        Weapon.__init__(self, t, name, description, image, None, tier)


class RayGun(Weapon):
    def __init__(self, tier=0):
        t = "ranged"
        name = "Raygun"  # TODO: generate names according to the tier
        description = "Uses DEX to attack"
        image = "blaster"
        Weapon.__init__(self, t, name, description, image, None, tier)


class MagicWand(Weapon):
    def __init__(self, tier=0):
        t = "ranged"
        name = "Magic Wand"  # TODO: generate names according to the tier
        description = "Uses INT to attack"
        image = "plunger"
        Weapon.__init__(self, t, name, description, image, None, tier)
