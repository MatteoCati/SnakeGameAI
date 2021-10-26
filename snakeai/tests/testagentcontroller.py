from snakeai.game.agent_controller import AgentGame
from snakeai.agents.agent_interface import AbstractAgent
from snakeai.game.constants import Actions

"""Use this mdule to check if AgentGame works correctly"""

if __name__ =="__main__":
    class MockAgent(AbstractAgent):
        def __init__(self, dim):
            self.count = 0
            super().__init__(dim)

        def reset(self):
            pass

        def fit(self, oldState, action, rew, state, done):
            print("Training ", self.count)
            self.count+=1
        
        def execute(self, state) -> Actions:
            return Actions.RIGHT

        @classmethod
        def load(cls, dim, model_path):
            pass

        def save(self, model_path = None):
            pass
        
    agent = MockAgent(20)
    game = AgentGame(20, show=True, replay_allowed=True)
    game.play(agent)
