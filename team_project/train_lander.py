import gymnasium as gym
import numpy as np
import random

lander = {
    "altitude": 100.0,
    "velocity": 0.0,
    "fuel": 50
}

Gravity = -0.0057
Thrust_power = 0.02


def step_environment(action):

    if action == 1 and lander["fuel"] > 0:
        acceleration = Gravity + Thrust_power
        lander["fuel"] -= 1
    else:
        acceleration = Gravity

    lander["velocity"] += acceleration
    lander["altitude"] += lander["velocity"]


q_table = {
    "High_Falling": {0: 0.0, 1: 0.0},
    "High_Raising": {0: 0.0, 1: 0.0},
    "Low_Falling":  {0: 0.0, 1: 0.0},
    "Low_Rising":   {0: 0.0, 1: 0.0},
    "On_grounding": {0: 0.0, 1: 0.0}
}


def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.choice([0, 1])
    else:
        actions_available = q_table[state]

        if actions_available[1] > actions_available[0]:
            return 1
        else:
            return 0


alpha = 0.1
gamma = 0.9


def update_q_memory(state, action, reward, next_state):

    old_value = q_table[state][action]

    best_future_value = max(q_table[next_state].values())

    learned_target = reward + (gamma * best_future_value)

    q_table[state][action] = old_value + alpha * (learned_target - old_value)


def get_current_state(lander):
    if lander["altitude"] <= 0:
        return "On_grounding"

    is_high = lander["altitude"] > 50

    is_falling = lander["velocity"] < 0

    if is_high and is_falling:
        return "High_Falling"
    elif is_high and not is_falling:
        return "High_Raising"
    elif not is_high and is_falling:
        return "Low_Falling"
    else:
        return "Low_Rising"


episodes = 1000
epsilon = 0.8

for misson in range(1, episodes + 1):

    if misson % 50 == 0 or misson == 1:
        print(f"\n--- MISSON{misson} START ---")

    lander["altitude"] = 100.0
    lander["velocity"] = 0.0
    lander["fuel"] = 200

    misson_active = True
    while misson_active:

        current_state = get_current_state(lander)

        action = choose_action(current_state, epsilon)

        step_environment(action)

        next_state = get_current_state(lander)

        reward = 0
        if next_state == "On_grounding":
            misson_activate = False

            if lander["velocity"] > -0.5:
                reward = 100
                print(f"SUCCESS! Soft landing. fuel left: {lander['fuel']}")
            else:
                reward = -100
                # Add this temporary line to see the height live:
                print(
                    f"Height: {lander['altitude']:.2f} | Fuel: {lander['fuel']}")

        else:

            reward = -1

        update_q_memory(current_state, action, reward, next_state)

epsilon = max(0.01, epsilon * 0.995)

print("\nTraining Complete! Here is what the brain learned:")
print(q_table)
