
import numpy as np
from fe import fe_run
import time
import sys

ACTIONS = range(0, 12)

class Maze(object):
    def __init__(self):
        self.fe_state = fe_run()
        self.start_time = time.time()
        pass

    def is_game_over(self):
        # check if robot in the final position
        if time() - self.start_time > 30:
            return True
        else:
            return False

    def get_state_and_reward(self):
        return self.fe_state, self.give_reward()

    def give_reward(self):
        # reward is calcualted by change in amount of map iscovered form prev to new)
        # TODO proper way to do this is find how much of the overall map is uncovered

        # return how much more cur map has explored can prev map
        if self.fe_state.prev_map is None:
            # map doesn't exist
            return 0
        else: 
            # count number of cells that are not -1 in cur map and non -1 in prev map
            cur = np.array(self.fe_state.cur_map) != -1
            prev = np.array(self.fe_state.prev_map) != -1
            # TODO scale reward
            return 1 if len(cur) - len(prev) > 0 else -1

            # return np.array(self.fe_state.cur_map) != -1 - np.array(self.fe_state.prev_map) != -1