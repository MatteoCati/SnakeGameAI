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

    def execute(self, state) -> Actions:
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
            This method must always be overriden
        """
        raise NotImplementedError
    
    def fit(self, oldState, action, rew, state, done):
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
        raise NotImplementedError
    
    def reset(self):
        """Prepare agent for starting a new game"""
        pass