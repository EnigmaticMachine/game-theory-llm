import sys
import itertools
import pandas as pd
from statistics import mean
from strategies import strategy_funcs
from constants import rewards


def simulate_round(strategy1, strategy2, history1=[], history2=[]):
    action1 = strategy1(history2)
    action2 = strategy2(history1)
    history1.append(action1)
    history2.append(action2)

    if action1 == "cooperate" and action2 == "cooperate":
        return (rewards["both_cooperate"], rewards["both_cooperate"])
    elif action1 == "defect" and action2 == "defect":
        return (rewards["both_defect"], rewards["both_defect"])
    elif action1 == "cooperate" and action2 == "defect":
        return (rewards["cooperate_defect"], rewards["defect_cooperate"])
    elif action1 == "defect" and action2 == "cooperate":
        return (rewards["defect_cooperate"], rewards["cooperate_defect"])


def run_simulation(strategy1, strategy2, rounds=100):
    total_rewards = [0, 0]
    history1, history2 = [], []

    for _ in range(rounds):
        reward1, reward2 = simulate_round(
            strategy_funcs[strategy1], strategy_funcs[strategy2], history1, history2
        )
        total_rewards[0] += reward1
        total_rewards[1] += reward2
    return total_rewards


def simulate_all():
    strategies = list(strategy_funcs.keys())

    columns = ["strategy_1", "strategy_2", "result_1", "result_2", "winner"]
    df = pd.DataFrame(columns=columns)

    strategies_pairs = get_all_pairs(strategies)
    results = {}
    for pair in strategies_pairs:
        df_row = pd.DataFrame(columns=columns)

        result = run_simulation(pair[0], pair[1], rounds=20)
        if result[0] > result[1]:
            winner = pair[0]
        elif result[0] == result[1]:
            winner = None
        else:
            winner = pair[1]
        results[pair] = {"result": result, "winner": winner}
        df_row = pd.DataFrame(
            {
                "strategy_1": [pair[0]],
                "strategy_2": [pair[1]],
                "result_1": [result[0]],
                "result_2": [result[1]],
                "winner": [winner],
            }
        )

        df = pd.concat([df, df_row], axis=0)

    return df


def get_all_pairs(strategies):
    return list(itertools.combinations(strategies, 2))


def analyze_results(df):

    # To calculate average scores
    df["result_1"] = pd.to_numeric(df["result_1"])
    df["result_2"] = pd.to_numeric(df["result_2"])

    # Combine the strategies and results into a single series for easier manipulation
    results_1 = df[["strategy_1", "result_1"]].rename(
        columns={"strategy_1": "strategy", "result_1": "score"}
    )
    results_2 = df[["strategy_2", "result_2"]].rename(
        columns={"strategy_2": "strategy", "result_2": "score"}
    )
    combined_results = pd.concat([results_1, results_2])

    # Compute the average score per strategy
    average_scores = combined_results.groupby("strategy")["score"].mean().reset_index()
    average_scores.columns = ["strategy", "average_score"]

    # Count the wins per strategy
    total_wins = df["winner"].value_counts().reset_index()
    total_wins.columns = ["strategy", "total_wins"]

    # Merging average scores and total wins
    analysis = pd.merge(average_scores, total_wins, on="strategy", how="left").fillna(0)
    analysis["total_wins"] = analysis["total_wins"].astype(int)

    analysis_sorted = analysis.sort_values(by="average_score", ascending=False)

    print(analysis_sorted)


def print_analysis(analysis):
    print("\nStrategy Analysis:")
    print("-" * 70)
    print(f"{'Strategy':<20} {'Avg Score':<15} {'Win Rate':<15} {'Total Wins':<10}")
    print("-" * 70)
    for entry in analysis:
        print(
            f"{entry['strategy']:<20} {entry['average_score']:<15.2f} {entry['win_rate']:<15.2f}% {entry['total_wins']:<10}"
        )


if __name__ == "__main__":
    args = sys.argv[1:]

    all_results = simulate_all()
    analysis = analyze_results(all_results)
    # print_analysis(analysis)
