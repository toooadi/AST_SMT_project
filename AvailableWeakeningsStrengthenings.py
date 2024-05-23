from transformations.strengthening import StrengthenEquals, StrengthenLess, StrengthenLessEquals, StrengthenNotEquals
from transformations.weakening import WeakenEquals, WeakenLess, WeakenLessEquals, WeakenNotEquals

STRENGTHEN = [
    StrengthenEquals.StrengthenEquals(),
    StrengthenLess.StrengthenLess(),
    StrengthenLessEquals.StrengthenLessEquals(),
    StrengthenNotEquals.StrengthenNotEquals()
    ]

WEAKEN = [
    WeakenEquals.WeakenEquals(),
    WeakenLess.WeakenLess(),
    WeakenLessEquals.WeakenLessEquals(),
    WeakenNotEquals.WeakenNotEquals()
]