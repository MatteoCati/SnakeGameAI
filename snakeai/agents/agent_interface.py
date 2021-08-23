from snakeai.game.constants import Actions 

class AbstractAgent():
    """Abstract interface for all agents

    Parameters
    -------------
    dim : int
        the side of the board
    
    Attributes
    ----------------
    dim : int
        the side of the board
    """

    def __init__(self, dim):
        self.dim = dim

    def execute(self, snake, apple) -> Actions:
        """Get the next action to do, given the state
        
        Parameters
        --------------
        snake : list(Coords)
            the position of the snake
        apple : Coords
            the position of the apple
        
        Returns
        --------------
        Actions
            the direction in which  to move
        
        Raises
        ------------
        NotImplementedError
            This method should always be overriden
        """
        raise NotImplementedError
    
    def fit(self, oldSnake, oldApple, rew, snake, apple, done):
        """Train the agent with data for a single step
        
        Parameters
        -----------
        oldSnake : list(Coords)
            The initial snake
        oldApple : Coords
            The initial position of the apple
        rew : int
            The reward obtained
        snake : list(Coords)
            The new snake
        apple : Coords
            The new position of the apple
        done : bool
            Whether the new state is terminal
        
        Raises
        ----------
        NotImplementedError
            This method must be overridden"""
        raise NotImplementedError
    
    def reset(self):
        """Prepare agent for starting a new game"""
        pass