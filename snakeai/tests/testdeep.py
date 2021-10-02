from snakeai.game.constants import Rewards
from snakeai.agents.deep_agent import DeepQAgent
from snakeai.game.agent_controller import AgentGame
from collections import deque
from tqdm import tqdm
import matplotlib.pyplot as plt
import pickle as pkl
import os
from snakeai.game.model import Snake
import time

def train(episodes, size, show= False, agent : DeepQAgent = None):
    """Train a StateAgent
    
    This method will train a StateAgent for a certain amount of steps.
    Then it will print some stats about it. The agent will be returned by the function. The 
    states are not saved on a file.
    
    Parameters
    -----------
    episodes: int
        The number of episodes in which the agent is trained
    size: int
        The size of the board (side length)"""
    if not agent:
        agent = DeepQAgent(size)
    maxScore = 0
    scores = deque(maxlen=20)
    avgs = list()
    t = tqdm(range(episodes))
    game = AgentGame(size,show=show, fps =20, replayAllowed=False)
    for _ in t:
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


def fastTrain(episodes, size, agent : DeepQAgent = None):
    """EXPERIMENTAL: This method should be faster than the standard `train`"""
    path = os.path.abspath(".\\models")
    model = Snake(size)
    if not agent:
        agent = DeepQAgent(size)
    t = tqdm(range(episodes))
    scores = deque(maxlen = 50)
    cumScores = deque(maxlen = 50)
    cumavgs = list()
    maxScore = 0
    avgs = list()
    for ep in t:
        model.reset()
        state = model.state
        rew  = None
        step = 0
        cs = 0
        while not Rewards.isGameOver(rew) and step < 10_000:
            step += 1
            action = agent.execute(state)
            oldState = state
            model.changeDirection(action)
            rew = model.step()
            state = model.state
            cs += rew.value
            agent.fit(oldState, action, rew.value, state, model.isGameOver)
        scores.append(model.score)
        cumScores.append(cs)
        maxScore = max(maxScore, model.score)
        t.set_postfix_str(f"HS: {maxScore}, avg: {sum(scores)/len(scores):.2f}, cumAvg: {sum(cumScores)/len(cumScores):.1f}")
        avgs.append(sum(scores)/len(scores))
        cumavgs.append(sum(cumScores)/len(cumScores))
        agent.reset()
        if((ep+1)%100 == 0):
            with open(path+"\\avgs\\avgUntil"+str(ep+1)+".pkl", "wb") as fin:
                pkl.dump((avgs, cumavgs), fin)
                avgs = list()
                cumavgs = list()
    print("\nEpsilon:", agent.epsilon)
    print("High Score:", maxScore)
    print("Average score:", sum(scores)/len(scores))
    return agent

def play(dim = 5, model_path= None, fps= 7):
    if not model_path:
        model_path = ".\\models\\CompleteDeepQModel"
        dim = 12
    agent = DeepQAgent.load(dim, model_path)
    agent.epsilon = 0
    game = AgentGame(dim, replayAllowed=True)
    game.play(agent)