import gymnasium as gym
import numpy as np
import random

drone = {
    "altitude": 100.0,
    "velocity": 0.0,
    "battery": 100
}

Gravity = 9.8
left_button = 59.3
right_button = 59.3
Thrust_power = 0.06


def step_environment(action):

    if action == 1 and ["battery"] > 0:
        acceleration = Gravity + right_button + left_button + Thrust_power
        drone["battery"] = -1
    else:
        acceleration = Gravity

    drone["velocity"] += acceleration
    drone["altitude"] += drone["velocity"]


q_table = {
    "High_falling": {0: 0.0, 1: 0.0},
    "High_Rasing": {0: 0.0, 1: 0.0},
    "Low_falling": {0: 0.0, 1: 0.0},
    "Low_raising": {0: 0.0, 1: 0.0},
    "On_grounding": {0: 0.0, 1: 0.0},
    "far_left": {0: 0.0, 1: 0.0},
    "far_right": {0: 0.0, 1: 0.0},
    "center": {0: 0.0, 1: 0.0}
}
