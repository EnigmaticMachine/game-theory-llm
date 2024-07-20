from random import choice
import itertools
import random


def always_cooperate(*args, **kwargs):
    return "cooperate"


def always_defect(*args, **kwargs):
    return "defect"


def tit_for_tat(history):
    if not history:
        return "cooperate"  # Default action if no history is available
    else:
        return history[-1]


def friedman(history):
    if history and "defect" in history:
        return "defect"
    return "cooperate"


def joss(history, defection_probability=0.1):
    if history and history[-1] == "defect":
        return "defect"
    if random.random() < defection_probability:
        return "defect"
    return "cooperate"


def graaskamp(history, probe_round=50):
    if len(history) == probe_round:
        return "defect"  # Probe the opponent's strategy
    return joss(history)  # Behave like Joss otherwise


def tit_for_two_tats(history):
    if len(history) >= 2 and history[-1] == "defect" and history[-2] == "defect":
        return "defect"
    return "cooperate"


def random_strategy(*args, **kwargs):
    return choice(["cooperate", "defect"])


def soft_majority(history):
    if not history:
        return "cooperate"
    cooperations = history.count("cooperate")
    defections = history.count("defect")
    return "cooperate" if cooperations >= defections else "defect"


def generous_tit_for_tat(history, generosity=0.1):
    if not history:
        return "cooperate"
    if history[-1] == "defect" and random.random() > generosity:
        return "defect"
    return "cooperate"


def suspicious_tit_for_tat(history):
    if not history:
        return "defect"
    return history[-1]


def gradual(history):
    defections = history.count("defect")
    if defections == 0:
        return "cooperate"
    if len(history) - len(history.rstrip("cooperate")) == defections:
        return "cooperate"
    return "defect"


strategy_funcs = {
    "always_cooperate": always_cooperate,
    "always_defect": always_defect,
    "tit_for_tat": tit_for_tat,
    "friedman": friedman,
    "joss": joss,
    "graaskamp": graaskamp,
    "tit_for_two_tats": tit_for_two_tats,
    "random_strategy": random_strategy,
    "soft_majority": soft_majority,
    "generous_tit_for_tat": generous_tit_for_tat,
    "suspicious_tit_for_tat": suspicious_tit_for_tat,
}
