# batch_runner.py
# Author: Yi Luo 20700131
# Date: May 2025
# Course: COMP4030 Designing Intelligent Agents

# Description:
# Runs simulations for baseline, shared_map, and coordination strategies.
# Ensures consistent experimental parameters and logs results to a CSV file.

# Uses run_experiment() from multi_robot_coordination_experiment.py and visual_tools.py for plotting.

from multi_robot_coordination_experiment import (
    run_experiment,
    STRATEGY_BASELINE,
    STRATEGY_SHARED_MAP,
    STRATEGY_COORDINATION
)
from visual_tools import save_all_charts

# Configuration Parameters
NUM_RUNS = 10           # Number of runs per strategy
NUM_BOTS = 3            # Number of robots in each run
NUM_DIRT = 40           # Number of dirt patches to clean
MAX_STEPS = 1000        # Maximum steps per simulation

# List of strategies to evaluate
strategies = [
    STRATEGY_BASELINE,
    STRATEGY_SHARED_MAP,
    STRATEGY_COORDINATION
]

# Main Execution Loop
if __name__ == "__main__":
    # Run experiments for each strategy
    for strategy in strategies:
        print(f"Running strategy: {strategy}")
        for run_id in range(NUM_RUNS):
            print(f"  Run #{run_id + 1}...")
            # Run a single experiment in headless mode (no GUI), opposite if headless=False
            run_experiment(
                strategy=strategy,
                run_id=run_id,
                num_bots=NUM_BOTS,
                num_dirt=NUM_DIRT,
                max_steps=MAX_STEPS,
                headless=True
            )
    # After all experiments, generate summary charts
    print("\nAll experiments complete. Generating summary plot...")
    save_all_charts()
    print("Done!")


