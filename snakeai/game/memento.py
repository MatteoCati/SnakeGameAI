from typing import List

from snakeai.game.constants import Actions, Coords


class FrozenState:
    """A class that stores the state of the game in a given moment.

    Parameters
    -----------
    snake : list(Coords)
        The position of the snake
    apple : Coords
        The position of the apple
    direction : Actions
        The direction of the snake
    dim : int
        The size of the board

    Attributes
    -----------
    snake : list(Coords)
        The position of the snake
    apple : Coords
        The position of the apple
    direction : Actions
        The direction of the snake
    dim : int
        The size of the board
    """
    def __init__(self, snake: List[Coords], apple: Coords, direction: Actions, dim: int):
        self.snake = snake
        self.apple = apple
        self.direction = direction
        self.dim = dim

    @property
    def simple_state(self) -> List[int]:
        """list : A list with the information about obstacles, position of the apple
            relative to the position of the snake, current direction"""
        data = []
        data.append(1 if self.apple.y < self.snake[-1].y else 0) # Is apple up
        data.append(1 if self.apple.x > self.snake[-1].x else 0) # Is apple right
        data.append(1 if self.apple.y > self.snake[-1].y else 0) # Is apple down
        data.append(1 if self.apple.x < self.snake[-1].x else 0) # Is apple left

        is_empty = lambda c: (not c in self.snake) and 0 <= c.x < self.dim and 0 < c.y < self.dim
        up = Actions.UP.value + self.snake[-1]
        data.append(0 if is_empty(up) else 1)

        right = Actions.RIGHT.value + self.snake[-1]
        data.append(0 if is_empty(right) else 1)

        down = Actions.DOWN.value + self.snake[-1]
        data.append(0 if is_empty(down) else 1)

        left = Actions.LEFT.value + self.snake[-1]
        data.append(0 if is_empty(left) else 1)

        data.append(int(self.direction == Actions.UP))
        data.append(int(self.direction == Actions.RIGHT))
        data.append(int(self.direction == Actions.DOWN))
        data.append(int(self.direction == Actions.LEFT))

        return data

    @property
    def simple_state_string(self):
        return "".join([str(x) for x in self.simple_state])

    @property
    def table_string(self) -> str:
        """str : A string with the coords of the snake and of the apple"""
        state = [str(el) for el in self.snake]
        state.append(str(self.apple))
        return "".join(state)

    @property
    def table(self) -> List[List[int]]:
        """2d list of int : A table representing the board at the current state"""
        table = []
        for y in range(self.dim):
            row = []
            for x in range(self.dim):
                coord = Coords(x, y)
                if coord == self.apple:
                    row.append(3)
                elif coord in self.snake:
                    if coord == self.snake[-1]:
                        row.append(1)
                    else:
                        row.append(-1)
                else:
                    row.append(0)
            table.append(row)
        return table
