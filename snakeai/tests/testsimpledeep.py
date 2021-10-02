from snakeai.agents.simple_deep_agent import DQN
from snakeai.game.agent_controller import AgentGame
from collections import deque
from tqdm import tqdm
import matplotlib.pyplot as plt

def train(episodes, size, show = False) -> DQN:
    """Train a `DQN` agent
    
    This method will train a StateAgent for a certain amount of steps.
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
    game = AgentGame(size, show=show, fps=20, replay_allowed=False)
    for i in t:
        game.play(agent)
        scores.append(game.model.score)
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

def  play(model_path = None, fps = 5):
    """Play with an already trained `DQN`

    If no path is given, a default (pre-trained) model will be used

    Parameters
    ------------
    model_path: str, optional
        the path to the trained model to load
    """
    if not model_path:
        model_path = ".\\models\\deepCopiedModel"
    size = 12
    agent = DQN.load(size, model_path)
    game = AgentGame(size, replay_allowed=True, fps=fps)
    agent.epsilon = 0
    game.play(agent)
