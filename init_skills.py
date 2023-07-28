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


melee_attack = Attack("Melee attack", "",
                      "melee_attack", "single", False, "STR", 0, decrease_hp)

ranged_attack = Attack("Ranged attack", "",
                       "raygun", "single", True, "DEX", 0, decrease_hp)

swing = Attack("Swing", "",
               "saxophone", "row", False, "DEX", 50, decrease_hp)

piercing_shot = Attack("Piercing shot", "",
                       "bullet", "column", True, "DEX", 50, decrease_hp)

heal = Buff("Heal", "",
            "heart", "single", 30, increase_hp)

hold = Buff("Hold the floor!", "",
            "shield_bronze", "self", 40, only_target)

rage = Attack("Rage", "",
              "angry_cat", "single", False, "STR", 50, decrease_hp)
