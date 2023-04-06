import numpy as np
from rl_env_sim import Slam_Map
from rl_agent_sim import Agent
import matplotlib.pyplot as plt

if __name__ == '__main__':
    slam_map = Slam_Map()
    robot = Agent(slam_map.map, alpha=0.1, random_factor=0.25)
    moveHistory = []

    for i in range(5000):
        if i % 1000 == 0:
            print(i)

        while not slam_map.is_game_over():
            state, cur_pos, _ = slam_map.get_state_and_reward() # get the current state
            action, best_state = robot.choose_action(state, slam_map.allowed_states[cur_pos], cur_pos) # choose an action (explore or exploit)
            # if i == 4999:
                # slam_map.print_map()
            print(best_state)
            slam_map.update_map(action, best_state) # update the slam_map according to the action
            state, cur_pos, reward = slam_map.get_state_and_reward() # get the new state and reward
            robot.update_state_history(cur_pos, reward) # update the robot memory with state and reward
            if slam_map.steps > 1000:
                # end the robot if it takes too long to find the goal
                break
        
        robot.learn() # robot should learn after every episode
        moveHistory.append(slam_map.steps) # get a history of number of steps taken to plot later
        slam_map = Slam_Map() # reinitialize the maze
plt.semilogy(moveHistory, "b--")
plt.show()