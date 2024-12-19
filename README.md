# Maze Walker

Maze Walker is a Python program where a robot learns to navigate a randomly generated maze using reinforcement learning. The program supports both graphical (Pygame) and text-based (CLI) modes and can dynamically switch between modes or fall back to text mode if graphical mode cannot be started.

---

## Features

### General

- Generates random mazes with a single entrance and one guaranteed path to the center
- Includes reinforcement learning (Q-learning) for the robot to self-learn the optimal path
- Supports graphical (GUI) mode using Pygame for visualization
- Includes text-only (CLI) mode for environments where graphical mode is unavailable
- Automatically falls back to CLI mode if GUI mode fails, with a user notification
- Default behavior dynamically selects the best mode based on system capabilities

### Graphical Mode (GUI)

- Visualizes the maze as a grid with walls and paths
- Displays the robot navigating the maze in real-time
- Adjustable maze dimensions via arguments
- Interactive controls:
  - Close window button: Exit the simulation
  - `ESC` or `Ctrl+C`: Exit the program

### Text-Only Mode (CLI)

- Renders the maze using ASCII characters:
  - `#` for walls
  - `.` for paths
- Dynamically updates the robot's position in the terminal
- Logs robot's actions and progress step-by-step
- Interactive controls:
  - `Enter`: Step through the robot's actions
  - `ESC` or `Ctrl+C`: Exit the program

---

## Requirements

- Python 3.6 or higher
- Pygame (for GUI mode)

To install Pygame, run:

```bash
pip install pygame
```

## Running the Program

Save the script as `mazewalker.py` and run it from the terminal using one of the following modes.

### Graphical Mode (GUI)

```bash
python mazewalker.py --mode gui
```

### Text-Only Mode (CLI)

```bash
python mazewalker.py --mode text
```

### Automatic Mode Selection

If no mode is specified, the program defaults to GUI mode if Pygame is available. If GUI mode fails or Pygame is unavailable, the program automatically falls back to text mode.

---

## Command-Line Arguments

| Argument   | Default | Description                                            |
| ---------- | ------- | ------------------------------------------------------ |
| `--mode`   | `gui`   | Choose between `gui` (graphical) and `text` (CLI) mode |
| `--width`  | 21      | Width of the maze in cells                             |
| `--height` | 21      | Height of the maze in cells                            |

---

## Example Commands

### Graphical Mode with Custom Maze Size

```bash
python mazewalker.py --mode gui --width 25 --height 25
```

### Text-Only Mode with Default Maze Size

```bash
python mazewalker.py --mode text
```

### Automatic Mode Selection

```bash
python mazewalker.py
```

---

## Code Structure

The program is structured into several modular functions and classes to handle different aspects of the simulation:

- `generate_maze(width, height)`: Generates a random maze with a single entrance and one path to the center
- `RobotAI`: Implements Q-learning for self-learning and navigation
  - `choose_action(state)`: Selects the next action based on the Q-table and exploration rate
  - `learn(state, action, reward, next_state)`: Updates the Q-table based on rewards
- `run_text_mode(maze)`: Handles text-based rendering and interaction
- `run_gui_mode(maze)`: Handles graphical rendering and interaction using Pygame
- `main()`: Parses command-line arguments, handles mode selection, and manages fallback logic

---

## Development and Contributions

This project was developed collaboratively with Code Duo, an AI-powered coding assistant, and refined based on user feedback.

For contributions or feature requests, please contact:

- [Code Duo](https://chat.openai.com/g/g-RRSEH8DSf-code-duo)

---

## Future Enhancements

Planned features for future development:

- Visualization of Q-learning progress in GUI mode
- Save and load maze configurations for reuse
- Customizable robot behavior parameters via CLI arguments
- User-designed mazes in CLI mode

---

## License

This project is licensed under the MIT License. Users are free to use, modify, and distribute the code.

For more information or to report issues, please contact istvan@airobotika.com.
