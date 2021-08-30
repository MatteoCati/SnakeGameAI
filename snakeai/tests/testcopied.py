from snakeai.agents.copy_agent import DQN
from snakeai.game.agent_controller import AgentGame
from collections import deque
from tqdm import tqdm
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

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
    agent = DQN(size)
    maxScore = 0
    scores = deque(maxlen=20)
    avgs = list()
    t = tqdm(range(episodes))
    game = AgentGame(size,show=True, fps =20, replayAllowed=False)
    for i in t:
        game.play(agent)
        scores.append((game.model.score))
        maxScore = max(maxScore, game.model.score)
        t.set_postfix_str(f"HS: {maxScore}, avg: {sum(scores)/len(scores):.2f}")
        avgs.append(sum(scores)/len(scores))
        agent.reset()
    print("\nEpsilon:", agent.epsilon)
    print("High Score:", maxScore)
    print("Average score:", sum(scores)/len(scores))
    plt.plot(range(len(avgs)), avgs, "o")
    plt.show()
    return agent

if __name__ == "__main__":
    import os
    #agent = train(60, 20)
    path = os.path.abspath(".\\models\\deepCopiedModel")
    agent = DQN(20)
    agent.model = load_model(path)
    game = AgentGame(20, replayAllowed=True)
    agent.epsilon = 0
    game.play(agent)