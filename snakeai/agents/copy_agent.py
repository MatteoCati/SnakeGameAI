import random
import numpy as np
from collections import deque
from keras.layers import Dense
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from snakeai.game.constants import Actions
from snakeai.agents.agent_interface import AbstractAgent

class DQN(AbstractAgent):
    """An agent that uses deep learning, using a simplified description of the state
    
    Parameters
    -----------
    dim : int
        the dimension of the board (side length)
    
    Attributes
    -----------
    dim : int
        the size of the board (side length)
    epsilon : float [0, 1]
        The current epsilon value
    gamma : float [0, 1]
        The discount factor
    batch_size : int
        The dimension of each batch for training
    epsilon_min : float [0, 1]
        The minimum value for epsilon
    epsilon_decay : float [0, 1)
        The decay factor of epsilon at each episode
    learning_rate : float [0, 1]
        The learning rate
    memory : deque
        The list of states used for learning
    model : keras.Model
        The model used by the agent
    """
    def __init__(self, dim):

        self.action_space = 4
        self.state_space = 12
        self.dim = dim

        self.epsilon = 1
        self.gamma = 0.95
        self.batch_size = 500
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.00025
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()


    def build_model(self):
        """Create The Deep Learning model"""
        inputs = keras.Input((self.state_space,))
        x = Dense(128, activation = "relu")(inputs)
        x = Dense(128, activation = "relu")(x)
        x = Dense(128, activation = "relu")(x)
        outputs = layers.Dense(self.action_space, activation = "softmax", name = "output")(x)
        model = keras.Model(inputs = inputs, outputs = [outputs])
        model.compile(optimizer = Adam(learning_rate=self.learning_rate), loss="mse")
        return model

    def execute(self, state):
        """Get the next action to do, given the state
        Parameters
        -----------
        state : FrozenState
            The current state of the game

        Returns
        --------
        Actions
            The action chosen by the agent
        """
        state = np.reshape(state.simpleState, (1, self.state_space))
        if np.random.rand() <= self.epsilon:
            act =  random.randrange(self.action_space)
        else:
            act_values = self.model.predict(state)
            act =  np.argmax(act_values[0])
        if act == 0:
            return Actions.UP
        elif act == 1:
            return Actions.RIGHT
        elif act == 2:
            return Actions.DOWN
        return Actions.LEFT

    def fit(self, oldState, action, rew, state, done):
        """Add the current step to the memory and train the model
        
        Parameters
        ------------
        oldState : FrozenState
            The state of the game before taking the action
        action : Actions
            The action chosen
        rew : int
            The reward obtained after taking the action
        state : FrozenState
            The state after takinf the action
        done : bool
            Whether the state is terminal 
        """
        action = [Actions.UP, Actions.RIGHT, Actions.DOWN, Actions.LEFT].index(action)
        oldState = np.reshape(oldState.simpleState, (1, self.state_space))
        state = np.reshape(state.simpleState, (1, self.state_space))
        self.memory.append((oldState, action, rew, state, done))
        self.replay()

    def replay(self):
        """Train the model with one batch"""
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict(states)

        ind = np.array([i for i in range(self.batch_size)])
       # print(actions)
        targets_full[[ind], [actions]] = targets
        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
