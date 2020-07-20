# `pong-ai`


## Description

This program is a clone for the classic Pong game. With a CLI activation, the user has the option of playing against another user, a specialized "AI agent," or a basic computer player that follows the ball. Currently, the only agent is a Q-learning AI. Further plans include additional agents that use other various decision-making structures, such as a neural network or a Markov decision process.

## Installation

With [Git](https://git-scm.com/downloads), [Python](https://www.python.org/downloads/), and [Poetry](https://python-poetry.org/docs/) installed, simply run the following command to get the project on your machine.

```bash
git clone https://github.com/dawsonbooth/pong-ai
```

The game may additionally run slowly on macOS as opposed to a Windows PC. Solutions to this are not well documented, and given the scope of the project a PC may be better suited for the program anyway.

## Usage

This is a command-line program. The main file, `pong.py` can be executed as follows:

```bash
python pong.py [-h] [-a1 [{player,basic,q-learning}]] [-a2 [{player,basic,q-learning}]]
```

Optional arguments:

```
  -h, --help			Show the help message and exit
  -a1, --agent1 {player,basic,q-learning}
                    	Type of agent for the left paddle
  -a2, --agent2 {player,basic,q-learning}
                    	Type of agent for the right paddle
```

## License

This software is released under the terms of [MIT license](LICENSE).
