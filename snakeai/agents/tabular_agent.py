from snakeai.game.constants import Actions
import pickle
import random
from snakeai.agents.agent_interface import AbstractAgent
import bz2
from collections import defaultdict

class StateAgent(AbstractAgent):
    """A class for an agent that uses a tabular method

    All Q values for the states are recorded. The agent chooses the action that maximizes Q.
    States are representeed as a string with all the positions of the snake plus the position of the apple.

    Parameters
    -------------
    dim : int
        the side of the board
    epsilon : float, default=1
        the initial value for epsilon

    Attributes
    ----------------
    stateDict : dict
        The dictionar that stores Q values
    GAMMA : float [0, 1]
        the gamma value for training
    STEP : float [0, 1]
        the step size
    EPSILON: float [0, 1]
        the epsilon value for epsilon-greedy
    DECAY : float [0, 1)
        the decay rate for epsilon
    MIN_EPSILON : float [0, 1]
        the minimum value for epsilon when decaying
    """
    def __init__(self, dim, epsilon = 1):
        super().__init__(dim)
        self.stateDict = defaultdict(self.defaultValue)
        self.reset()
        self.GAMMA = 0.995
        self.STEP = 0.6
        self.EPSILON = epsilon
        self.DECAY = 0.999
        self.MIN_EPSILON = 0.01
    
    def defaultValue(self):
        """The default Value for the Q 
        
        Returns
        --------
        list(float)
            The default value"""
        return [2,2,2,2]

    def reset(self):
        self.prevAction = 1
        
    def execute(self, state):
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
        action = self.stateDict[state].index(max(self.stateDict[state]))
        if random.random() < self.EPSILON:
            action = random. choice([0,1,2,3])
        self.prevAction = action
        if action == 0:
            return Actions.UP
        elif action == 1:
            return Actions.DOWN
        elif action == 2:
            return Actions.LEFT
        else:
            return  Actions.RIGHT 
    
    def fit(self, oldState, action, rew, state, done):
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
            self.stateDict[oldState][self.prevAction] = self.stateDict[oldState][self.prevAction] +\
                            self.STEP * (rew + self.GAMMA*max(self.stateDict[nextState]) - self.stateDict[oldState][self.prevAction])
        else:
            self.stateDict[oldState][self.prevAction] = self.stateDict[oldState][self.prevAction] +\
                            self.STEP * (rew - self.stateDict[oldState][self.prevAction])
            if(self.EPSILON > self.MIN_EPSILON):
                self.EPSILON *= self.DECAY
    
    def save(self, title = "StateAgentDictionary"):
        """Save the states of the agent
        
        Parameters
        ------------
        title : str, default=StateAgentDictionary
            the name of the file to be saved"""
        with bz2.BZ2File(title + str(self.dim)+".pbz2", "w") as f: 
            pickle.dump(self.stateDict, f)

    def load(self, title = "StateAgentDictionary"):
        """Loads the states of the agent
        
        Parameters
        ------------
        title : str, default=StateAgentDictionary
            the name of the file to be loaded
            
        Raises
        -------
        TypeError 
            If the data in the file is not a dict or a defauldict    
        """
        data = bz2.BZ2File(title + str(self.dim) + ".pbz2", "rb")
        dt = pickle.load(data)
        if type(dt) == dict:
            self.stateDict = defaultdict(self.defaultValue, dt)
        elif type(dt) == defaultdict:
            self.stateDict = dt
        else:
            raise TypeError("The file should contain a dict or a defaultdict")
        print("loaded", len(self.stateDict), "states")


