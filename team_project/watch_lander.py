import gymnasium as gym
from stable_baselines3 import PPO

# Load the environment with rendering enabled
env = gym.make("LunarLander-v3", continuous=True, render_mode="human")

# Load our trained AI
model = PPO.load("lunar_lander_agent")

# Run a test flight
obs, info = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        print("Flight ended. Resetting...")
        obs, info = env.reset()

env.close()
