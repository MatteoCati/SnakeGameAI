import random
from typing import List, Tuple

from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.constants import Actions, Rewards, Coords
from snakeai.game.memento import FrozenState
from snakeai.game.model import Snake


class Recursive(AbstractAgent):
    """A Class for an agent that uses recursion

    The agent will find the best move by simulating `maxDepth` steps in all directions
    and choosing the path with the best cumulative reward

    Parameters
    --------------
    dim : int
        the side of the board
    maxDepth : int, default=5
        the maximum depth for the recursion

    Attributes
    ------------
    dim : int
        the side of the board
    maxDepth : int
        the maximum depth for the recursion
    gamma : float [0;1]
        the discount factor for the recursion
    """

    def __init__(self, dim: int, maxDepth: int=5):
        super().__init__(dim)
        self.maxDepth = maxDepth
        self.gamma = 0.75

    def _recursion(self, original: List[Coords], depth: int)-> Tuple[int, Actions]:
        bestActions = []
        best = -10000
        for act in Actions:
            sim = Snake(self.dim)
            sim.snake = original.snake
            sim.apple = original.apple
            sim.direction = original.direction
            sim.changeDirection(act)
            rew = sim.step()
            nextRew = rew.value
            if not Rewards.isGameOver(rew) and depth < self.maxDepth:
                rew2, _ = self._recursion(sim, depth + 1)
                nextRew += rew2 * self.gamma
            if best < nextRew:
                best = nextRew
                bestActions = [act]
            elif best == nextRew:
                bestActions.append(act)
        return best, random.choice(bestActions)

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

    def fit(self, oldState: FrozenState, action: Actions, rew: int, state: FrozenState, done: bool):
        """This agent does not need to train, so this method does nothing"""

    @classmethod
    def load(cls, dim: int, model_path: str):
        """This agent does not save anything. If the method is called, it raises a NotImplementedError"""
        raise NotImplementedError("A recursive agent cannot be loaded from a file")

    def save(self, model_path: str = None):
        """This agent cannot be saved. If the method is called, it raises a NotImplementedError"""
        raise NotImplementedError("A recursive Agent cannot be saved")
