from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.loaders import sounds


class Char:
    def __init__(self, name, image_base, desc, stg, dex, con, ing):
        self.name = name
        self.state = "stand"
        self.image_base = image_base
        self.desc = desc
        self.actor = Actor(image_base)
        self.badge = Actor(f"{self.image_base}_badge1")
        self.str = stg
        self.dex = dex
        self.con = con
        self.int = ing
        self.weapon = None
        self.armor = None
        self.slot_no = None

    def max_hp(self):
        return self.con * 10 + 50

    def max_mp(self):
        return self.int + 10

    def set_jump(self):
        self.state = "jump"
        self.actor.image = f"{self.image_base}_jump"
        sounds.eep.play()

    def set_stand(self):
        self.state = "stand"
        self.actor.image = self.image_base
        sounds.eep.play()

    def funny_jump(self):
        self.set_jump()
        clock.schedule_unique(self.set_stand, 0.1)

    def __repr__(self):
        return f"{self.name}"


class Weapon:
    def __init__(self, type, name, image, attack):
        self.type = type
        self.name = name
        self.image = image
        self.actor = Actor(image)
        self.attack = attack


class Armor:
    def __init__(self, type, name, image, defence):
        self.type = type
        self.name = name
        self.image = image
        self.actor = Actor(image)
        self.defence = defence