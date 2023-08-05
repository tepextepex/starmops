from pgzero.actor import Actor
from pgzero.clock import clock
from pgzero.loaders import sounds

from random import choices, seed


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


class Armor:
    def __init__(self, type, name, image, defence):
        self.type = type
        self.name = name
        self.image = image
        self.actor = Actor(image)
        self.defence = defence
        self.equipped = None
        self.description = None


class Potion:
    def __init__(self, name, description, image, effect):
        self.name = name
        self.description = description
        self.actor = Actor(image)
        self.effect = effect
        self.equipped = None  # potions can't be equipped

    def apply(self, target):
        self.effect(target)


class HealingPotion(Potion):
    def __init__(self):
        def effect(target):
            new_hp = target.hp + target.max_hp() * 0.666
            target.hp = new_hp if new_hp < target.max_hp() else target.max_hp()
        Potion.__init__(self, "Healing potion", "Increases HP for 66.6%. Hail Satan!",
                        "healing_vial", effect)


class LesserCider(Potion):
    def __init__(self):
        def effect(target):
            new_mp = target.mp + target.max_mp() * 0.50
            target.mp = new_mp if new_mp < target.max_mp() else target.max_mp()
        Potion.__init__(self, "Cider", "Increases MP but not too much (+50%). This bottle is way too small!",
                        "lesser_cider", effect)


class GreaterCider(Potion):
    def __init__(self):
        def effect(target):
            target.mp = target.max_mp()
        Potion.__init__(self, "Greater cider", "Fully replenishes your MP (+100%). Down the hatch, son.",
                        "greater_cider", effect)


class RevivalPotion(Potion):
    def __init__(self):
        def effect(target):
            target.revive()
        Potion.__init__(self, "Revival goo", "Revives a dead character. It is obvious! Can't you see that skull on the label?",
                        "poison", effect)


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
