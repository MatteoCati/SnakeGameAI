import sys
import time
from typing import Union

from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.constants import GUIMode, Actions
from snakeai.game.memento import FrozenState
from snakeai.game.view import GeneralView
from snakeai.game.user_controller import UserGame


class AgentGame(UserGame):
    """The class for controlling the game when played by an agent

    Parameters
    --------------
    dim : int, default=20
        the side of the board
    fps : int, default=7
        the number of fps
    show : bool, default=True
        Whether to show the GUI or not
    replay_allowed : Bool, default=False
        whether the game should wait for replay after game over
    mode : GuiMode, default=GUIMode.WINDOW
        The type of interface

    Attributes
    --------------
    model : Snake
        The model for the game
    view : GeneralView
        The GUI for the game
    frame_time : float
        The duration of each frame in seconds (if show is set to True)
    replay_allowed : bool
        Whether the game should close immediately at game over
    to_init : bool
        Whether the GUI should be initialized
    """

    def __init__(self, dim: int = 20, fps: int = 7, show: bool = True, replay_allowed: bool = False,
                 mode: GUIMode = GUIMode.WINDOW):
        self.show = show
        if not show:
            replay_allowed = False
            mode = GUIMode.NO_SHOW
            fps = 10**100
        super().__init__(dim, fps, mode)
        self.replay_allowed = replay_allowed
        self.agent = None

    def wait_end_of_frame(self, elapsed: float):
        if self.show:
            super().wait_end_of_frame(elapsed)

    def start(self) -> FrozenState:
        """Start the game

        Returns
        ---------
        FrozenState
            The state at the beginning of the game
        """
        super().start()
        return self.model.state

    def step(self, action: Union[Actions, str]):
        """Execute one step (frame) of the game

        Parameters
        ------------
        action : Actions or ``"QUIT"``
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
        inp = self.view.get_input()
        if inp == "QUIT":
            self.quit()
            sys.exit()
        old_state = self.model.state
        self.model.change_direction(action)
        rew = self.model.step()
        if self.show:
            self.view.updateUI(self.model.snake, self.model.apple, self.model.score,
                               self.model.highScore, self.model.isGameOver)
            self.wait_end_of_frame(time.time() - start)
        return old_state, rew.value, self.model.state, self.model.isGameOver

    def play(self, agent: AbstractAgent = None):
        """Play a complete game

        Parameters
        ------------
        agent : AbstractAgent
            The agent that will play
        """
        if not self.agent:
            self.agent = agent

        state = self.start()
        self.agent.reset()
        while not self.model.isGameOver:
            action = self.agent.execute(state)
            old_state, rew, state, done = self.step(action)
            self.agent.fit(old_state, action, rew, state, done)
        if self.show:
            self.view.updateUI(self.model.snake, self.model.apple, self.model.score, self.model.highScore,
                               self.model.isGameOver)
            self.wait_end_of_frame(0.0)
        if self.replay_allowed:
            self.wait_for_quit()
