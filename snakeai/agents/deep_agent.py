from snakeai.game.model import Snake
from snakeai.game.constants import Actions, Coords
from snakeai.agents.agent_interface import AbstractAgent
import random
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from collections import deque

class MLAgent(AbstractAgent):
    def __init__(self, dim):
       # self.MAX_TRAIN_SIZE = 2000
        self.BATCH_SIZE = 500
        self.GAMMA = 0.95
        self.UPDATE_TARGET_MODEL = 50
        self.EPSILON = 1
        self.MIN_EPSILON = 0.01
        self.EPSILON_DECAY = 0.995
        
        self.dim = dim
        self.model = self.createModel()
        self.trainingData = deque(maxlen = 5000)
        self.prevAction = None
        self.num_episodes = 0
    
    def reset(self):
        self.prevAction = None
        self.num_episodes += 1
        if self.EPSILON > self.MIN_EPSILON:
            self.EPSILON *= self.EPSILON_DECAY
        #if self.num_episodes > self.UPDATE_TARGET_MODEL:
        #    self.num_episodes = 0
        #    self.target_model.set_weights(self.model.get_weights())
    
    def _tablecreateModel(self):
        inputs = keras.Input((self.dim, self.dim, 1))
        x = layers.Conv2D(filters= 32, kernel_size = 3, activation = "relu")(inputs)
        x = layers.Flatten()(x)
        x = layers.Dense(64, activation = "relu")(x)
        x = layers.Dense(64, activation = "relu")(x)
        outputs = layers.Dense(4, activation = "linear", name = "output")(x)
        model = keras.Model(inputs = inputs, outputs = [outputs])
        model.compile(optimizer = keras.optimizers.Adam(learning_rate=0.03), loss={'output': 'mse'}, metrics={'output': 'accuracy'})
        return model

    def createModel(self):
        inputs = keras.Input((12,))
        x = layers.Dense(128, activation = "relu")(inputs)
        x = layers.Dense(128, activation = "relu")(x)
        x = layers.Dense(128, activation = "relu")(x)
        outputs = layers.Dense(4, activation = "linear", name = "output")(x)
        model = keras.Model(inputs = inputs, outputs = [outputs])
        model.compile(optimizer = keras.optimizers.Adam(learning_rate=0.00025), loss={'output': 'mse'}, metrics={'output': 'accuracy'})
        return model
    
    def _difrefineData(self, snake, apple):
        data = list()
        for y in range(self.dim):
            t = list()
            for x in range(self.dim):
                p = Coords(x, y)
                if p == snake[-1]:
                    t.append(3)
                elif p in snake:
                    t.append(2)
                elif p == apple:
                    t.append(1)
                else:
                    t.append(0)
            data.append(t)
        return np.array(data).reshape(-1, self.dim*self.dim)
    
    def refineData(self, snake, apple):
        data = []
        data.append(1 if apple.y < snake[-1].y else 0) # Is apple up
        data.append(1 if apple.y > snake[-1].y else 0) # Is apple down
        data.append(1 if apple.x < snake[-1].x else 0) # Is apple left
        data.append(1 if apple.x > snake[-1].x else 0) # Is apple right

        isEmpty = lambda c: (not c in snake) and 0 <= c.x < self.dim and 0 < c.y < self.dim
        up = Actions.UP.value + snake[-1]
        if isEmpty(up): data.append(1)
        else: data.append(0)

        down = Actions.DOWN.value + snake[-1]
        if isEmpty(down): data.append(1)
        else: data.append(0)

        left = Actions.LEFT.value + snake[-1]
        if isEmpty(left): data.append(1)
        else: data.append(0)

        right = Actions.RIGHT.value + snake[-1]
        if isEmpty(right): data.append(1)
        else: data.append(0)

        data.append(int(self.prevAction == 0))
        data.append(int(self.prevAction == 1))
        data.append(int(self.prevAction == 2))
        data.append(int(self.prevAction == 3))

        return np.array(data).reshape(-1, 12)


    
    def execute(self, snake, apple):
        if random.random() < self.EPSILON:
            self.prevAction = random.choice([0,1,2,3])
        else:
            state = self.refineData(snake, apple)
            probs = self.model.predict(state)
            self.prevAction = np.argmax(probs)
        if self.prevAction == 0:
            return Actions.UP
        elif self.prevAction == 1:
            return Actions.DOWN
        elif self.prevAction == 2:
            return Actions.LEFT
        return Actions.RIGHT
        
    def fit(self, oldSnake, oldApple, action, rew, snake, apple, done):
        oldState = self.refineData(oldSnake, oldApple)
        state = self.refineData(snake, apple)
        self.trainingData.append((oldState, self.prevAction, rew, state, done))
        self.train()
        
    def train(self):
        if len(self.trainingData) < self.BATCH_SIZE:
            return
        batch = random.sample(self.trainingData, self.BATCH_SIZE)
        x = []
        y = []
        for (state, action, reward, nextState, isGameOver) in batch:
            x.append(state)
            currentEstimate = self.model.predict(state)[0]
            Q = reward
            if not isGameOver:
                Q += self.GAMMA * np.max(self.model.predict(nextState))
            if action == Actions.UP:
                currentEstimate[0] = Q
            elif action == Actions.DOWN:
                currentEstimate[1] = Q
            elif action == Actions.LEFT:
                currentEstimate[2] = Q
            else:
                currentEstimate[3] = Q
            y.append(currentEstimate)
        #print("fit", np.array(x).shape)
        self.model.fit(x = np.array(x).reshape(-1, 12), y = np.array(y), batch_size = self.BATCH_SIZE, 
                       verbose = 0, shuffle=False)