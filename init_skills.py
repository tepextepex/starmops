from classes import Attack, Buff


def increase_hp(value, *targets):
    for target in targets:
        target.hp = target.hp + value if target.hp + value < target.max_hp() else target.max_hp()


def decrease_hp(value, *targets):
    for target in targets:
        target.hp = target.hp - value if target.hp - value > 0 else 0


def steal_mp(value, *targets):
    for target in targets:
        target.mp = 1


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

mana_steal = Attack("Steal the force", "Drains the target's MP completely",
              "low_battery", "single", True, "INT", 30, steal_mp)

piercing_shot = Attack("Piercing shot", "Attacks two targets at the same time",
                       "bullet", "column", True, "DEX", 50, decrease_hp)

nuke = Attack("Nuke", "Attacks all the enemies. Evaporate 'em all!",
              "nuke", "area", True, "DEX", 50, decrease_hp)

holy_grenade = Attack("Holy granade", "Pope's taken a bunch of these on a planet inhabited by antropomorphic worms",
                      "orb", "row", True, "INT", 40, decrease_hp)

band_aid = Buff("Heal", "Increases HP but just a little bit",
            "band", "single", 20, increase_hp)

heal = Buff("Heal", "Increases HP of one of your allies",
            "heart", "single", 30, increase_hp)

hold = Buff("Hold the floor!", "Makes the caster be a single target for all enemies. Lasts for one turn",
            "door", "self", 40, only_target)

revive = Buff("Revive", "The power of resurrection",
              "revive", "single", 40, revive_char)

rage = Attack("Rage", "150% attack on a single target",
              "convince", "single", False, "STR", 30, decrease_hp)
