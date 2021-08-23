from enum import Enum

class Coords():
    """A class for representing coordinates
    
    Cating to string a Coords object will return the string *(x, y)*
    Summing two coordinates together will do the element-wise sum.
    Two Coords object can also be compared for equality. 

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
    def __init__(self, x, y):
        self. x = x
        self.y = y
    
    def __add__(self, other):
        if type(other) != type(self):
            raise TypeError("It is not a Coord object")
        return Coords(self.x+other.x, self.y+other.y)
    
    def __str__(self) -> str:
        return "(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __repr__(self) -> str:
        return "Coords(" + str(self.x) + ", " + str(self.y) + ")"
    
    def __eq__(self, o: object) -> bool:
        if type(o) != type(self):
            return False
        return o.x == self.x and o.y == self.y
    
    def distance(self, other):
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
            if `other` is not of type Coords
        
        """
        if type(other) != type(self):
            raise TypeError("It is not a Coord object")
        return abs(self.x - other.x) + abs(self.y - other.y)

class Actions(Enum):
    """The actions that can be chosen"""
    UP = Coords(0, -1)
    DOWN = Coords(0, 1)
    LEFT = Coords(-1, 0)
    RIGHT = Coords(1, 0)

class Rewards(Enum):
    """The possible rewards values
    
    The isGameOver method can e used to check if a reward is a game over value"""
    GOT_APPLE = 10
    FAILED = -100
    ENDED = 100
    CLOSER = -1
    AWAY = -1

    @classmethod
    def isGameOver(cls, rew):
        """Check if a reward is considered game over
        
        Parameters
        ------------
        rew : Rewards
            The rewards to check
        
        Returns
        ----------
        Bool 
            Whether is game over or not
        """
        return rew in [cls.FAILED, cls.ENDED]
