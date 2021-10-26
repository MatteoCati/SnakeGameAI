from snakeai.game.model import Snake
from snakeai.game.view import GameGUI
import time

""""This module is used for testing the GameGUI"""

if __name__ == "__main__":
    snake = Snake(12)
    view = GameGUI()
    view.init_screen(snake.dim, snake.snake, snake.apple, snake.score, snake.highScore)
    while not snake.isGameOver:
        time.sleep(0.50)
        act = view.get_input()
        if act == "QUIT":
            break
        if act:
            snake.change_direction(act)
        snake.step()
        view.updateUI(snake.snake, snake.apple, snake.score, snake.highScore, snake.isGameOver)
    view.quit()
