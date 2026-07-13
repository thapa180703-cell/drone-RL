"""Entry point for F2 class-based Q-learning starter."""

from grid_world import GridWorld
from q_agent import QLearningAgent


def main():
    env = GridWorld(size=(4, 4), goal=(3, 3))
    agent = QLearningAgent(env, alpha=0.1, gamma=0.9, epsilon=0.2)

    agent.train(episodes=1000, max_steps=100)
    agent.test_run(max_steps=100)

    # Visualizations added for this year's starter
    agent.plot_learning_curve()
    agent.plot_q_table()

    print("\nTODO: parameters and reward design を変更して挙動を観察しよう。")


if __name__ == "__main__":
    main()
