import time
from typing import Union
import pickle as pkl

from snakeai.game.agent_controller import AgentGame
from snakeai.game.constants import Actions, GUIMode
from snakeai.game.user_controller import UserGame


class Recorder(AgentGame):
    """This class will record the game played by the agent, as a list of tuple(state, action)

    Note that for this to work properly, you should use a new recorder for each game"""

    def __init__(self, dim, show):
        self.recorded = []
        self.dim = dim
        super().__init__(dim, show=show)

    @property
    def recording(self):
        """list((Coords, Action)): The list of state actions played"""
        return self.recorded.copy()

    def start(self):
        state = super().start()
        self.recorded.append((state.apple, state.direction))
        return state

    def step(self, action: Union[Actions, str]):
        old_state, rew, state, isGameOver = super().step(action)
        self.recorded.append((state.apple, state.direction))
        return old_state, rew, state, isGameOver

    def save(self, path: str):
        """Save the recorded game on file

        Parameters
        -----------
        path: str
            the path were the game is save. ends with .pkl

        Raises
        -------
        TypeError
            If the file has not the .pkl extension
        """
        if path[-4:] != ".pkl":
            raise TypeError("The file should have .pkl extension")
        with open(path, "wb") as fout:
            pkl.dump((self.dim, self.show, self.recorded), fout)

    @classmethod
    def load(cls, path: str):
        """Load a recorded game from file

        Parameters
        -----------
        path: str
            the path were the game is saved. Ends with .pkl

        Raises
        -------
        TypeError
            If the file has not the .pkl extension
        """
        if path[-4:] != ".pkl":
            raise TypeError("The file should have .pkl extension")
        with open(path, "rb") as fin:
            dim, show, recorded = pkl.load(fin)
        rec = cls(dim, show)
        rec.recorded = recorded
        return rec


class Player(UserGame):
    def __init__(self, recorder: Recorder, mode: GUIMode = GUIMode.WINDOW):
        self.recording = recorder.recording
        super().__init__(recorder.dim, mode=mode)
        self.index = 0

    def step(self):
        """Execute one step (frame) of the game"""
        start = time.time()
        self.index += 1
        apple, act = self.recording[self.index]
        if act == "QUIT":
            self.quit()
        if act and act != "REPLAY":
            self.model.change_direction(act)
        self.model.step()
        self.model.apple = apple
        self.view.updateUI(self.model.snake, self.model.apple, self.model.score,
                           self.model.highScore, self.model.isGameOver)
        self.wait_end_of_frame(time.time() - start)

    def start(self):
        """Start the game"""
        start = time.time()
        self.model.reset()
        self.model.apple = self.recording[0][0]
        self.index = 0
        if self.is_first_game:
            self.is_first_game = False
            self.view.init_screen(self.model.dim, self.model.snake, self.model.apple,
                                  self.model.score, self.model.highScore)
        else:
            self.view.updateUI(self.model.snake, self.model.apple, self.model.score,
                               self.model.highScore)
        self.wait_end_of_frame(time.time() - start)
