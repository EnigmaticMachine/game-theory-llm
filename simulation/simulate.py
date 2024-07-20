from strategies import strategy_funcs
from constants import rewards

def simulate_round(strategy1, strategy2):
    action1 = strategy1()
    action2 = strategy2()
    outcome = (action1, action2)

    if outcome == ("cooperate", "cooperate"):
        return rewards["both_cooperate"], rewards["both_cooperate"]
    elif outcome == ("defect", "defect"):
        return rewards["both_defect"], rewards["both_defect"]
    elif outcome == ("cooperate", "defect"):
        return rewards["cooperate_defect"], rewards["defect_cooperate"]
    elif outcome == ("defect", "cooperate"):
        return rewards["defect_cooperate"], rewards["cooperate_defect"]

def run_simulation(strategy1, strategy2, rounds=100):
    total_rewards = [0, 0]

    for _ in range(rounds):
        reward1, reward2 = simulate_round(strategy_funcs[strategy1], strategy_funcs[strategy2])
        total_rewards[0] += reward1
        total_rewards[1] += reward2

    return total_rewards

if __name__ == "__main__":
    # Example of how to run a simulation
    strategy1 = 'always_cooperate'
    strategy2 = 'always_defect'
    results = run_simulation(strategy1, strategy2)
    print(f"Results: {strategy1} vs {strategy2} -> {results}")
