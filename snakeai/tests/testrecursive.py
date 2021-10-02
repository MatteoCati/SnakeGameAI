from snakeai.agents.recursive_agent import Recursive
from snakeai.game.agent_controller import AgentGame


def play(dim= 12, recursion_depth = 5, fps = 7):
    """Play with  a recursive agent

    Parameters
    ----------
    dim : int, default=12
        the side of the board
    recursion_depth : int, default=12
        the number of recursive steps
    fps : int, default=7
        the number of frames per second
    """
    agent = Recursive(dim, recursion_depth)
    game = AgentGame(dim, fps=fps, replay_allowed=True)
    game.play(agent)