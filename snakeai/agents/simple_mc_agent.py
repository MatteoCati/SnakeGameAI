import logging
import pickle
import random
import bz2
import time
from collections import defaultdict
from snakeai.game.constants import Actions
from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.memento import FrozenState
from snakeai.game.agent_controller import AgentGame


def play(size: int = 20, model_path: str = None, fps: int = 7):
    """Play with an already trained `SimpleMCAgent`

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
        model_path = "./models/default/DefaultSimpleMCAgent"
        size = 20
    agent = SimpleMCAgent.load(size, model_path)
    agent.epsilon = 0
    game = AgentGame(size, fps=fps, replay_allowed=True)
    game.play(agent)


class SimpleMCAgent(AbstractAgent):
    """A class for an agent that uses a monte carlo method, with simplified states.

    All Q values for the states are recorded. The agent chooses the action that maximizes Q.
    The values are updated only at the end of the episode.

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
        self.state_dict = defaultdict(self.default_value)
        self.count_dict = defaultdict(self.default_count)
        self.reset()

    @staticmethod
    def default_value():
        """list : The default Value for Q"""
        return [2, 2, 2, 2].copy()

    @staticmethod
    def default_count():
        """list : The default Value for N"""
        return [0, 0, 0, 0].copy()

    def reset(self):
        self.prev_action = 1
        self.current_episode = []

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
            action = random.choice([0, 1, 2, 3])
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
        self.current_episode.append(old_state.simple_state_string)
        if action == Actions.UP:
            action_num = 0
        elif action == Actions.DOWN:
            action_num = 1
        elif action == Actions.LEFT:
            action_num = 2
        else:
            action_num = 3
        self.current_episode.append(action_num)
        self.current_episode.append(rew)
        if done:
            self.replay()
            if self.epsilon > self.MIN_EPSILON:
                self.epsilon *= self.DECAY

    def replay(self):
        """Replay the episode and learn the new values for Q"""
        g = 0
        for i in range(len(self.current_episode) - 3, -1, -3):
            g = self.GAMMA * g + self.current_episode[i + 2]
            state = self.current_episode[i]
            action = self.current_episode[i + 1]
            self.count_dict[state][action] += 1
            self.state_dict[state][action] = self.state_dict[state][action] + \
                                             (1 / self.count_dict[state][action]) * (g - self.state_dict[state][action])

    def save(self, model_path: str = None):
        """Save the states values of the agent. If a path is not given, uses a default one.

        Parameters
        ------------
        model_path : str, optional
            the position where the agent must be saved
        """
        start = time.time()
        if not model_path:
            model_path = "./models/SimpleMonteCarloModel"
        with bz2.BZ2File(model_path + str(self.dim) + ".pbz2", "w") as fout:
            pickle.dump((dict(self.state_dict), dict(self.count_dict)), fout)
        logging.info(f"Saved  {len(self.state_dict)} states in {time.time() - start :.2f} s")

    @classmethod
    def load(cls, dim: int, model_path: str) -> 'SimpleMCAgent':
        """Create a new agent from the given file

        Parameters
        -----------
        dim : int
            The size of the board
        model_path: str
            The path from which the agent is loaded

        Raises
        -------
        TypeError
            If the data in the file is not of type dict
        """
        start = time.time()
        agent = cls(dim)
        data = bz2.BZ2File(model_path + str(dim) + ".pbz2", "rb")
        data, counter = pickle.load(data)
        if not (isinstance(data, dict) and isinstance(counter, dict)):
            raise TypeError("The file should contain two dictionaries")
        agent.state_dict = defaultdict(agent.default_value, data)
        agent.count_dict = defaultdict(agent.default_count, counter)
        logging.info(f"loaded {len(agent.state_dict)} states in {time.time() - start :.2f} s")
        return agent
