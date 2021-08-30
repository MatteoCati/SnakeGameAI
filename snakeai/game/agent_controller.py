from snakeai.game.model import Snake
from snakeai.game.view import GeneralView, GameGUI, cliGUI
from snakeai.game.constants import Actions, Rewards
from snakeai.game.user_controller import UserGame
import time

class AgentGame(UserGame):
    """The class for controlling the game when played by an agent
    
    Parameters
    --------------
    dim : int, default=20
        the side of the board
    fps : int, default=7
        the number of fps
    show : Bool, deafult=True
        Whether to show the GUI or not
    replayAllowed : Bool, default=False
        whether the game should wait for replay after game over
    mode : str {window, cli}, default="window"
        The type of interface

    Attributes
    --------------
    model : Snake
        The model for the game
    view : GeneralView
        The GUI for the game 
    frameTime : float
        The duration of each frame in seconds (if show is set to True)
    replayAllowed : bool
        Whether the game should close immediately at game over
    toInit : bool
        Whether the GUI should be initialized
    """
    def __init__(self, dim = 20, fps = 7, show = True, replayAllowed = False, mode = "window"):
        self.model = Snake(dim)
        self.frameTime = 1/fps
        self.toInit = True
        if not show: replayAllowed = False
        if show:
            if mode == "cli":
                self.view = cliGUI()
            else:
                self.view = GameGUI()
        else:
            self.view = GeneralView()
            self.frameTime = 0
        self.replayAllowed = replayAllowed
    
    def start(self):
        """Start the game
        
        Returns
        ---------
        FrozenState
            The state at the beginning of the game
        """
        super().start()
        return self.model.state

    def step(self, action):
        """Execute one step (frame) of the game
        
        Parameters
        ------------
        action : Actions
            the direction in which to move

        Returns
        ------------
        FrozenState
            The state before the step
        int
            The reward obtained
        FrozenState
            The state after the step
        Bool
            True if the new state is terminal, False otherwise
        """
        start = time.time()
        q = self.view.getInput()
        if q == "QUIT":
            self.quit()
            raise SystemExit
        oldState = self.model.state
        self.model.changeDirection(action)
        snake = self.model.snake
        apple = self.model.apple
        rew = self.model.step()
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.highScore, self.model.isGameOver)
        time.sleep(max(0, self.frameTime - (time.time()-start)))
        return oldState, rew.value, self.model.state, self.model.isGameOver
    
    def reset(self):
        if self.closeOnFail:
            self.quit()

    def play(self, agent= None):
        """Play a complete game
        
        Parameters
        ------------
        agent : AbstractAgent, optional
            The agent that will play the game. If not initialized, the program rais ean error
            
        Raises
        -------
        AttributeError
            If the agent is not set
        """
        if agent:
            self.agent = agent
        if not self.agent:
            raise AttributeError("Agent has not been given")
        
        state = self.start()
        self.agent.reset()
        done = False
        rew = None
        while not self.model.isGameOver:
            action = self.agent.execute(state)
            oldState, rew, state, done = self.step(action)
            self.agent.fit(oldState, action, rew, state, done)
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.highScore, self.model.isGameOver)
        time.sleep(self.frameTime)
        if self.replayAllowed:
            self.waitForQuit()
