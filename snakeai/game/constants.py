from enum import Enum, auto
import math
from dataclasses import dataclass


@dataclass
class Coords:
    """A class for representing coordinates

    Casting to string a `Coords` object will return the string *(x, y)*
    Summing two coordinates together will do the element-wise sum.
    Two `Coords` objects can also be compared for equality.

    Parameters
    -------------
    x : int
    y : int

    Attributes
    --------------
    x : int
        The x coordinate
    y : int
        The y coordinate
    """
    x: int
    y: int

    def __add__(self, other: 'Coords') -> 'Coords':
        if not isinstance(other, Coords):
            raise TypeError("It is not a Coord object")
        return Coords(self.x+other.x, self.y+other.y)

    def manhattan_distance(self, other: 'Coords') -> int:
        """Calculate manhattan distance between this position and the other

        Parameters
        -----------
        other : Coords
            the other coordinates

        Returns
        -----------
        int
            the distance

        Raises
        -------------
        TypeError
            if `other` is not of type `Coords`

        """
        if not isinstance(other, Coords):
            raise TypeError("It is not a Coord object")
        return abs(self.x - other.x) + abs(self.y - other.y)

    def distance(self, other: 'Coords') -> float:
        """Calculate distance between two coordinates

        Parameters
        -----------
        other : Coords
            the other coordinates

        Returns
        --------
        float
            the distance

        Raises
        -------
        TypeError
            if `other` is not of type `Coords`
        """
        if not isinstance(other, Coords):
            raise TypeError("It is not a Coord object")
        return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2)


class Actions(Enum):
    """The actions that can be chosen to move the snake"""
    UP = Coords(0, -1)
    DOWN = Coords(0, 1)
    LEFT = Coords(-1, 0)
    RIGHT = Coords(1, 0)


class Rewards(Enum):
    """The possible rewards values

    The isGameOver method can be used to check if a reward is a game over value
    """
    GOT_APPLE = 100
    FAILED = -100
    ENDED = 100
    CLOSER = 1
    AWAY = -1

    @classmethod
    def is_game_over(cls, rew: 'Rewards') -> bool:
        """Check if a reward is given at game over

        Parameters
        ------------
        rew : Rewards
            The reward to check

        Returns
        ----------
        Bool
            Whether is game over or not
        """
        return rew in [cls.FAILED, cls.ENDED]


class GUIMode(Enum):
    """How the GUI should be displayed"""
    WINDOW = auto()
    CLI = auto()
    NO_SHOW = auto()
