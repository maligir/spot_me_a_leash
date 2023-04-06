import numpy as np

ACTIONS = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}

class Agent(object):
    def __init__(self, states, alpha=0.15, random_factor=0.2): # 80% explore, 20% exploit
        self.state_history = [((0, 0), 0)] # state, reward
        self.alpha = alpha
        self.randomFactor = random_factor
        self.G = {}
        self.init_reward(states)

    def init_reward(self, states):
        for i, row in enumerate(states):
            for j, col in enumerate(row):
                self.G[(j, i)] = np.random.uniform(low=1.0, high=0.1)
    
    def choose_action(self, state, allowedMoves, current_pos):
        maxSum = -np.inf
        next_move = None
        best_state = None
        randomN = np.random.random()
        if randomN < self.randomFactor:
            # if random number below random factor, choose random action
            next_move = np.random.choice(allowedMoves)
        else:
            # if exploiting, gather all possible actions and choose one with the highest G (reward)
            for action in allowedMoves:
                new_pos = tuple([sum(x) for x in zip(current_pos, ACTIONS[action])])
                
                # calculate vision based on how much robot can see in a radius
                # if new state count is greater more than current then that is best state
                
                # calculate possible vision
                vision_x = []
                vision_y = []
                for i in range(0, 3):
                    for j in range(0, 3):
                        vision_y.append(new_pos[0] + i)
                        vision_x.append(new_pos[1] + j)
                        vision_y.append(new_pos[0] - i)
                        vision_x.append(new_pos[1] - j)
                        vision_y.append(new_pos[0] + i)
                        vision_x.append(new_pos[1] - j)
                        vision_y.append(new_pos[0] - i)
                        vision_x.append(new_pos[1] + j)
                
                # remove vision out of bounds
                x = np.array(vision_x)
                y = np.array(vision_y)
                mask = np.logical_and(np.logical_and(x>=0, x<=state.shape[1]), np.logical_and(y>=0, y<=state.shape[0]))
                x=x[mask]
                y=y[mask]
                
                # calculate new state with move
                new_state = np.copy(state) 
                new_state[new_pos[0], new_pos[1]] = 2
                new_state[current_pos[0], current_pos[1]] = 0

                # calculate new state with vision
                for i in range(len(x)):
                    if new_state[y[i], x[i]] == 0:
                        new_state[y[i], x[i]] = 1
                        
                # choose state with most vision uncovered
                if np.sum(new_state) > maxSum:
                    next_move = action
                    maxSum = np.sum(new_state)
                    best_state = new_state

        return (next_move, best_state)

    def update_state_history(self, state, reward):
        self.state_history.append((state, reward))

    def learn(self):
        target = 0

        for prev, reward in reversed(self.state_history):
            self.G[prev] = self.G[prev] + self.alpha * (target - self.G[prev])
            target += reward

        self.state_history = []

        self.randomFactor -= 10e-5 # decrease random factor each episode of play