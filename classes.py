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
        self.skills = []
        self.hp = self.max_hp()
        self.mp = self.max_mp()
        self.only_target = False  # TODO: how to unset this option?
        self.stun = False
        self.dead = False

    def remove_effects(self):
        self.only_target = False
        self.stun = False

    def kill(self):
        self.hp = 0
        self.dead = True
        self.remove_effects()
        self.actor.image = f"{self.image_base}_duck"

    def revive(self):
        self.hp = self.max_hp() / 4
        self.dead = False
        self.actor.image = self.image_base

    def max_hp(self):
        return self.con * 10 + 50

    def max_mp(self):
        return self.int * 10

    def set_jump(self):
        self.state = "jump"
        self.actor.image = f"{self.image_base}_jump"
        sounds.eep.play()

    def set_stand(self):
        self.state = "stand"
        self.actor.image = self.image_base
        sounds.eep.play()

    def funny_jump(self):
        if not self.dead:
            self.set_jump()
            clock.schedule_unique(self.set_stand, 0.1)

    def learn(self, *skills):
        for skill in skills:
            self.skills.append(skill)

    def equip_weapon(self, weapon):
        self.weapon = weapon
        weapon.equipped = self

    def equip_armor(self, armor):
        self.armor = armor
        armor.equipped = self

    def __repr__(self):
        return f"{self.name}"


class Skill:
    def __init__(self, target, name, description, image, aim, ranged, uses, mp_cost, effect):
        self.target = target  # friend or foe
        self.name = name
        self.description = description
        self.image = image
        self.actor = Actor(image)
        self.aim = aim  # number of affected slots (single | row | column | area | self)
        self.ranged = ranged
        self.uses = uses  # STR / DEX / INT
        self.mp_cost = mp_cost
        self.effect = effect  # should be a function to apply on target Char

    def affect_target(self, value, *targets):
        self.effect(value, *targets)
        for t in targets:
            if t.hp == 0:
                t.kill()

    def __repr__(self):
        return f"{self.name}"


class Attack(Skill):
    def __init__(self, name, description, image, aim, ranged, uses, mp_cost, effect):
        Skill.__init__(self, "foe", name, description, image, aim, ranged, uses, mp_cost, effect)


class Buff(Skill):
    def __init__(self, name, description, image, aim, mp_cost, effect):
        # buffs are always ranged and use INT:
        Skill.__init__(self, "friend", name, description, image, aim, True, "INT", mp_cost, effect)
