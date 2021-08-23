import pygame
from snakeai.game.constants import Actions
import time

class GeneralView():
    """
    The base class for any view of the game. If this is used, it does not show anything
    """
    def initScreen(self, dim, snake, apple, score):
        pass

    def quit(self):
        pass

    def getInput(self):
        pass

    def updateUI(self, snake, apple, score, isGameOver = False):
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

    
    def initScreen(self, dim, snake, apple, score):
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
        self.screen = pygame.display.set_mode([max(280, boardSide), 33+boardSide])
        self.board = pygame.Surface((boardSide, boardSide))
        self.updateUI(snake, apple, score)
    
    def quit(self):
        """Close the game"""
        pygame.quit()
    
    def getInput(self):
        """Get and returns input from the user
        
        Returns
        -----------
        `Actions` or ``"QUIT"``
            the current input"""
        for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return "QUIT"
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_UP:
                        return Actions.UP
                    if ev.key == pygame.K_DOWN:
                        return Actions.DOWN
                    if ev.key == pygame.K_LEFT:
                        return Actions.LEFT
                    if ev.key == pygame.K_RIGHT:
                        return Actions.RIGHT

    def updateUI(self, snake, apple, score, isGameOver = False):
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
            text = self.font.render("Game Over! - High score: "+str(score), True, (0,0,0))
        else:
            text = self.font.render("Score: "+str(score), True, (0,0,0))
        
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


