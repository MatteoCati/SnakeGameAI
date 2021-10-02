from snakeai.game.user_controller import UserGame

def play(size: int, fps: int= 2):
    """Play the game on a board of the given size

    Parameters
    ----------
    size: int
        the side of the board
    fps: int
        the number of frames per seconds
    """
    game = UserGame(size, fps)
    game.play()