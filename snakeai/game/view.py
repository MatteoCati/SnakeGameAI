from typing import List, Union, Optional

import pygame
from snakeai.game.constants import Actions, Coords, GUIMode


class GeneralView:
    """
    The base class for any view of the game. If this is used, it does not show anything
    """

    def init_screen(self, dim: int, snake: List[Coords], apple: Coords, score: int, high_score: int):
        """Create a screen when the game start

        Parameters
        -----------
        dim : int
            the side of the board
        snake : list(Coords)
            The position of the snake
        apple : Coords
            the position pof the apple
        score : int
            The current score
        high_score : int
            the current high score
        """

    def quit(self):
        """close the screen"""

    def get_input(self) -> Optional[Union[Actions, str]]:
        """Get the user input"""
        return None

    def updateUI(self, snake: List[Coords], apple: List[Coords], score: int, high_score: int, isGameOver: bool = False):
        """Update the screen with current data

        Parameters
        ----------
        snake : list(Coords)
            The position of the snake
        apple : Coords
            The position of the apple
        score : int
            The current score
        high_score : int
            the current high score
        isGameOver bool, default=False
            Whether the game is finished
        """


class GameGUI(GeneralView):
    """A GUI object for rendering and playing the game

    This is the class used to create a window on the screen.
    """
    SQUARE_SIDE = 20
    RED = (255, 0, 0)
    DARK_GREEN = (11, 102, 35)
    LIGHT_GREEN = (76, 187, 23)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def init_screen(self, dim: int, snake: List[Coords], apple: Coords, score: int, high_score: int):
        """
        Create the window where the game will be shown

        Parameters
        --------------
        dim : int
            the side of the board
        snake : list(Coords)
        apple : Coords
        score : int
            The current score
        high_score: int
            The current high score
        """
        pygame.init()
        self.font = pygame.font.SysFont("freesans", 28)
        board_side = self.SQUARE_SIDE * dim
        pygame.display.set_caption('Snake Game')
        self.screen = pygame.display.set_mode([max(327, board_side), 33 + board_side])
        self.board = pygame.Surface((board_side, board_side))
        self.updateUI(snake, apple, score, high_score)

    def quit(self):
        """Close the window"""
        pygame.quit()

    def get_input(self) -> Optional[Union[Actions, str]]:
        """Get and returns input from the user

        Returns
        -----------
        `Actions`, ``"REPLAY"`` or ``"QUIT"``
            the current input
        """
        res = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                res = "QUIT"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    res = "REPLAY"
                if event.key == pygame.K_UP:
                    res = Actions.UP
                if event.key == pygame.K_DOWN:
                    res = Actions.DOWN
                if event.key == pygame.K_LEFT:
                    res = Actions.LEFT
                if event.key == pygame.K_RIGHT:
                    res = Actions.RIGHT
            if res:
                return res
        return res

    def updateUI(self, snake: List[Coords], apple: Coords, score: int, high_score: int, isGameOver: bool = False):
        """
        Update the GUI with the current state of the game

        Parameters
        ----------------
        snake : list(Coords)
        apple : Coords
        score : int
            The current score
        high_score: int
            The current high score
        isGameOver : Bool, default=False
            if set to `True`, it shows the game over screen
        """
        self.board.fill(self.WHITE)
        self.screen.fill(self.WHITE)
        if isGameOver:
            text = self.font.render("Game Over! - Final score: " + str(score) + "/" + str(high_score), True, self.BLACK)
        else:
            text = self.font.render("Score: " + str(score) + " - " + "High Score: " + str(high_score), True, self.BLACK)

        self.screen.blit(text, (0, 0))

        # Draw the snake
        for rect in snake:
            if rect == snake[-1]:
                pygame.draw.rect(self.board, self.LIGHT_GREEN, pygame.Rect(rect.x * self.SQUARE_SIDE,
                                                                           rect.y * self.SQUARE_SIDE, self.SQUARE_SIDE,
                                                                           self.SQUARE_SIDE))
            else:
                pygame.draw.rect(self.board, self.DARK_GREEN, pygame.Rect(rect.x * self.SQUARE_SIDE,
                                                                          rect.y * self.SQUARE_SIDE, self.SQUARE_SIDE,
                                                                          self.SQUARE_SIDE))
        # Draw the apple
        pygame.draw.circle(self.board, self.RED,
                           ((apple.x + 0.5) * self.SQUARE_SIDE, (apple.y + 0.5) * self.SQUARE_SIDE),
                           self.SQUARE_SIDE / 2)
        # Top border
        pygame.draw.line(self.board, self.BLACK, (0, 0), (self.board.get_width(), 0), 1)
        # Bottom border
        pygame.draw.line(self.board, self.BLACK,
                         (0, self.board.get_height() - 1), (self.board.get_width(), self.board.get_height() - 1), 1)
        # Left border
        pygame.draw.line(self.board, self.BLACK, (0, 0), (0, self.board.get_height() - 1), 1)
        # Right border
        pygame.draw.line(self.board, self.BLACK,
                         (self.board.get_width() - 1, 0), (self.board.get_width() - 1, self.board.get_height() - 1), 1)
        horPosition = (self.screen.get_width() - self.board.get_width()) // 2
        self.screen.blit(self.board, (horPosition, text.get_height()))
        pygame.display.update()


class CliGUI(GeneralView):
    """A GUI object for rendering the game in the command line"""

    def init_screen(self, dim: int, snake: List[Coords], apple: Coords, score: int, high_score: int):
        """Show the initial state of the game"""
        self.dim = dim
        self.updateUI(snake, apple, score, high_score)

    def get_input(self) -> Optional[Union[Actions, str]]:
        """Get the input from the user and return the action

        Returns
        ---------
        `Actions`, ``"REPLAY"`` or ``"QUIT"``
            the current input
        """
        inp = input("Choose action: ").lower()
        res = None
        if inp == "q":
            res = "QUIT"
        elif inp == "r":
            res = "REPLAY"
        elif inp == "up":
            res = Actions.UP
        elif inp == "down":
            res = Actions.DOWN
        elif inp == "left":
            res = Actions.LEFT
        elif inp == "right":
            res = Actions.RIGHT
        return res

    def updateUI(self, snake: List[Coords], apple: Coords, score: int, high_score: int, isGameOver: bool = False):
        """
        Print in the command line the current state of the game

        Parameters
        ----------------
        snake : list(Coords)
        apple : Coords
        score : int
            The current score
        high_score: int
            The current high score
        isGameOver : bool, default=False
            if set to `True`, it shows the game over screen
        """
        if isGameOver:
            print("--" + "-" * self.dim)
            print("Final Score:", score, "/", high_score)
        print("--" + "-" * self.dim)
        for y in range(self.dim):
            row = "|"
            for x in range(self.dim):
                coord = Coords(x, y)
                if coord == apple:
                    row += "o"
                elif coord in snake:
                    row += "x"
                else:
                    row += " "
            row += "|"
            print(row)
        print("--" + "-" * self.dim)


def generate_view(mode: GUIMode) -> GeneralView:
    """Generate a GUI according to the given mode

    Parameters
    -----------
        mode: GUIMode
            The type of GUI to generate

    Returns
    --------
    GeneralView
        A GUI of the specified type
    """
    if mode == GUIMode.NO_SHOW:
        return GeneralView()
    if mode == GUIMode.WINDOW:
        return GameGUI()
    if mode == GUIMode.CLI:
        return CliGUI()
