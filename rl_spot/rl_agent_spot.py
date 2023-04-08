import numpy as np

# ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
# ACTIONS = publish to cmd vel one direction (up, down, left, right)
# ACTIONS = publish to cmd vel/nav goal 360 degrees of rotation and forward movement

class Agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2): # 80% explore, 20% exploit
        self.state_history = [((0, 0), 0)] # state, reward
        self.alpha = alpha
        self.randomFactor = random_factor
        # self.G = np.gauss(0 to 360 degrees) to set initial rewards
    
    def choose_action(self, state):
        next_move = None
        randomN = np.random.random()
        if randomN < self.randomFactor:
            # if random number below random factor, choose random action
            # next move = closest/farthest frontier
            pass
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            # next move = we move in the direction of the higheset G
            # move in that direction
            pass
        
        return next_move

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0
        
        # for every state and reward (prev occupancy grid and value of direction to move)
        # update the value of the direction to move

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.randomFactor -= 10e-5 # decrease random factor each episode of play