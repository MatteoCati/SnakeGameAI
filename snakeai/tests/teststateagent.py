from snakeai.game.agent_controller import AgentGame
from snakeai.agents.tabular_agent import StateAgent
import os
from collections import deque
from tqdm import tqdm

def train(episodes, size):
    """Train a StateAgent
    
    This mehod will train a StateAgent for a certain amount of steps. 
    Then it will print some stats about it. The agent will be returned by the function. The 
    states are not saved on a file.
    
    Parameters
    -----------
    episodes: int
        The number of episodes in which the agent is trained
    size: int
        The size of the board (side length)"""
    agent = StateAgent(size)
    maxScore = 0
    scores = deque(maxlen=1000)
    for i in tqdm(range(episodes)):
        game = AgentGame(size,show=False)
        game.play(agent)
        scores.append((game.model.score))
        maxScore = max(maxScore, game.model.score)
        agent.reset()
    #agent.save()
    print("Epsilon:", agent.EPSILON)
    print("High Score:", maxScore)
    print("Average score:", sum(scores)/len(scores))
    return agent

if __name__ == "__main__":
    agent = train(100_000, 4)
    # agent = StateAgent(4, 0)
    # path = os.path.abspath(".\\models\\CompleteStateAgentDictionaryDefault")
    # agent.load(path)
    game = AgentGame(4, closeOnFail=False)
    game.play(agent)
    
