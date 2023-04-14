import numpy as np
from rl_env_sim import Maze
from rl_agent_sim import Agent
if __name__ == '__main__':
    maze = Maze()
    robot = Agent(alpha=0.1, random_factor=0.2)
    # robot.load() # comment out for first training iteration
    moveHistory = []
    while not maze.is_game_over():
        fe_state, _ = maze.get_state_and_reward() # get the current state
        action = robot.choose_action(fe_state) # choose an action (explore or exploit)
        fe_state, reward = maze.get_state_and_reward() # get the new state and reward
        robot.update_state_history(fe_state, reward) # update the robot memory with state and reward
    
    robot.learn() # robot should learn after every episode
    robot.save() # save the robot memory