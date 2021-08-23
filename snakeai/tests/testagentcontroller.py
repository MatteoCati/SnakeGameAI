from snakeai.game.agent_controller import AgentGame
from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.constants import Actions

if __name__ =="__main__":
    class MockAgent(AbstractAgent):
        def __init__(self, dim):
            self.count = 0
            super().__init__(dim)

        def reset(self):
            pass

        def fit(self, oldSnake, oldApple, rew, snake, apple, done):
            print("Training ", self.count)
            self.count+=1
        
        def execute(self, snake, apple) -> Actions:
            return Actions.RIGHT
        
    agent = MockAgent(20)
    game = AgentGame(20, show = True)
    game.play(agent)