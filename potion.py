from pgzero.actor import Actor


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
