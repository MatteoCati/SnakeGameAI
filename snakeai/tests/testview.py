from snakeai.game.model import Snake
from snakeai.game.constants import Actions
from snakeai.game.view import GameGUI
import time

if __name__ == "__main__":
    snake = Snake()
    view = GameGUI()
    view.initScreen(snake.dim, snake.snake, snake.apple, snake.score)
    while not snake.isGameOver:
        time.sleep(0.50)
        act = view.getInput()
        if act == "QUIT":
            break
        if act:
            snake.changeDirection(act)
        snake.step()
        view.updateUI(snake.snake, snake.apple, snake.score, snake.isGameOver)
        

    view.quit()