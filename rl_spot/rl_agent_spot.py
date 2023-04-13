import numpy as np

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
            next_move = {"dist": .5, "rad": max(self.G, key=self.G.get)}
        
        fe_state.move_info = next_move
        # TODO change 60 to a reasonable time
        if fe_state.move_info["rad"] < 7:
            fe_state.turn_time = 60 * self.move_info["rad"]
        else:
            fe_state.turn_time = 60 * abs(self.move_info["rad"] - 12)
        fe_state.move_time = 180
        
        return next_move

    def update_state_history(self, fe_state, reward):
        self.state_history.append((fe_state.move_info, reward))

    def learn(self):
        target = 0
        
        # for every state and reward (prev occupancy grid and value of direction to move)
        # update the value of the direction to move

        for move_info, reward in reversed(self.state_history):
            self.G[move_info["rad"]] = self.G[move_info["rad"]] + self.alpha * (target - self.G[move_info["rad"]])
            target += reward

        self.state_history = []

        self.randomFactor -= 10e-5 # decrease random factor each episode of play
        # TODO chang random factor based on how fast we want it to learn