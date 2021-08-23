from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.constants import Actions, Rewards
from snakeai.game.model import Snake
import random


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
    def __init__(self, dim, maxDepth = 5):
        super().__init__(dim)
        self.maxDepth = maxDepth
        self.gamma = 0.75
    
    def _recursion(self, original, depth):
        ok = list()
        mass = -10000
        for dir in Actions:
            sim = Snake(self.dim)
            sim._snake = original.snake
            sim.apple = original.apple
            sim.changeDirection(dir)
            r = sim.step()
            nextRew = r.value
            if r != Rewards.FAILED and depth < self.maxDepth:
                r2, _ = self._recursion(sim, depth+1)
                nextRew += r2 * self.gamma
            if mass < nextRew:
                mass = nextRew
                ok = [dir]
            elif mass == nextRew:
                ok.append(dir)
        return mass, random.choice(ok)
    
    def execute(self, snake, apple):
        """Get the next action to do, given the state
        
        Parameters
        --------------
        snake : list(Coords)
            the position of the snake
        apple : Coords
            the position of the apple
        
        Returns
        --------------
        Actions
            the direction in which  to move
        """
        original = Snake(self.dim)
        original._snake = snake
        original.apple = apple
        best, dir = self._recursion(original, 1)
        return dir
    
    def fit(self, oldSnake, oldApple, rew, snake, apple, done):
        """This agent does not need to train, so this method does nothing"""
        pass

