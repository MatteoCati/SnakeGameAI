from snakeai.game.agent_controller import AgentGame
from snakeai.agents.simple_tabular_agent import SimpleStateAgent
from collections import deque
from tqdm import tqdm


def train(episodes, size, show=False, agent: SimpleStateAgent = None):
    """Train a StateAgent

    This method will train a StateAgent for a certain amount of steps.
    Then it will print some stats about it. The agent will be returned by the function. The
    states are not saved on a file.

    Parameters
    -----------
    episodes: int
        The number of episodes in which the agent is trained
    size: int
        The size of the board (side length)
    show: bool, default=False
        Whether the GUI should be visible
    agent: StateAgent, optional
        The agent to be trained
    """
    if not agent:
        agent = SimpleStateAgent(size)
    maxScore = 0
    scores = deque(maxlen=1000)
    for i in tqdm(range(episodes)):
        game = AgentGame(size, show=show, replay_allowed=False, fps=15)
        game.play(agent)
        scores.append((game.model.score))
        maxScore = max(maxScore, game.model.score)
        agent.reset()
    print("Epsilon:", agent.epsilon)
    print("High Score:", maxScore)
    print("Average score:", sum(scores) / len(scores))
    return agent


def play(dim=5, model_path=None, fps=7):
    if not model_path:
        model_path = ".\\models\\CompleteSimpleStateAgentDictionary"
        dim = 4
    agent = SimpleStateAgent.load(dim, model_path)
    agent.epsilon = 0
    game = AgentGame(dim, fps=fps, replay_allowed=True)
    game.play(agent)
