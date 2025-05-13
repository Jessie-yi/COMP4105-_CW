#COMP4105 Designing Intelligent Agents Coursework
---

## Overview

This project simulates multiple vacuum robots operating in a 2D grid using three strategies:

- **Baseline** – Independent A* path planning  
- **Shared Map** – Agents merge local dirt maps  
- **Coordination** – Adds proximity-based avoidance on top of shared maps  

Each run logs dirt collected and runtime. Results are analysed using CSV summaries and visualised with heatmaps and bar charts.

---

## How to Run

### Requirements

- Python 3.8+
- Libraries: `numpy`, `matplotlib`, `pandas`, `seaborn`, `tkinter`

### Commands  
- **Run batch experiments**:  
  ```bash
  python batch_runner.py
````

* **Run GUI simulation**:

  ```bash
  python multi_robot_coordination_experiment.py
  ```

---

## Included Files

* `multi_robot_coordination_experiment.py`
* `batch_runner.py`
* `aStar.py`
* `visual_tools.py`
* `results.csv` / `results_summary.xlsx`
* `demo/demo.mp4`
* `README.md`

---

## Notes

* A\* logic is adapted from course material (`aStar.py`).
* Strategy logic, coordination, visualisation, and CSV/export functions were developed for this project.
* Demo video and results are included for reference.
