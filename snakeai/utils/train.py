import logging
import pickle as pkl
from typing import Tuple, List, Type
from tqdm import tqdm

from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.agent_controller import AgentGame


def general_train(agent: AbstractAgent, episodes: int, size: int, show=False, avg_length=1000) -> Tuple[AbstractAgent, List[int]]:
    """ Train the given agent and return the trained agent together with a list of scores

    Parameters
    ----------
    agent: AbstractAgent
        The agent to be trained
    episodes: int
        The number of episodes to train the agent for
    size: int
        The size of the board
    show: bool, default=False
        Whether the screen should be shown during training
    avg_length: int, default = 1000
        The size of the sliding window for the average shown during training

    Returns
    -------
    tuple(AbstractAgent, list(int) )
        The trained agent and a list with the scores achieved for each episode of training
    """
    scores = []
    t = tqdm(range(episodes))
    max_score = 0
    avg = 0
    for _ in t:
        game = AgentGame(size, show=show, replay_allowed=False)
        game.play(agent)
        scores.append(game.model.score)
        agent.reset()
        length = min(len(scores), avg_length)
        avg = sum(scores[-length:])/length
        max_score = max(max_score, scores[-1])
        t.set_postfix_str(f"HS: {max_score}, avg: {avg:.2f}")
    print("\nEpsilon:", agent.epsilon)
    print("High Score:", max_score)
    print("Average score:", avg)
    return agent, scores


def test_agent(agent: AbstractAgent, trials: int = 50) -> Tuple[int, float]:
    """Test the agent for a certain number of time to calculate average and maximum score

    Parameters
    ----------
    agent: AbstractAgent
        Teh agent to be tested
    trials: int, default=50
        The number of run to execute to get the statistics

    Returns
    -------
    int, float
        The maximum score achieved and the average score

    """
    epsilon = agent.epsilon
    board_size = agent.dim
    agent.epsilon = 0
    scores = []
    for _ in tqdm(range(trials)):
        game = AgentGame(board_size, show=False)
        game.play(agent)
        scores.append(game.model.score)
        agent.reset()
    agent.epsilon = epsilon
    return max(scores), sum(scores)/len(scores)


def train_and_play(cls: Type[AbstractAgent], board_size: int, episodes: int, output_model: str, model_input_file=None,
                   avg_length=500, score_file=None, version=1, test_run=50):
    """A method for executing a full training of any agent

    This method will train an agent (either by creating a new one or by loading it from a file). then it will test it
    for showing the stats after training. both the model and (optionally) the scores are saved to a file and finally the
    agent plays on a screen visible to the user

    Parameters
    ----------
    cls: Type[AbstractAgent]
        The class of agent to be trained
    board_size: int
        the size of the board
    episodes: int
        the number of epsiodes to train the agent for
    output_model: str
        The path where the model should be saved after training.
    model_input_file: str, optional
        If given, the file from which a pretrained model can be loaded (instead of training a new one)
    avg_length: int, default=500
        The length of the window for the moving average during training
    score_file: str, optional
        If given, the scores will be saved in a file with path `score_file`+`version`
    version: int, default=1
        The version number (used for saving the scores)
    test_run: int, default = 50
        The number of runs for testing the agent
    """
    logging.basicConfig(level=logging.INFO, format="%(module)s - %(levelname)s - %(message)s")

    # Create Agent
    if model_input_file:
        agent = cls.load(board_size, model_input_file)
        agent.epsilon = 0.01
    else:
        agent = cls(board_size)

    # Train Agent
    trained_agent, all_scores = general_train(agent, episodes=episodes, size=board_size,
                                              avg_length=avg_length, show=False)

    # Save Agent
    trained_agent.save(output_model)
    if score_file:
        with open(score_file+str(version)+".pkl", "wb") as f_out:
            pkl.dump(all_scores, f_out)

    # Test trained Agent
    max_score, avg = test_agent(agent, test_run)
    print("---Stats with epsilon=0---")
    print("Average:", avg)
    print("High score:", max_score)

    # Play with Agent
    game = AgentGame(board_size, replay_allowed=True, fps=7)
    game.play(trained_agent)
