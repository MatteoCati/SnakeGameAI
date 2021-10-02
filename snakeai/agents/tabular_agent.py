import logging
import pickle
import random
import bz2
from collections import defaultdict
from snakeai.game.constants import Actions
from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.memento import FrozenState


class StateAgent(AbstractAgent):
    """A class for an agent that uses a tabular method

    All Q values for the states are recorded. The agent chooses the action that maximizes Q.
    States are represented as a string with all the positions of the snake plus the position
    of the apple.

    Parameters
    -------------
    dim : int
        the side of the board
    start_epsilon : float, default=1
        the initial value for epsilon

    Attributes
    ----------------
    state_dict : dict
        The dictionary that stores Q values
    GAMMA : float [0, 1]
        the gamma value for training
    STEP : float [0, 1]
        the step size
    epsilon: float [0, 1]
        the epsilon value for epsilon-greedy
    DECAY : float [0, 1)
        the decay rate for epsilon
    MIN_EPSILON : float [0, 1]
        the minimum value for epsilon when decaying
    """
    GAMMA = 0.995
    STEP = 0.6
    DECAY = 0.999
    MIN_EPSILON = 0.01

    def __init__(self, dim: int, start_epsilon: float = 1):
        super().__init__(dim)
        self.state_dict = defaultdict(lambda : self.default_value)
        self.reset()
        self.epsilon = start_epsilon

    @property
    def default_value(self):
        """list : The default Value for Q"""
        return [2,2,2,2].copy()

    def reset(self):
        self.prev_action = 1

    def execute(self, state: FrozenState) -> Actions:
        """Get the next action to do, given the state

        Parameters
        --------------
        state : FrozenState
            the current state of the game

        Returns
        --------------
        Actions
            the direction in which  to move
        """
        state = state.tableString
        action = self.state_dict[state].index(max(self.state_dict[state]))
        if random.random() < self.epsilon:
            action = random. choice([0,1,2,3])
        self.prev_action = action
        if action == 0:
            return Actions.UP
        if action == 1:
            return Actions.DOWN
        if action == 2:
            return Actions.LEFT
        return  Actions.RIGHT

    def fit(self, oldState: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """Update the Q values

        Parameters
        -----------
        oldState : FrozenState
            the state of the game before taking the action
        action : Actions
            The action taken
        rew : int
            The reward obtained
        state : FrozenState
            the state of the game after taking the action
        done : bool
            Whether the new state is terminal
        """
        oldState = oldState.tableString
        nextState = state.tableString
        if not done:
            self.state_dict[oldState][self.prev_action] = self.state_dict[oldState][self.prev_action] + \
                                                          self.STEP * (rew + self.GAMMA * max(self.state_dict[nextState]) -
                                                                       self.state_dict[oldState][self.prev_action])
        else:
            self.state_dict[oldState][self.prev_action] = self.state_dict[oldState][self.prev_action] + \
                                                          self.STEP * (rew - self.state_dict[oldState][self.prev_action])
            if self.epsilon > self.MIN_EPSILON :
                self.epsilon *= self.DECAY

    def save(self, model_path: str = None):
        """Save the states of the agent. If a path is not given, uses a default one.

        Parameters
        ------------
        model_path : str, optional
            the position where the agent must be saved
        """
        if not model_path:
            model_path = ".\\models\\StateAgentDictionary"
        with bz2.BZ2File(model_path + str(self.dim) + ".pbz2", "w") as fout:
                pickle.dump(dict(self.state_dict), fout)

    @classmethod
    def load(cls, dim: int, model_path: str) -> 'StateAgent':
        """Create a new agent from the given file

        Raises
        -------
        TypeError
            If the data in the file is not a dict or defaultdict
        """
        agent = cls(dim)
        data = bz2.BZ2File(model_path + str(dim) + ".pbz2", "rb")
        data = pickle.load(data)
        if isinstance(data, dict):
            agent.state_dict = defaultdict(lambda : agent.default_value, data)
        elif isinstance(data, defaultdict):
            agent.state_dict = data
        else:
            raise TypeError("The file should contain a dict or a defaultdict")
        logging.info("loaded", len(agent.state_dict), "states")
        return agent
