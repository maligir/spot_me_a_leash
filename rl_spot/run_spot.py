import numpy as np
from rl_env_sim import Maze
from rl_agent_sim import Agent
import matplotlib.pyplot as plt

if __name__ == '__main__':
    maze = Maze()
    robot = Agent(maze.maze, alpha=0.1, random_factor=0.25)
    moveHistory = []

    for i in range(5000):
        if i % 1000 == 0:
            print(i)

        while not maze.is_game_over():
            fe_state, _ = maze.get_state_and_reward() # get the current state
            action = robot.choose_action(fe_state) # choose an action (explore or exploit)
            fe_state, reward = maze.get_state_and_reward() # get the new state and reward
            robot.update_state_history(fe_state, reward) # update the robot memory with state and reward
        
        robot.learn() # robot should learn after every episode
        maze = Maze() # reinitialize the maze