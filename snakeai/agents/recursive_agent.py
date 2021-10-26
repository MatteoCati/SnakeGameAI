import random
from typing import Tuple

from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.constants import Actions, Rewards
from snakeai.game.memento import FrozenState
from snakeai.game.model import Snake
from snakeai.game.agent_controller import AgentGame


def play(dim: int = 12, recursion_depth: int = 5, fps: int = 7):
    """Play with  a recursive agent

    Parameters
    ----------
    dim : int, default=12
        the side of the board
    recursion_depth : int, default=12
        the number of recursive steps
    fps : int, default=7
        the number of frames per second
    """
    agent = Recursive(dim, recursion_depth)
    game = AgentGame(dim, fps=fps, replay_allowed=True)
    game.play(agent)


class Recursive(AbstractAgent):
    """A Class for an agent that uses recursion

    The agent will find the best move by simulating `maxDepth` steps in all directions
    and choosing the path with the best cumulative reward

    Parameters
    --------------
    dim : int
        the side of the board
    max_depth : int, default=5
        the maximum depth for the recursion

    Attributes
    ------------
    dim : int
        the side of the board
    max_depth : int
        the maximum depth for the recursion
    gamma : float [0;1]
        the discount factor for the recursion
    """

    def __init__(self, dim: int, max_depth: int = 5):
        super().__init__(dim)
        self.max_depth = max_depth
        self.gamma = 0.75

    def _recursion(self, original: Snake, depth: int) -> Tuple[int, Actions]:
        best_actions = []
        best = -10000
        for act in Actions:
            sim = Snake(self.dim)
            sim.snake = original.snake
            sim.apple = original.apple
            sim.direction = original.direction
            sim.change_direction(act)
            rew = sim.step()
            next_reward = rew.value
            if not Rewards.is_game_over(rew) and depth < self.max_depth:
                rew2, _ = self._recursion(sim, depth + 1)
                next_reward += rew2 * self.gamma
            if best < next_reward:
                best = next_reward
                best_actions = [act]
            elif best == next_reward:
                best_actions.append(act)
        return best, random.choice(best_actions)

    def execute(self, state: FrozenState) -> Actions:
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
        original = Snake(self.dim)
        original.snake = state.snake.copy()
        original.apple = state.apple
        original.direction = state.direction
        _, direction = self._recursion(original, 1)
        return direction

    def fit(self, old_state: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """This agent does not need to train, so this method does nothing"""

    @classmethod
    def load(cls, dim: int, model_path: str):
        """This agent does not save anything. If the method is called, it raises a NotImplementedError"""
        raise NotImplementedError("A recursive agent cannot be loaded from a file")

    def save(self, model_path: str = None):
        """This agent cannot be saved. If the method is called, it raises a NotImplementedError"""
        raise NotImplementedError("A recursive Agent cannot be saved")
