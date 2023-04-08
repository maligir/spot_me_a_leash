
import numpy as np

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

class Maze(object):
    def __init__(self):
        # self.robot_position = (0, 0)
        # self.steps = 0
        pass

    def is_game_over(self):
        # check if robot in the final position
        if self.robot_position == (5, 5):
            return True
        else:
            return False

    def get_state_and_reward(self):
        return self.robot_position, self.give_reward()

    def give_reward(self):
        # if at end give 0 reward
        # if not at end give -1 reward
        # reward is calcualted by change in amount of mapd iscovered form prev to new)
        if self.robot_position == (5, 5):
            return 0
        else: 
            return -1