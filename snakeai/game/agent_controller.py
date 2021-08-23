from snakeai.game.model import Snake
from snakeai.game.view import GeneralView, GameGUI
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
    closeOnFail : Bool default=True
        whether the game should close immediately at game over

    Attributes
    --------------
    model : Snake
        The model for the game
    view : GeneralView
        The GUI for the game 
    frameTime : float
        The duration of each frame in seconds (if show is set to True)
    closeOnFail : Bool
        Whether the game should close immediately at game over
    """
    def __init__(self, dim = 20, fps = 7, show = True, closeOnFail = True):
        self.model = Snake(dim)
        self.frameTime = 1/fps
        if not show: closeOnFail = True
        if show:
            self.view = GameGUI()
        else:
            self.view = GeneralView()
            self.frameTime = 0
        self.closeOnFail = closeOnFail
    
    def start(self):
        """Start the game
        
        Returns
        ---------
        list of Coords
            The position of the snake
        Coords
            The position of the apple
        """
        super().start()
        return self.model.snake, self.model.apple

    def step(self, action):
        """Execute one step (frame) of the game
        
        Parameters
        ------------
        action : Actions
            the direction in which to move

        Returns
        ------------
        list(Coords)
            The coordinates of the old snake
        Coords
            The coordinates of the old apple
        int
            The reward obtained
        list(Coords)
            The coordinates of the new snake
        Coords
            The coordinates of the new apple
        Bool
            True if the new state is terminal, False otherwise
        """
        start = time.time()
        q = self.view.getInput()
        if q == "QUIT":
            self.quit()
            raise SystemExit
        self.model.changeDirection(action)
        snake = self.model.snake
        apple = self.model.apple
        rew = self.model.step()
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.isGameOver)
        time.sleep(max(0, self.frameTime - (time.time()-start)))
        return snake, apple, rew.value, self.model.snake, self.model.apple, self.model.isGameOver
    
    def play(self, agent):
        """Play a complete game
        
        Parameters
        ------------
        agent : AbstractAgent
            The agent that will play the game"""
        snake, apple = self.start()
        agent.reset()
        done = False
        rew = None
        while not self.model.isGameOver:
            action = agent.execute(snake, apple)
            oldSnake, oldApple, rew, snake, apple, done = self.step(action)
            agent.fit(oldSnake, oldApple, rew, snake, apple, done)
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.isGameOver)
        self.waitForQuit()
