import random
from collections import deque
import numpy as np
from keras.layers import Dense
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from snakeai.game.constants import Actions
from snakeai.agents.agent_interface import AbstractAgent
from tensorflow.keras.models import load_model

from snakeai.game.memento import FrozenState
from snakeai.game.agent_controller import AgentGame


def play(size: int = 20, model_path: str = None, fps: int = 7):
    """Play with an already trained `DQN`

    If no path is given, a default (pre-trained) model will be used

    Parameters
    ------------
    size: int, default=20
        the size of the board
    model_path: str, optional
        the path to the trained model to load
    fps: int, default=7
        The number of fps for the game
    """
    if not model_path:
        model_path = "./models/default/SimpleDeepAgent"
        size = 20
    agent = DQN.load(size, model_path)
    game = AgentGame(size, replay_allowed=True, fps=fps)
    agent.epsilon = 0
    game.play(agent)


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
    GAMMA : float [0, 1]
        The discount factor
    batch_size : int
        The dimension of each batch for training
    MIN_EPSILON : float [0, 1]
        The minimum value for epsilon
    EPSILON_DECAY : float [0, 1)
        The decay factor of epsilon at each episode
    learning_rate : float [0, 1]
        The learning rate
    memory : deque
        The list of states used for learning
    model : keras.Model
        The neural network used by the agent
    """

    EPSILON_DECAY = 0.995
    GAMMA = 0.95

    def __init__(self, dim: int):
        super().__init__(dim)
        self.action_space = 4
        self.state_space = 12
        self.batch_size = 500
        self.learning_rate = 0.00025
        self.memory = deque(maxlen=2500)
        self.model = self.build_model()

    def build_model(self) -> keras.Model:
        """Create The Deep Learning model"""
        inputs = keras.Input((self.state_space,))
        x = Dense(128, activation="relu")(inputs)
        x = Dense(128, activation="relu")(x)
        x = Dense(128, activation="relu")(x)
        outputs = layers.Dense(self.action_space, activation="softmax", name="output")(x)
        model = keras.Model(inputs=inputs, outputs=[outputs])
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss="mse")
        return model

    def execute(self, state: FrozenState) -> Actions:
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
        state = np.reshape(state.simple_state, (1, self.state_space))
        if np.random.rand() <= self.epsilon:
            act = random.randrange(self.action_space)
        else:
            act_values = self.model.predict(state)
            act = np.argmax(act_values[0])
        if act == 0:
            return Actions.UP
        if act == 1:
            return Actions.RIGHT
        if act == 2:
            return Actions.DOWN
        return Actions.LEFT

    def fit(self, old_state: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """Add the current step to the memory and train the model

        Parameters
        ------------
        old_state : FrozenState
            The state of the game before taking the action
        action : Actions
            The action chosen
        rew : int
            The reward obtained after taking the action
        state : FrozenState
            The state after taking the action
        done : bool
            Whether the state is terminal 
        """
        action = [Actions.UP, Actions.RIGHT, Actions.DOWN, Actions.LEFT].index(action)
        old_state = np.reshape(old_state.simple_state, (1, self.state_space))
        state = np.reshape(state.simple_state, (1, self.state_space))
        self.memory.append((old_state, action, rew, state, done))
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

        targets = rewards + self.GAMMA * (np.amax(self.model.predict(next_states), axis=1)) * (1 - dones)
        targets_full = self.model.predict(states)

        ind = np.array(list(range(self.batch_size)))
        targets_full[[ind], [actions]] = targets
        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.epsilon > self.MIN_EPSILON:
            self.epsilon *= self.EPSILON_DECAY

    def save(self, model_path: str = None):
        """Save the model to a file. if no path is given, it uses a default one."""
        if not model_path:
            model_path = "./models/SimpleDeepModel"
        self.model.save(model_path)

    @classmethod
    def load(cls, dim: int, model_path: str) -> 'DQN':
        """Create a new agent from the given file."""
        agent = cls(dim)
        agent.model = load_model(model_path)
        return agent
