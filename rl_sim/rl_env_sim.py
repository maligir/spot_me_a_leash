
import numpy as np

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

class Slam_Map(object):
    def __init__(self):
        self.map = np.zeros((6, 6))
        self.map[0, 0] = 2
        self.map[5, :5] = -1
        self.map[:4, 5] = -1
        self.map[2, 2:] = -1
        self.map[3, 2] = -1
        self.robot_position = (0, 0)
        self.steps = 0
        self.prev_map = np.copy(self.map)
        self.construct_allowed_states()

    def print_map(self):
        print('---------------------------------')
        for row in self.map:
            for col in row:
                if col == 0:
                    print('', end="\t") # empty space
                elif col == -1:
                    print('X', end="\t") # walls
                elif col == 2:
                    print('R', end="\t") # robot position
            print("\n")
        print('---------------------------------')

    def is_allowed_move(self, state, action):
        # check allowed move from a given state
        y, x = state
        y += ACTIONS[action][0]
        x += ACTIONS[action][1]
        if y < 0 or x < 0 or y > 5 or x > 5:
            # if robot will move off the board
            return False

        if self.map[y, x] == 0 or self.map[y, x] == 2:
            # if robot moves into empty space or its original start position
            return True
        else:
            return False

    def construct_allowed_states(self):
        # create a dictionary of allowed states from any position
        # using the isAllowedMove() function
        # this is so that you don't have to call the function every time
        allowed_states = {}
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                # iterate through all spaces
                if self.map[(y,x)] != -1:
                    # if the space is not a wall, add it to the allowed states dictionary
                    allowed_states[(y,x)] = []
                    for action in ACTIONS:
                        if self.is_allowed_move((y,x), action) and (action != 0):
                            allowed_states[(y,x)].append(action)
        self.allowed_states = allowed_states

    def update_map(self, action, best_state):
        y, x = self.robot_position # get current position
        self.prev_map = np.copy(self.map) # save the previous map
        self.map = np.copy(best_state) # set the current position to 0
        y += ACTIONS[action][0] # get new position
        x += ACTIONS[action][1] # get new position
        self.robot_position = (y, x) # set new position
        self.steps += 1 # add steps

    def is_game_over(self):
        # check if robot in the final position
        if 0 in self.map:
            return False
        else:
            return True
        # if self.robot_position == (5,5):
        #     return True
        # else:
        #     return False

    def get_state_and_reward(self):
        return self.map, self.robot_position, self.give_reward()

    def give_reward(self):
        # if at end give 0 reward
        # if not at end give -1 reward
        if np.sum(self.prev_map) == np.sum(self.map):
            return 0
        else: 
            return -1