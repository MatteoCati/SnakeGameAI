import sys
import time

from snakeai.game.constants import GUIMode
from snakeai.game.view import generate_view
from snakeai.game.model import Snake


class UserGame:
    """The class for controlling the game when played by the user

    Parameters
    --------------
    dim : int, default=20
        the side of the board
    fps : int, default=3
    mode : str {window, cli}
        The type of interface

    Attributes
    --------------
    model : Snake
        The model for the game
    view : GameGUI
        The GUI for the game
    frame_time : float
        The duration of each frame in seconds
    is_first_game : bool
        Whether the GUI should be initialized
    """

    def __init__(self, dim: int = 20, fps: int = 3, mode: GUIMode = GUIMode.WINDOW):
        self.model = Snake(dim)
        self.view = generate_view(mode)
        self.frame_time = 1 / fps
        self.is_first_game = True

    def wait_end_of_frame(self, elapsed: float):
        """Wait until the time elapsed is at least `frame_time`

        Parameters
        -----------
        elapsed: float
            the time elapsed since the start of the current frame"""
        time.sleep(max(0.0, self.frame_time - elapsed))

    def start(self):
        """Start the game"""
        start = time.time()
        self.model.reset()
        if self.is_first_game:
            self.is_first_game = False
            self.view.init_screen(self.model.dim, self.model.snake, self.model.apple,
                                  self.model.score, self.model.highScore)
        else:
            self.view.updateUI(self.model.snake, self.model.apple, self.model.score,
                               self.model.highScore)
        self.wait_end_of_frame(time.time() - start)

    def quit(self):
        """Quit the game and close the program"""
        self.view.quit()
        sys.exit()

    def wait_for_quit(self):
        """Wait until the user decide to quit"""
        while True:
            action = self.view.get_input()
            if action == "QUIT":
                self.quit()
                return
            if action == "REPLAY":
                self.play()

    def step(self):
        """Execute one step (frame) of the game"""
        start = time.time()
        act = self.view.get_input()
        if act == "QUIT":
            self.quit()
        if act and act != "REPLAY":
            self.model.change_direction(act)
        self.model.step()
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score,
                           self.model.highScore, self.model.isGameOver)
        self.wait_end_of_frame(time.time() - start)

    def play(self):
        """Play a complete game"""
        self.start()
        while not self.model.isGameOver:
            self.step()
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score,
                           self.model.highScore, self.model.isGameOver)
        self.wait_for_quit()
