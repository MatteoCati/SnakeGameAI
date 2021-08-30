from snakeai.game.view import GameGUI, cliGUI
from snakeai.game.model import Snake
from snakeai.game.constants import Actions
import time

class UserGame():
    """The class for controlling the game when played by the user
    
    Parameters
    --------------
    dim : int, default=20
        the side of the board
    fps : int, default=3
    closeOnFail : Bool, default=False
        whether the game should close immediately at game over
    mode : str {window, cli}
        The type of interface

    Attributes
    --------------
    model : Snake
        The model for the game
    view : GameGUI
        The GUI for the game
    frameTime : float
        The duration of each frame in seconds
    closeOnFail : Bool
        Whether the game should close immediately at game over
    """
    def __init__(self, dim = 20, fps = 3, closeOnFail = False, mode="window"):
        self.model = Snake(dim)
        if mode == "cli":
            self.view = cliGUI()
        else:
            self.view = GameGUI()
        self.frameTime = 1/fps
        self.closeOnFail = closeOnFail
    
    def start(self):
        """Start the game"""
        start = time.time()
        self.model.reset()
        self.view.initScreen(self.model.dim, self.model.snake, self.model.apple, self.model.score)
        time.sleep(max(0, self.frameTime - (time.time()-start)))
    
    def quit(self):
        """Quit the game"""
        self.view.quit()

    def waitForQuit(self):
        """Wait until the game can be quitted"""
        if self.closeOnFail:
            self.quit()
            return
        a = ""
        while a != "QUIT":
            a = self.view.getInput()
        self.quit()
    
    def step(self):
        """Execute one step (frame) of the game"""
        start = time.time()
        act = self.view.getInput()
        if act == "QUIT":
            self.quit()
            raise SystemExit
        if act:
            self.model.changeDirection(act)
        self.model.step()
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.isGameOver)
        time.sleep(max(0, self.frameTime - (time.time()-start)))
    
    def play(self):
        """Play a complete game"""
        self.start()
        while not self.model.isGameOver:
            self.step()
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.isGameOver)
        self.waitForQuit()

    


