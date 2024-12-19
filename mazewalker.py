import argparse
import random
import sys

# Try importing Pygame for GUI mode
try:
    import pygame

    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


# Maze generation logic with a single entrance
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = [(0, 0)]
    visited = set(stack)

    while stack:
        x, y = stack[-1]
        maze[y][x] = 0
        neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
        random.shuffle(neighbors)

        for nx, ny in neighbors:
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                visited.add((nx, ny))
                stack.append((nx, ny))
                maze[(y + ny) // 2][(x + nx) // 2] = 0
                break
        else:
            stack.pop()

    # Add a single entrance and ensure the center is open
    maze[0][0] = 0
    maze[height // 2][width // 2] = 0
    return maze


# Robot AI with self-learning
class RobotAI:
    def __init__(self, maze):
        self.maze = maze
        self.q_table = {}
        self.actions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0
        self.exploration_decay = 0.99

    def get_state(self, x, y):
        return (x, y)

    def choose_action(self, state):
        if random.random() < self.exploration_rate:
            return random.choice(self.actions)
        return max(
            self.actions, key=lambda action: self.q_table.get((state, action), 0)
        )

    def learn(self, state, action, reward, next_state):
        old_value = self.q_table.get((state, action), 0)
        future_rewards = max(self.q_table.get((next_state, a), 0) for a in self.actions)
        self.q_table[(state, action)] = old_value + self.learning_rate * (
            reward + self.discount_factor * future_rewards - old_value
        )

    def update_exploration(self):
        self.exploration_rate *= self.exploration_decay


# Helper function for robot movement
def move_robot(position, action, maze):
    x, y = position
    if action == "UP" and y > 0 and maze[y - 1][x] == 0:
        return [x, y - 1]
    elif action == "DOWN" and y < len(maze) - 1 and maze[y + 1][x] == 0:
        return [x, y + 1]
    elif action == "LEFT" and x > 0 and maze[y][x - 1] == 0:
        return [x - 1, y]
    elif action == "RIGHT" and x < len(maze[0]) - 1 and maze[y][x + 1] == 0:
        return [x + 1, y]
    return position  # No movement if blocked


# Text-based Mode
def run_text_mode(maze):
    print("Running in Text Mode...")
    robot = RobotAI(maze)
    robot_pos = [0, 0]
    goal_pos = [len(maze[0]) // 2, len(maze) // 2]

    while robot_pos != goal_pos:
        for row in maze:
            print("".join(["#" if cell == 1 else "." for cell in row]))
        print(f"Robot is at {robot_pos}, Goal is at {goal_pos}")
        state = tuple(robot_pos)
        action = robot.choose_action(state)
        next_pos = move_robot(robot_pos, action, maze)
        reward = 100 if next_pos == goal_pos else -1
        robot.learn(state, action, reward, tuple(next_pos))
        robot.update_exploration()
        robot_pos = next_pos
        input("Press Enter to step...")

    print("Robot reached the goal!")


# GUI-based Mode
def run_gui_mode(maze):
    try:
        if not PYGAME_AVAILABLE:
            raise RuntimeError("Pygame is not installed. Falling back to text mode.")
        pygame.init()
        cell_size = 20
        width, height = len(maze[0]), len(maze)
        screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption("Maze Walker")
        clock = pygame.time.Clock()

        robot = RobotAI(maze)
        robot_pos = [0, 0]
        goal_pos = [width // 2, height // 2]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Draw the maze
            screen.fill((0, 0, 0))
            for y, row in enumerate(maze):
                for x, cell in enumerate(row):
                    color = (255, 255, 255) if cell == 1 else (0, 0, 0)
                    pygame.draw.rect(
                        screen,
                        color,
                        (x * cell_size, y * cell_size, cell_size, cell_size),
                    )

            # Draw the robot
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (
                    robot_pos[0] * cell_size + cell_size // 2,
                    robot_pos[1] * cell_size + cell_size // 2,
                ),
                cell_size // 3,
            )

            # Robot decision and movement
            state = tuple(robot_pos)
            action = robot.choose_action(state)
            next_pos = move_robot(robot_pos, action, maze)
            reward = 100 if next_pos == goal_pos else -1
            robot.learn(state, action, reward, tuple(next_pos))
            robot.update_exploration()
            robot_pos = next_pos

            if robot_pos == goal_pos:
                print("Robot reached the goal!")
                break

            pygame.display.flip()
            clock.tick(30)

    except Exception as e:
        print(f"Error in GUI mode: {e}. Falling back to text mode.")
        run_text_mode(maze)


# Main function
def main():
    parser = argparse.ArgumentParser(description="Maze Walker")
    parser.add_argument(
        "--mode", choices=["gui", "text"], help="Choose the mode to run the program"
    )
    args = parser.parse_args()

    width, height = 21, 21
    maze = generate_maze(width, height)

    # Default to GUI if Pygame is available and no mode is specified
    if args.mode == "gui" or (PYGAME_AVAILABLE and args.mode is None):
        run_gui_mode(maze)
    else:
        run_text_mode(maze)


if __name__ == "__main__":
    main()
