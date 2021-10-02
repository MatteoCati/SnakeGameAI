from snakeai.agents.tabular_agent import StateAgent
from snakeai.tests.teststateagent import  play, train

if __name__ == "__main__":
    agent = StateAgent.load(5, ".\\models\\CompleteStateAgent")
    agent.epsilon = 0.3
    trained_agent = train(10_000, 5, agent=agent)
    trained_agent.save(".\\models\\CompleteStateAgent")
    play(5, ".\\models\\CompleteStateAgent")
