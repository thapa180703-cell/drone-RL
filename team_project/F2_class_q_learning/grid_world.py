"""GridWorld environment for F2 class-based Q-learning starter."""

class GridWorld:
    def __init__(self, size=(4, 4), goal=(3, 3)):
        self.size = size
        self.goal = goal
        self.state = (0, 0)
        self.actions = ["up", "down", "left", "right"]

    def reset(self):
        """Reset environment and return initial state."""
        self.state = (0, 0)
        return self.state

    def step(self, action):
        """Move one step in the environment.

        Returns:
            next_state, reward, done
        """
        x, y = self.state

        if action == "up" and x > 0:
            x -= 1
        elif action == "down" and x < self.size[0] - 1:
            x += 1
        elif action == "left" and y > 0:
            y -= 1
        elif action == "right" and y < self.size[1] - 1:
            y += 1

        self.state = (x, y)
        done = self.state == self.goal
        reward = 1.0 if done else -0.01
        return self.state, reward, done
