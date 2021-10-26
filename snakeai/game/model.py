import random
from typing import List

from snakeai.game.constants import Actions, Coords, Rewards
from snakeai.game.memento import FrozenState


# noinspection PyAttributeOutsideInit
class Snake:
    """A class which stores the info about the game

    Parameters
    -------------
    dim : int
        The side of the board

    Attributes
    ------------
    dim : int
        the side of the board
    MAX_SCORE : int
        The maximum score achievable
    MAX_GROWING : int
        The maximum length of the snake
    score : int
        The current score
    direction : Actions
        The current direction
    isGameOver : bool
        whether the snake has reached game over
    highScore : int
        The maximum score achieved
    """
    def __init__(self, dim: int):
        self.dim = dim
        self.MAX_SCORE = dim*dim
        self.MAX_GROWING = int(0.9*dim*dim)
        self.highScore = 0
        self.reset()

    def reset(self):
        """Prepare to start the game"""
        self._snake = [Coords(self.dim//2, self.dim//2)]
        self.set_apple()
        self.direction = Actions.DOWN
        self.score = 0
        self.isGameOver = False

    @property
    def state(self) -> FrozenState:
        """FrozenState : A description of the current state"""
        return FrozenState(self.snake, self.apple, self.direction, self.dim)

    def set_apple(self):
        """Choose new valid position for the apple"""
        positions = []
        for x in range(self.dim):
            for y in range(self.dim):
                coord = Coords(x, y)
                if coord not in self._snake:
                    positions.append(coord)
        self.apple = random.choice(positions)

    def change_direction(self, direction: Actions):
        """Change the direction of the snake. Ignore it if it is opposite to current direction

        Parameters
        -------------
        direction : Actions
            the new direction of the snake
        """
        opposites = [(Actions.UP, Actions.DOWN), (Actions.DOWN, Actions.UP),
                    (Actions.LEFT, Actions.RIGHT), (Actions.RIGHT, Actions.LEFT)]
        if not (direction, self.direction) in opposites:
            self.direction = direction

    @property
    def snake(self) -> List[Coords]:
        """list of Coords : The body of the snake (head is last)"""
        return self._snake.copy()

    @snake.setter
    def snake(self, new_snake: List[Coords]):
        self._snake = new_snake.copy()

    def step(self) -> Rewards:
        """Update model by moving snake of one step

        Returns
        -----------
        Rewards
            The reward obtained after the step
        """
        next_head = self._snake[-1] + self.direction.value
        # Check collision with itself
        if next_head in self._snake:
            self.isGameOver = True
            return Rewards.FAILED
        # Check collision with border
        if not (0 <= next_head.x < self.dim and 0 <= next_head.y < self.dim):
            self.isGameOver = True
            return Rewards.FAILED
        prev_distance = self._snake[-1].distance(self.apple)
        self._snake.append(next_head)
        if next_head == self.apple:
            self.score += 1
            self.highScore = max(self.score, self.highScore)
            if self.score > self.MAX_GROWING:
                self._snake.pop(0)
            self.set_apple()
            self.isGameOver = self.score > self.MAX_SCORE
            if self.isGameOver:
                return Rewards.ENDED
            return Rewards.GOT_APPLE
        self._snake.pop(0)
        if self._snake[-1].distance(self.apple) >= prev_distance:
            return Rewards.AWAY
        return Rewards.CLOSER
