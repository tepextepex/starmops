from classes import Attack, Buff


def increase_hp(value, *targets):
    for target in targets:
        target.hp = target.hp + value if target.hp + value < target.max_hp() else target.max_hp()


def decrease_hp(value, *targets):
    for target in targets:
        target.hp = target.hp - value if target.hp - value > 0 else 0


def only_target(value, *targets):
    for target in targets:
        target.only_target = True


def revive_char(value, *targets):
    for target in targets:
        target.revive()


def stun_char(value, *targets):
    for target in targets:
        target.stun = True


melee_attack = Attack("Melee attack", "",
                      "melee_attack", "single", False, "STR", 0, decrease_hp)

ranged_attack = Attack("Ranged attack", "",
                       "raygun", "single", True, "DEX", 0, decrease_hp)

swing = Attack("Blood harvest", "Attacks the entire row",
               "scythe", "row", False, "DEX", 50, decrease_hp)

stun = Attack("Confuse", "Jebedi force makes the enemy skip a turn",
              "confuse", "single", True, "INT", 30, stun_char)

piercing_shot = Attack("Piercing shot", "Attacks two targets at the same time",
                       "bullet", "column", True, "DEX", 50, decrease_hp)

heal = Buff("Heal", "Increases HP of one of your allies",
            "heart", "single", 30, increase_hp)

hold = Buff("Hold the floor!", "Makes the caster be a single target for all enemies. Lasts for one turn",
            "door", "self", 40, only_target)

revive = Buff("Revive", "The power of resurrection",
              "revive", "single", 40, revive_char)

rage = Attack("Rage", "150% attack on a single target",
              "convince", "single", False, "STR", 30, decrease_hp)
