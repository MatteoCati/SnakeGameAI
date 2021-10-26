import random
from collections import deque
from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.memento import FrozenState
from snakeai.game.constants import Actions
from keras.layers import Dense, Conv2D, Flatten
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
import numpy as np
from tensorflow.keras.models import load_model

class DeepQAgent(AbstractAgent):
    """An agent that uses deep learning, using a simplified description of the state

    Parameters
    -----------
    dim : int
        the dimension of the board (side length)

    Attributes
    -----------
    dim : int
        the size of the board (side length)
    action_space : int
        The number of actions to choose from
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
    targetModel : keras.Model
        The model used as target during training
    updatePeriod : int
        The number of episodes after which the targetModel is updated
    lastUpdate : int
        The number of episodes occurred since last update of targetModel
    prevState1 : list(list(int))
        The previous state
    prevState2 : list(list(int))
        The state 2 time steps ago
    prevState3 : list(list(int))
        The state 3 time steps ago 
    """

    def __init__(self, dim):
        super().__init__(dim)

        self.action_space = 4
        self.gamma = 0.95
        self.batch_size = 500
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.00025
        self.memory = deque(maxlen=2500)
        self.model = self.createModel()
        self.targetModel = self.createModel()
        self.updatePeriod = 20
        self.lastUpdate = 0
        self.updateTargetModel()

        self.prevState1 = None
        self.prevState2 = None
        self.prevState3 = None

    def updateTargetModel(self):
        """Update target model with weights from the current model"""
        self.targetModel.set_weights(self.model.get_weights())

    def createModel(self):
        """Create The Deep Learning model"""
        inputs = keras.Input((self.dim, self.dim, 2))
        x = Conv2D(filters = 32, kernel_size=(5,5), activation="relu")(inputs)
        x = Conv2D(filters = 64, kernel_size=(3,3), activation="relu")(x)
        x = Conv2D(filters = 128, kernel_size=(2,2), activation="relu")(x)
        x = Flatten()(x)
        x = Dense(512, activation = "relu")(x)
        #x = Dense(128, activation = "relu")(x)
        #x = Dense(128, activation = "relu")(x)
        outputs = layers.Dense(self.action_space, activation = "linear", name = "output")(x)
        model = keras.Model(inputs = inputs, outputs = [outputs])
        model.compile(optimizer = Adam(learning_rate=self.learning_rate), loss="mse")
        return model


    def execute(self, state) -> Actions:
        st = state.table
        if self.prevState1:
            table = [self.prevState3, self.prevState2, self.prevState1, st]
        else:
            table = [st, st, st, st]
        table = np.reshape(table, (-1, self.dim, self.dim, 2))
        if np.random.rand() <= self.epsilon:
            act =  random.randrange(self.action_space)
        else:
            act_values = self.model.predict(table)
            act =  np.argmax(act_values[0])
        if act == 0:
            return Actions.UP
        if act == 1:
            return Actions.RIGHT
        if act == 2:
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
        st = oldState.table
        if self.prevState:
            table = [self.prevState, st]
        else:
            table = [st, st]
        oldTable = np.reshape(table, (-1, self.dim, self.dim, 2))

        table = np.reshape([oldState.table, state.table], (-1, self.dim, self.dim, 2))

        self.memory.append((oldTable, action, rew, table, done))
        self.prevState = oldState.table
        self.replay()
        if done:
            self.lastUpdate += 1
            if self.lastUpdate > self.updatePeriod :
                self.updateTargetModel()
                self.lastUpdate = 0

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

        targets = rewards + self.gamma*(np.amax(self.targetModel.predict(next_states), axis=1))*(1-dones)

        targets_full = self.targetModel.predict(states)

        ind = np.array(list(range(self.batch_size)))
        targets_full[[ind], [actions]] = targets
        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    @classmethod
    def load(cls, dim, model_path):
        agent = cls(dim)
        path = model_path+"Size"+str(dim)
        agent.model = load_model(path)
        agent.updateTargetModel()
        return agent

    def save(self, model_path = None):
        if not model_path:
            model_path = ".\\models\\deepQModel"
        path = model_path + "Size" + str(self.dim)
        self.model.save(path)