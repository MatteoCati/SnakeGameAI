import logging
import pickle as pkl
import random
import bz2
import time
from collections import defaultdict
from snakeai.game.constants import Actions
from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.memento import FrozenState
from snakeai.game.agent_controller import AgentGame


def play(size: int = 20, model_path: str = None, fps: int = 7):
    """Play with an already trained `SimpleStateAgent`

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
        model_path = "./models/default/DefaultSimpleStateAgent"
        size = 20
    agent = SimpleStateAgent.load(size, model_path)
    agent.epsilon = 0
    game = AgentGame(size, fps=fps, replay_allowed=True)
    game.play(agent)


class SimpleStateAgent(AbstractAgent):
    """A class for an agent that uses a tabular method, with simplified states.

    All Q values for the states are recorded. The agent chooses the action that maximizes Q.

    Parameters
    -------------
    dim : int
        the side of the board

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

    def __init__(self, dim: int):
        super().__init__(dim)
        self.state_dict = defaultdict(lambda: self.default_value)
        self.reset()

    @property
    def default_value(self):
        """list : The default Value for Q"""
        return [2, 2, 2, 2].copy()

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
        state = state.simple_state_string
        action = self.state_dict[state].index(max(self.state_dict[state]))
        if random.random() < self.epsilon:
            action = random. choice([0, 1, 2, 3])
        self.prev_action = action
        if action == 0:
            return Actions.UP
        if action == 1:
            return Actions.DOWN
        if action == 2:
            return Actions.LEFT
        return Actions.RIGHT

    def fit(self, old_state: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """Update the Q values

        Parameters
        -----------
        old_state : FrozenState
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
        old_state = old_state.simple_state_string
        next_state = state.simple_state_string
        if not done:
            self.state_dict[old_state][self.prev_action] = self.state_dict[old_state][self.prev_action] + \
                                                           self.STEP * (rew + self.GAMMA * max(self.state_dict[next_state]) -
                                                                        self.state_dict[old_state][self.prev_action])
        else:
            self.state_dict[old_state][self.prev_action] = self.state_dict[old_state][self.prev_action] + \
                                                           self.STEP * (rew - self.state_dict[old_state][self.prev_action])
            if self.epsilon > self.MIN_EPSILON:
                self.epsilon *= self.DECAY

    def save(self, model_path: str = None):
        """Save the states of the agent. If a path is not given, uses a default one.

        Parameters
        ------------
        model_path : str, optional
            the position where the agent must be saved
        """
        start = time.time()
        if not model_path:
            model_path = "./models/SimpleStateAgent"
        with bz2.BZ2File(model_path + str(self.dim) + ".pbz2", "w") as fout:
            pkl.dump(dict(self.state_dict), fout)
        logging.info(f"Saved  {len(self.state_dict)} states in {time.time() - start :.2f} s")

    @classmethod
    def load(cls, dim: int, model_path: str) -> 'SimpleStateAgent':
        """Create a new agent from the given file

        Parameters
        -----------
        dim : int
            The size of the board
        model_path: str
            The path to the model to load
        Raises
        -------
        TypeError
            If the data in the file is not a `dict` or `defaultdict`
        """
        start = time.time()
        agent = cls(dim)
        data = bz2.BZ2File(model_path + str(dim) + ".pbz2", "rb")
        data = pkl.load(data)
        if isinstance(data, dict):
            agent.state_dict = defaultdict(lambda: agent.default_value, data)
        elif isinstance(data, defaultdict):
            agent.state_dict = data
        else:
            raise TypeError("The file should contain a dict or a defaultdict")
        logging.info(f"loaded {len(agent.state_dict)} states in {time.time() - start :.2f} s")
        return agent
