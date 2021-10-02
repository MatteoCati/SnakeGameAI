from snakeai.game.constants import Actions
from abc import ABC, abstractmethod, abstractclassmethod

from snakeai.game.memento import FrozenState


class AbstractAgent(ABC):
    """Abstract interface for all agents

    Parameters
    -------------
    dim : int
        the side of the board

    Attributes
    ----------------
    dim : int
        The side of the board
    """
    def __init__(self, dim: int):
        self.dim = dim


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

        Raises
        ------------
        NotImplementedError
            This method must always be overridden
        """


    @abstractmethod
    def fit(self, oldState: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """Train the agent with data for a single step

        Parameters
        -----------
        oldState : FrozenState
            The state before taking the action
        action : Actions
            The action taken
        rew : int
            The reward obtained
        state : FrozenState
            The state after taking the action
        done : bool
            Whether the new state is terminal

        Raises
        ----------
        NotImplementedError
            This method must always be overridden"""


    def reset(self):
        """Prepare agent for starting a new game"""

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
