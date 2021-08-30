from snakeai.agents.recursive_agent import Recursive
from snakeai.game.agent_controller import AgentGame

if __name__ == "__main__":
    agent = Recursive(7, 5)
    game = AgentGame(7, replayAllowed=True)
    game.play(agent)