from snakeai.game.constants import Actions

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
    
    Attributes
    -----------
    snake : list(Coords)
        The position of the snake
    apple : Coords
        The position of the apple
    direction : Actions
        The direction of the snake
    """
    def __init__(self, snake, apple, direction, dim):
        self.snake = snake
        self.apple = apple
        self.direction = direction
        self.dim = dim
    
    @property
    def simpleState(self):
        """list : A list with the insformations about obstacles, position of the apple relative to the position of the snake, current direction"""
        data = []
        data.append(1 if self.apple.y < self.snake[-1].y else 0) # Is apple up
        data.append(1 if self.apple.x > self.snake[-1].x else 0) # Is apple right
        data.append(1 if self.apple.y > self.snake[-1].y else 0) # Is apple down
        data.append(1 if self.apple.x < self.snake[-1].x else 0) # Is apple left
        
        isEmpty = lambda c: (not c in self.snake) and 0 <= c.x < self.dim and 0 < c.y < self.dim
        up = Actions.UP.value + self.snake[-1]
        if isEmpty(up): data.append(0)
        else: data.append(1)

        right = Actions.RIGHT.value + self.snake[-1]
        if isEmpty(right): data.append(0)
        else: data.append(1)

        down = Actions.DOWN.value + self.snake[-1]
        if isEmpty(down): data.append(0)
        else: data.append(1)

        left = Actions.LEFT.value + self.snake[-1]
        if isEmpty(left): data.append(0)
        else: data.append(1)

        data.append(int(self.direction == Actions.UP))
        data.append(int(self.direction == Actions.RIGHT))
        data.append(int(self.direction == Actions.DOWN))
        data.append(int(self.direction == Actions.LEFT))

        return data
    
    @property
    def tableString(self):
        """str : A string with the coords of the snake and of the apple"""
        state = [str(el) for el in self.snake]
        state.append(str(self.apple))
        return "".join(state)