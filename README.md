# SnakeAI
This library implements an environment for the Snake Game. This can be used for playing, but also for training  Reinforcement
Learning agents.

# Table of Contents
1. [Playing Snake](#paragraph1)
2. [Playing with an RL Agent](#paragraph2)
3. [Training an agent](#paragraph3)


##Playing Snake <a name="paragraph1"></a>
To play the game, you just need to create a `UserGame` object and call the `play` method.
```python
from snakeai.game.user_controller import UserGame
game = UserGame(20)
game.play()
```
The number specified in the `UserGame` definition is the dimension of the board (the length of its side).
To change direction, you need to use the arrow keys. At the end of the game, press `R` to play again.

You can also choose whether to play in a new window or inside the command line, by specifying the mode when creating the 
`UserGame` object. This can be `GUIMode.WINDOW` or `GUIMode.CLI`.
```python
from snakeai.game.user_controller import UserGame
from snakeai.game.constants import GUIMode
game = UserGame(20, mode=GUIMode.CLI)
game.play()
```
In this case, to play you need to write `up`, `down`, `left`, `right`.

##Playing with a RL Agent <a name="paragraph2"></a>

There are five different agents you can choose from, contained in the `snakeai.agents` package:
* `recursive_agent.Recursive` uses a simulated environment to find the best move 
* `tabular_agent.StateAgent` uses the Sarsa algorithm. The states describe the board exactly
* `simple_tabular_agent.SimpleStateAgent` uses the Sarsa algrithm, with simplified states
* `simple_mc_agent.SimpleMCAgent` uses the Monte Carlo method, with simplified states
* `simple_deep_agent.DQN` uses a Deep Q Network, with simplified states.

The agents labelled as "simple" use as state an array composed of 12 boolean values. The `StateAgent`, instead, uses
a complete description of the board. 

To play with one of these agents, you can use the `play` method from the relevant module. For example, to play with the
`SimpleStateAgent` (contained in the `snakeai.agents.simple_tabular_agent` module):
```python
from snakeai.agents.simple_tabular_agent import play
play()
```
If you do not specify a path, the program will use a default model. 

##Training an agent <a name="paragraph3"></a>
To train one of these agents, you can use the following code:
```python
from snakeai.agents.simple_tabular_agent import  SimpleStateAgent
from snakeai.game.agent_controller import AgentGame

episodes = 100_000
game = AgentGame(dim=20, show=False)
agent = SimpleStateAgent(20)
for _ in range(episodes):
    game.play(agent)
    agent.reset()
```

Then you can save an agent using the `save` method. The path should end without any extension.
```python
agent.save(path = "./models/my_agent")
```

