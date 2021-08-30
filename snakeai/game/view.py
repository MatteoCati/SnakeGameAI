import pygame
from snakeai.game.constants import Actions, Coords
import time

class GeneralView():
    """
    The base class for any view of the game. If this is used, it does not show anything
    """
    def initScreen(self, dim, snake, apple, score, highScore):
        pass

    def quit(self):
        pass

    def getInput(self):
        pass

    def updateUI(self, snake, apple, score, highScore, isGameOver = False):
        pass



class GameGUI(GeneralView):
    """A GUI object for rendering and playing the game

    This is the class used to make the user play.

    Attributes
    --------------
    SQUARE_SIDE : int 
        the side of each square (in pixels)
    """
    def __init__(self):
        self.SQUARE_SIDE = 20

    
    def initScreen(self, dim, snake, apple, score, highScore):
        """
        Create the window where the game will be shown

        Parameters
        --------------
        dim : int
            the side of the board
        snake : list(Coords)
        apple : Coords
        score : int
        """
        pygame.init()
        self.font = pygame.font.SysFont("freesans", 28)
        boardSide = self.SQUARE_SIDE*dim
        self.screen = pygame.display.set_mode([max(327, boardSide), 33+boardSide])
        self.board = pygame.Surface((boardSide, boardSide))
        self.updateUI(snake, apple, score, highScore)
    
    def quit(self):
        """Close the game"""
        pygame.quit()
    
    def getInput(self):
        """Get and returns input from the user
        
        Returns
        -----------
        `Actions`, ``"REPLAY"`` or ``"QUIT"``
            the current input"""
        for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return "QUIT"
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_r:
                        return "REPLAY"
                    if ev.key == pygame.K_UP:
                        return Actions.UP
                    if ev.key == pygame.K_DOWN:
                        return Actions.DOWN
                    if ev.key == pygame.K_LEFT:
                        return Actions.LEFT
                    if ev.key == pygame.K_RIGHT:
                        return Actions.RIGHT

    def updateUI(self, snake, apple, score, highScore, isGameOver = False):
        """
        Update the GUI with the current state of the game

        Parameters
        ----------------
        snake : list of Coords
        apple : Coords
        score  int
        isGameOver : Bool, default=False
            if set to True, it shows the game over screen
        """
        self.board.fill((255, 255, 255))
        self.screen.fill((255, 255, 255))
        if isGameOver:
            text = self.font.render("Game Over! - Final score: " + str(score) + "/"+str(highScore), True, (0,0,0))
            
        else:
            text = self.font.render("Score: "+str(score) + " - " + "High Score: " + str(highScore), True, (0,0,0))
            
        
        self.screen.blit(text, (0, 0))
        
        for rect in snake:
            if rect == snake[-1]:
                pygame.draw.rect(self.board, (0,0,255), pygame.Rect(rect.x*self.SQUARE_SIDE, rect.y * self.SQUARE_SIDE, 
                                                                    self.SQUARE_SIDE, self.SQUARE_SIDE))
            else:
                pygame.draw.rect(self.board, (0,0,0), pygame.Rect(rect.x*self.SQUARE_SIDE, rect.y * self.SQUARE_SIDE, 
                                                                    self.SQUARE_SIDE, self.SQUARE_SIDE))
        
        pygame.draw.circle(self.board, (255, 0, 0), ((apple.x+0.5)*self.SQUARE_SIDE, (apple.y+0.5)*self.SQUARE_SIDE), self.SQUARE_SIDE/2)
        pygame.draw.line(self.board, (0,0,0), (0, 0), (self.board.get_width(), 0), 1) # Top border
        pygame.draw.line(self.board, (0,0,0), (0, self.board.get_height()-1), (self.board.get_width(), self.board.get_height()-1), 1) # Bottom border
        pygame.draw.line(self.board, (0,0,0), (0, 0), (0, self.board.get_height()-1), 1) # Left border
        pygame.draw.line(self.board, (0,0,0), (self.board.get_width()-1, 0), (self.board.get_width()-1, self.board.get_height()-1), 1) # Right border
        horPosition = (self.screen.get_width() - self.board.get_width())//2
        self.screen.blit(self.board, (horPosition, text.get_height()))
        pygame.display.update()

class cliGUI(GeneralView):
    """A GUI object for rendering the game on the command line"""
    def initScreen(self, dim, snake, apple, score, highScore):
        """Show the initial state of the game"""
        self.dim = dim
        self.updateUI(snake, apple, score, highScore)

    def getInput(self):
        """Get the input fro mthe user and return the action
        Returns
        ---------
        `Actions`, ``"REPLAY"`` or ``"QUIT"``
            the current input
        """
        inp = input("Choose action: ")
        if inp == "q":
            return "QUIT"
        if inp == "r":
            return "REPLAY"
        elif inp == "up":
            return Actions.UP
        elif inp == "down":
            return Actions.DOWN
        elif inp == "left":
            return Actions.LEFT
        elif inp == "right":
            return Actions.RIGHT

    def updateUI(self, snake, apple, score, highScore, isGameOver = False):
        """
        Print on the command line the current state of the game

        Parameters
        ----------------
        snake : list of Coords
        apple : Coords
        score : int
        isGameOver : Bool, default=False
            if set to True, it shows the game over screen
        """
        if isGameOver:
            print("--" + "-"*self.dim)
            print("Final Score:", score, "/", highScore)
        print("--" + "-"*self.dim)
        for y in range(self.dim):
            row = "|"
            for x in range(self.dim):
                c = Coords(x, y)
                if c == apple:
                    row += "o"
                elif c in snake:
                    row += "x"
                else: row += " "
            row += "|"
            print(row)
        print("--" + "-"*self.dim)

