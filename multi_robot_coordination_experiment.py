# multi_robot_coordination_experiment.py
# Author: Yi Luo 20700131
# Date: May 2025
# Course: COMP4030 Designing Intelligent Agents

# Description:
# Defines a 2D grid environment for testing multi-agent vacuuming strategies.
# Agents clean randomly placed dirt using one of three strategies:
# 1. Baseline – independent A* planning.
# 2. Shared Map – local perceptions are merged.
# 3. Coordination – shared maps plus proximity-based avoidance.

# Supports both GUI (Tkinter) and headless modes.
# Results are logged to CSV and visualized externally.

# Attribution:
# - Movement logic based on simpleBot4.py (course material).
# - A* pathfinding from aStar.py (template).
# - Coordination, shared state, batch control, and visual output designed by the author.

import tkinter as tk
import random
import math
import numpy as np
import csv
import time
from aStar import aStarSearch

# Available strategy identifiers for controlling agent behavior
STRATEGY_BASELINE = "baseline" # No communication between agents
STRATEGY_SHARED_MAP = "shared_map" # Agents merge perceived dirt into a shared global map
STRATEGY_COORDINATION = "coordination" # Agents coordinate based on proximity

# Shared map for dirt perception (only used in shared and coordination strategies)
shared_map = np.zeros((10, 10), dtype=np.int16)

class Counter:
    def __init__(self):
        self.dirt_collected = 0
        self.start_time = time.time()

    def collect(self):
        self.dirt_collected += 1

class Brain:
    def __init__(self, bot, all_agents, strategy):
        self.bot = bot
        self.agents = all_agents
        self.strategy = strategy
        local_map = self.bot.scan_dirt_map()

        # My logic: use shared map when strategy requires
        self.map = local_map if strategy == STRATEGY_BASELINE else (shared_map | local_map)
        self.path = aStarSearch(self.map) or []
        self.path_index = 0

    def check_proximity(self, threshold=100):
        for other in self.agents:
            if other is not self.bot:
                dist = math.hypot(self.bot.x - other.x, self.bot.y - other.y)
                if dist < threshold:
                    return True, other
        return False, None

    # Compute wheel speeds based on current path and strategy
    def think(self):
        if self.strategy == STRATEGY_COORDINATION:
            too_close, other = self.check_proximity()
            if too_close:
                angle = math.atan2(self.bot.y - other.y, self.bot.x - other.x)
                self.bot.theta = angle + math.pi
                return -2.0, 2.0, None, None

        if self.path_index < len(self.path):
            tx, ty = self.path[self.path_index][1]*100 + 50, self.path[self.path_index][0]*100 + 50
            dx, dy = tx - self.bot.x, ty - self.bot.y
            angle_to_target = math.atan2(dy, dx)
            angle_diff = (angle_to_target - self.bot.theta + math.pi) % (2 * math.pi) - math.pi

            if abs(angle_diff) > 0.2:
                sl, sr = -2.0, 2.0
            else:
                sl = sr = 5.0

            if math.hypot(dx, dy) < 80:
                self.path_index += 1
        else:
            sl = sr = 0.0

        return sl, sr, None, None

# Based on course code: simpleBot4 (bot and dirt structure)
class Bot:
    def __init__(self, name, passive_objects, counter):
        self.name = name
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 700)
        self.theta = random.uniform(0, 2*math.pi)
        self.ll = 60
        self.sl = self.sr = 0.0
        self.passive_objects = passive_objects
        self.counter = counter
        self.visit_grid = np.zeros((10, 10), dtype=np.int32) # Heatmap data？

    def scan_dirt_map(self):
        m = np.zeros((10, 10), dtype=np.int16)
        for obj in self.passive_objects:
            if isinstance(obj, Dirt):
                gx, gy = int(obj.centreX // 100), int(obj.centreY // 100)
                m[gy][gx] += 1
        return m

    def set_brain(self, brain):
        self.brain = brain

    def act(self):
        self.sl, self.sr, new_x, new_y = self.brain.think()
        if new_x is not None: self.x = new_x
        if new_y is not None: self.y = new_y

    # Move the robot and update the visit map
    def update(self, canvas, dt):
        self.move(canvas, dt)
        gx, gy = int(self.x // 100), int(self.y // 100)
        if 0 <= gx < 10 and 0 <= gy < 10:
            self.visit_grid[gy][gx] += 1

    # Detect and remove nearby dirt if within cleaning range
    def collect_nearby_dirt(self, canvas):
        collected = False
        for dirt in self.passive_objects[:]:
            dx = self.x - dirt.centreX
            dy = self.y - dirt.centreY
            distance = math.hypot(dx, dy)
            if distance < 20:
                if canvas is not None:
                    canvas.delete(dirt.name)
                self.passive_objects.remove(dirt)
                self.counter.collect()
                print(
                    f"[INFO] {self.name} collected dirt at ({int(dirt.centreX)}, {int(dirt.centreY)}) | Total: {self.counter.dirt_collected}")
                collected = True
                break  # Clean one each time
        return collected

    def move(self, canvas, dt):
        # Based on class code: differential drive robot motion using ICC (Instantaneous Center of Curvature)
        if self.sl == self.sr: R = 0
        else: R = (self.ll / 2.0) * ((self.sr + self.sl) / (self.sl - self.sr))
        omega = (self.sl - self.sr) / self.ll
        ICCx = self.x - R * math.sin(self.theta)
        ICCy = self.y + R * math.cos(self.theta)

        m = np.array([[math.cos(omega*dt), -math.sin(omega*dt), 0],
                      [math.sin(omega*dt),  math.cos(omega*dt), 0],
                      [0, 0, 1]])
        v1 = np.array([[self.x - ICCx], [self.y - ICCy], [self.theta]])
        v2 = np.array([[ICCx], [ICCy], [omega*dt]])
        newv = m @ v1 + v2

        self.x, self.y = newv[0, 0], newv[1, 0]
        self.theta = newv[2, 0] % (2*math.pi)

        if self.sl == self.sr:
            self.x += self.sr * math.cos(self.theta)
            self.y += self.sr * math.sin(self.theta)

        if canvas:
            canvas.delete(self.name)
            self.draw(canvas)

    def draw(self, canvas):
        fill_color = {"bot0": "blue", "bot1": "red", "bot2": "green"}.get(self.name, "black")
        canvas.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill=fill_color, tags=self.name)

class Dirt:
    def __init__(self, x, y, name):
        self.centreX = x
        self.centreY = y
        self.name = name

    def get_location(self):
        return self.centreX, self.centreY

# CSV logging function
def log_result(strategy, run_id, dirt_collected, elapsed_time):
    with open("results.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([strategy, run_id, dirt_collected, round(elapsed_time, 2)])

# GUI experiment runner
def run_experiment(strategy, run_id, num_bots=3, num_dirt=40, max_steps=1000, headless=False):
    global shared_map
    shared_map = np.zeros((10, 10), dtype=np.int16)
    counter = Counter()
    agents = []
    dirt_list = []

    if not headless:
        root = tk.Tk()
        canvas = tk.Canvas(root, width=1000, height=1000, bg="white")
        canvas.pack()
    else:
        root = None
        canvas = None

    # Place dirt objects randomly within the grid
    for i in range(num_dirt):
        x, y = random.randint(50, 950), random.randint(50, 950)
        dirt = Dirt(x, y, f"dirt{i}")
        dirt_list.append(dirt)
        if canvas:
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="gray", tags=dirt.name)

    # Create robots and attach strategy-specific controllers
    for i in range(num_bots):
        bot = Bot(f"bot{i}", dirt_list, counter)
        brain = Brain(bot, agents, strategy)
        bot.set_brain(brain)
        agents.append(bot)

    step = 0

    def loop():
        nonlocal step
        if canvas:
            canvas.delete("bot")
            canvas.delete("dirt")
            for d in dirt_list:
                canvas.create_oval(d.centreX - 5, d.centreY - 5, d.centreX + 5, d.centreY + 5, fill="gray", tags="dirt")

        for bot in agents:
            bot.act()
            bot.update(canvas, 0.1)
            bot.collect_nearby_dirt(canvas)

        if canvas is not None:
            canvas.delete("status_text")
            canvas.create_text(500, 20, text=f"Dirt Collected: {counter.dirt_collected}", fill="black",
                               font=("Arial", 16), tags="status_text" )
        print(f"[DEBUG] Dirt collected so far: {counter.dirt_collected}")

        step += 1
        if step < max_steps:
            if root:
                root.after(30, loop)
            else:
                loop()
        else:
            log_result(strategy, run_id, counter.dirt_collected, time.time() - counter.start_time)
            for i, bot in enumerate(agents):
                np.save(f"visit_grid_bot{i}.npy", bot.visit_grid)
                print(f"[INFO] visit_grid_bot{i}.npy saved.")
            if not headless and root is not None:
                root.destroy()

    if headless:
        while step < max_steps:
            loop()
    else:
        root.after(100, loop)
        root.mainloop()