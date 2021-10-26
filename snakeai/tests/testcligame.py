from snakeai.game.constants import GUIMode
from snakeai.game.user_controller import UserGame

"""Use this module to check that the cli GUI works"""

if __name__ == "__main__":
    game = UserGame(mode=GUIMode.CLI)
    game.play()
