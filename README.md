# Spot Me A Leash

This is a README document that describes a project for an exploration robot using reinforcement learning and keyboard input for manual control. The robot uses its current and previous states to learn and decide on its actions. These states are a combination of an occupancy grid and other information from the robot's perspective.

## Project Overview

The robot navigates a virtual environment called `Maze` in the `rl_env_spot.py` module. The agent's decision-making mechanism is described in the `rl_agent_spot.py` module. The `run_spot.py` is the main script that ties these modules together to perform reinforcement learning. The `fe.py` script is used to define the frontier exploration algorithm. Keyboard control is facilitated via the `keyboard_input.py` script, and automatic control is accomplished using the `automatic_itl.py` script.

The project consists of six main Python files:

1. **fe.py**: Contains the definition of frontier exploration logic.
2. **rl_agent_spot.py**: Contains the definition of the agent that learns from its actions and environment.
3. **rl_env_spot.py**: Sets up the environment in which the agent interacts.
4. **run_spot.py**: Main driver script that runs the reinforcement learning loop using the agent and the environment.
5. **keyboard_input.py**: Facilitates keyboard control of the robot.
6. **automatic_itl.py**: Allows for automatic control of the robot, listening for inputs and publishing them as movement commands.

## Python Files Description

### fe.py

This file contains the `fe_run` class which is responsible for the robot's frontier exploration. Here is a brief description of its methods:

- `__init__()`: Initializes the `fe_run` class with properties related to map, move, and turning time.
- `run_prog()`: Triggers the frontier exploration program, which involves publishing to cmd_vel and nav_goal while subscribing to map.
- `map_callback()`: Callback function for the map subscriber, which generates a copy of the map data.

### rl_agent_spot.py

This file contains the `Agent` class which is the main decision-maker entity in the program. Here is the brief description of its methods:

- `__init__()`: Initializes the agent with the learning rate (`alpha`), a randomness factor for the agent's actions, and initializes the agent's state history and reward table.
- `init_reward()`: Initializes the rewards for the actions randomly.
- `choose_action()`: Based on the current state, the agent decides on the next action.
- `update_state_history()`: Updates the state history with the latest state and its associated reward.
- `learn()`: Applies the Q-learning rule to update the action-value (Q) table.
- `save()`: Saves the agent's state history, action-value table, and the randomness factor to a pickle file.
- `load()`: Loads the agent's state history, action-value table, and the randomness factor from a pickle file.

### rl_env_spot.py

This file defines the `Maze` class which represents the environment in which the agent operates. Its methods are:

- `__init__()`: Initializes the Maze class and starts the fe_run program.
- `is_game_over()`: Checks whether the game is over. Currently, this is based on a 30 seconds time limit.
- `get_state_and_reward()`: Returns the current state and the associated reward.
- `give_reward()`: Calculates the reward based on the exploration of the map.

### run_spot.py

This script sets up the agent and environment, runs the reinforcement learning loop, and saves the agent's state at the end. The main steps in this loop are:

- Initialization of the Maze and Agent objects.
- While the game is not over:
  - The agent gets the current state and chooses an action.
  - The new state and reward are determined.
  - The agent's state history is updated.
- After the game, the agent learns from the state history and its memory is saved.

### keyboard_input.py

This script enables manual control of the robot using keyboard input. A direction (w, a, s, d) is entered through the keyboard, and it's published to the 'itl_keyboard' topic for the robot to execute.

### automatic_itl.py

This script listens to the 'itl_keyboard' topic for any incoming direction commands. Upon receiving a direction, it calculates the necessary linear and angular velocity for the robot to move in the desired direction and publishes this velocity command to the 'cmd_vel' topic.

## Instructions

A simplified instruction list for the deployment of the program is available in `instructions_simplified.txt`. It provides terminal commands for various operations including environment setup, program execution, and keyboard control.

## Getting Started

To run the reinforcement learning part of the code, use the command:

```bash
python run_spot.py
```

To control the robot manually using the keyboard, run:

```bash
python keyboard_input.py
```

and:

```bash
python automatic_itl.py
```

Note: All the python scripts require `rospy` which is a part of the Robot Operating System (ROS) to run. Therefore, you need to have ROS installed and configured properly on your machine.
## Contributing

Contributions are welcome. Please fork the repository and create a pull request for any features, fixes, or improvements.

## License

Please specify the license for your project. If you have not decided yet, consider using the [MIT License](https://opensource.org/licenses/MIT).

## Authors

Rahul Maligi & Anushka Shah.

## Contact

If you have any questions or suggestions, please feel free to contact us.

## Acknowledgments

Any acknowledgments, if applicable.

## Disclaimer

The code is for educational purposes only and is not suitable for any real-world application in its current state. Always test the code in a controlled environment before using.
