# visual_tools.py
# Author: Yi Luo 20700131
# Date: May 2025
# Course: COMP4030 Designing Intelligent Agents

# Description:
# Generates visual summaries for the multi-agent cleaning simulation.
# Includes average performance plots, boxplots, and heatmaps.

# Attribution:
# - Built using pandas, matplotlib, and seaborn.
# - Plotting functions support the experiment analysis workflow.

# Usage:
# Import functions (e.g., plot_avg_dirt) or call save_all_charts().
# Requires 'results.csv' and 'visit_grid_bot{n}.npy' as input.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

RESULTS_CSV = "results.csv"
HEATMAP_DIR = "heatmap"
os.makedirs(HEATMAP_DIR, exist_ok=True)

col_names = ["strategy", "run", "dirt", "time"]
df = pd.read_csv(RESULTS_CSV, names=col_names) # Read experiment results with custom column names

print("[DEBUG] First few rows of results:")
print(df.head())


def plot_avg_dirt():
    """
    Plots the average dirt collected for each strategy, including standard deviation error bars.
    Saves the figure as 'avg_dirt.png'.
    """
    avg = df.groupby("strategy")["dirt"].mean()
    std = df.groupby("strategy")["dirt"].std()
    plt.figure(figsize=(8, 6))
    plt.bar(avg.index, avg, yerr=std, capsize=5, color="skyblue")
    plt.title("Average Dirt Collected per Strategy")
    plt.ylabel("Dirt Collected")
    plt.xlabel("Strategy")
    plt.tight_layout()
    plt.savefig("avg_dirt.png")
    plt.close()

def plot_avg_time():
    """
    Plots the average runtime for each strategy, with standard deviation shown as error bars.
    Saves the figure as 'avg_time.png'.
    """
    avg = df.groupby("strategy")["time"].mean()
    std = df.groupby("strategy")["time"].std()
    plt.figure(figsize=(8, 6))
    plt.bar(avg.index, avg, yerr=std, capsize=5, color="salmon")
    plt.title("Average Time per Strategy")
    plt.ylabel("Time (s)")
    plt.xlabel("Strategy")
    plt.tight_layout()
    plt.savefig("avg_time.png")
    plt.close()

def plot_boxplot_dirt():
    """
    Creates a boxplot to show the distribution of dirt collected across all runs.
    Saves the figure as 'boxplot_dirt.png'.
    """
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x="strategy", y="dirt", hue="strategy", palette="pastel")
    plt.title("Dirt Collection Distribution")
    plt.xlabel("Strategy")
    plt.ylabel("Dirt Collected")
    plt.tight_layout()
    plt.savefig("boxplot_dirt.png")
    plt.close()

def plot_heatmap_from_grid(bot_index):
    """
    Generates a heatmap from the visited grid of a specific robot.

    Parameters:
        visited_grid (np.ndarray): 2D array (10x10) recording cell visit counts.
        bot_index (int): Index of the robot, used in the plot title and filename.

    he heatmap is saved as 'heatmaps/heatmap_bot{n}.png'.
    """
    filename = f"visit_grid_bot{bot_index}.npy"
    print(f"[DEBUG] Looking for {filename}...")

    if not os.path.exists(filename):
        print(f"[WARNING] Heatmap file {filename} not found.")
        return
    visited_grid = np.load(filename)
    plt.figure(figsize=(6, 5))
    sns.heatmap(visited_grid, annot=False, cmap="OrRd", cbar=True)
    plt.title(f"Heatmap - Bot {bot_index}")
    plt.tight_layout()
    filename = os.path.join(HEATMAP_DIR, f"heatmap_bot{bot_index}.png")
    plt.savefig(filename)
    plt.close()

def export_summary():
    """
    Calculates the average and standard deviation of dirt collected and runtime by strategy.
    Outputs the results to 'results_summary.xlsx'.
    """
    avg = df.groupby("strategy")[["dirt", "time"]].mean()
    std = df.groupby("strategy")[["dirt", "time"]].std()
    summary = avg.copy()
    summary["dirt_std"] = std["dirt"]
    summary["time_std"] = std["time"]
    summary.to_excel("results_summary.xlsx")
    print("[INFO] Saved summary to results_summary.xlsx")

def save_all_charts():
    """
    Runs all plotting and export functions:
    - Bar charts for average dirt and time
    - Boxplot for dirt distribution
    - Heatmaps (if implemented)
    - Summary table export
    """
    print("[INFO] Generating all charts...")
    plot_avg_dirt()
    plot_avg_time()
    plot_boxplot_dirt()
    for i in range(3):
        plot_heatmap_from_grid(i)
    export_summary()
    print("[INFO] Charts saved as PNGs.")
