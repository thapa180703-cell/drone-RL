"""Q-learning agent for F2 class-based starter."""

import random

import matplotlib.pyplot as plt
import numpy as np


class QLearningAgent:
    def __init__(self, env, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.env = env
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((env.size[0], env.size[1], len(env.actions)))
        self.actions = env.actions

        # Episode records for learning curve visualization
        self.episode_rewards = []
        self.episode_steps = []

    def choose_action(self, state):
        """Use epsilon-greedy policy to select an action."""
        if random.random() < self.epsilon:
            return random.choice(self.actions)

        x, y = state
        action_idx = np.argmax(self.q_table[x, y])
        return self.actions[action_idx]

    def update(self, state, action, reward, next_state):
        """Apply Q-learning update rule."""
        x, y = state
        a = self.actions.index(action)
        nx, ny = next_state

        best_next_q = np.max(self.q_table[nx, ny])
        td_target = reward + self.gamma * best_next_q
        td_error = td_target - self.q_table[x, y, a]
        self.q_table[x, y, a] += self.alpha * td_error

    def train(self, episodes=1000, max_steps=100):
        """Train the agent and store episode reward history."""
        for _episode in range(episodes):
            state = self.env.reset()
            total_reward = 0.0
            steps = 0
            done = False

            while not done and steps < max_steps:
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update(state, action, reward, next_state)

                state = next_state
                total_reward += reward
                steps += 1

            self.episode_rewards.append(total_reward)
            self.episode_steps.append(steps)

        print("Q学習完了")

    def test_run(self, max_steps=100):
        """Run greedy policy and print the test path."""
        state = self.env.reset()
        path = [state]
        done = False
        steps = 0

        while not done and steps < max_steps:
            x, y = state
            action_idx = np.argmax(self.q_table[x, y])
            action = self.actions[action_idx]

            next_state, _reward, done = self.env.step(action)
            path.append(next_state)
            state = next_state
            steps += 1

        print("テスト経路：", path)
        print("経路長：", len(path))
        return path

    def moving_average(self, values, window=30):
        if len(values) < window:
            return values
        kernel = np.ones(window) / window
        return np.convolve(values, kernel, mode="valid")

    def plot_learning_curve(self):
        """Plot episode reward history."""
        plt.figure(figsize=(7, 4))
        plt.plot(self.episode_rewards, alpha=0.4, label="episode reward")

        smooth = self.moving_average(self.episode_rewards, window=30)
        if len(smooth) > 0:
            offset = len(self.episode_rewards) - len(smooth)
            plt.plot(range(offset, len(self.episode_rewards)), smooth, linewidth=2, label="moving avg (30)")

        plt.title("Learning Curve")
        plt.xlabel("Episode")
        plt.ylabel("Total Reward")
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_q_table(self):
        """Visualize max Q-value for each state by heatmap."""
        max_q = np.max(self.q_table, axis=2)

        plt.figure(figsize=(5, 4))
        plt.imshow(max_q, cmap="YlGnBu", origin="upper")
        plt.colorbar(label="max Q")
        plt.title("Q-table Heatmap (max Q per state)")
        plt.xlabel("y")
        plt.ylabel("x")

        for i in range(self.env.size[0]):
            for j in range(self.env.size[1]):
                plt.text(j, i, f"{max_q[i, j]:.2f}", ha="center", va="center", color="black")

        plt.tight_layout()
        plt.show()


# TODO examples (students should implement):
# - Change episodes / alpha / gamma / epsilon and compare learning curves.
# - Change grid size, reward setting, and goal position.
# - Add epsilon decay and compare exploration behavior.
# - Add obstacles and check if the path gets closer to shortest path.
#
# Challenge examples:
# - Build a policy arrow map visualization.
# - Compare F1 function version and F2 class version.
# - Investigate relation to D3 inverted pendulum and deep RL.
