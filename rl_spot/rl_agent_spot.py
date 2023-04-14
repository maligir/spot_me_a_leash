import numpy as np
import pickle

# ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
# ACTIONS = publish to cmd vel one direction (up, down, left, right)
# ACTIONS = publish to cmd vel/nav goal 360 degrees of rotation and forward movement
ACTIONS = range(0, 12)

class Agent(object):
    def __init__(self, alpha=0.15, random_factor=0.2): # 80% explore, 20% exploit
        self.state_history = [(None, 0)] # fe_state, reward
        self.alpha = alpha
        self.randomFactor = random_factor
        self.G = {}
        self.init_reward()
        
    def init_reward(self):
        for i in ACTIONS:
            self.G[i] = np.random.uniform(low=1.0, high=0.1)
    
    def choose_action(self, fe_state):
        next_move = None
        randomN = np.random.random()
        if randomN < self.randomFactor:
            # if random number below random factor, choose random action
            # next move = closest/farthest frontier
            next_move = fe_state.move_info
            pass
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            # next move = we move in the direction of the higheset G
            # move in that direction
            # set next move to the highest direction in G
            next_move = {"dist": 900, "rad": max(self.G, key=self.G.get)}
        
        fe_state.move_rl = next_move
        # TODO change 60 to a reasonable time
        if fe_state.move_rl["rad"] < 7:
            fe_state.turn_time = 28 * fe_state.move_rl["rad"]
        else:
            fe_state.move_rl = 28 * abs(fe_state.move_rl["rad"] - 12)
        fe_state.move_time = 180
        
        return next_move

    def update_state_history(self, fe_state, reward):
        self.state_history.append((fe_state.move_rl, reward))

    def learn(self):
        target = 0
        
        # for every state and reward (prev occupancy grid and value of direction to move)
        # update the value of the direction to move

        for move_info, reward in reversed(self.state_history):
            self.G[move_info["rad"]] = self.G[move_info["rad"]] + self.alpha * (target - self.G[move_info["rad"]])
            target += reward

        self.state_history = []

        self.randomFactor -= 0.01 # decrease random factor each episode of play
        # TODO chang random factor based on how fast we want it to learn
    
    def save(self):
        with open("g.pickle", "wb") as g:
            pickle.dump(self.G, g)
        with open("random.pickle", "wb") as rando:
            pickle.dump(self.randomFactor, rando)
        with open("state_history.pickle", "wb") as sh:
            pickle.dump(self.state_history, sh)
    
    def load(self):
        with open("g.pickle", "rb") as g:
            self.G = pickle.load(g)
        with open("random.pickle", "rb") as rando:
            self.randomFactor = pickle.load(rando)
        with open("state_history.pickle", "rb") as sh:
            self.state_history = pickle.load(sh)