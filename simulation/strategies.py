from random import choice

def always_cooperate():
    return "cooperate"

def always_defect():
    return "defect"

def tit_for_tat(history):
    if not history:
        return "cooperate"
    return history[-1][1]  # Cooperate if the opponent cooperated last time

def random_strategy():
    return choice(["cooperate", "defect"])

strategy_funcs = {
    'always_cooperate': always_cooperate,
    'always_defect': always_defect,
    'tit_for_tat': tit_for_tat,
    'random_strategy': random_strategy,
}
