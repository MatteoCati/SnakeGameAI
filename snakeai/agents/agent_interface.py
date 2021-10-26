from snakeai.game.constants import Actions
from abc import ABC, abstractmethod

from snakeai.game.memento import FrozenState


class AbstractAgent(ABC):
    """Abstract interface for all agents

    Parameters
    -------------
    dim : int
        the side of the board
    initial_epsilon : float [0,1]
        The initial probability of choosing an action at random

    Attributes
    ----------------
    dim : int
        The side of the board
    epsilon : float [0,1]
        The probability of choosing an action at random
    """
    MIN_EPSILON = 0.0001

    def __init__(self, dim: int, initial_epsilon: int = 1):
        self.dim = dim
        self.epsilon = initial_epsilon

    @abstractmethod
    def execute(self, state: FrozenState) -> Actions:
        """Get the next action to do, given the state

        Parameters
        --------------
        state : FrozenState
            The current state of the game

        Returns
        --------------
        Actions
            the direction in which  to move
        """

    @abstractmethod
    def fit(self, old_state: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """Train the agent with data for a single step

        Parameters
        -----------
        old_state : FrozenState
            The state before taking the action
        action : Actions
            The action taken
        rew : int
            The reward obtained
        state : FrozenState
            The state after taking the action
        done : bool
            Whether the new state is terminal
        """

    def reset(self):
        """Prepare the agent for starting a new game"""

    @abstractmethod
    def save(self, model_path: str = None):
        """Save the model. If no path is given, a default path will be used.

        Parameters
        -----------
        model_path: str, optional
            the custom path where the model should be saved
        """

    @classmethod
    @abstractmethod
    def load(cls, dim: int, model_path: str):
        """Load the model from a specified path.

        Parameters
        -----------
        dim : int
            The side of the board for the game
        model_path: str
            the path to the model that must be loaded
        """
