# Description

This program is a clone for the classic Pong game. With a CLI activation, the user has the option of playing against another user, a specialized "AI agent," or a basic computer player that follows the ball. Currently, the only agent is a Q-learning AI. Further plans include additional agents that use other various decision-making structures, such as a neural network or a Markov decision process.

# Installation

With Git installed, simply clone the repository using the command:

```bash
git clone https://github.com/dawsonbooth/pong-ai.git
```

Next, make sure PyGame is installed.

```bash
pip install pygame
```

_Currently, PyGame/Python has issues with recent versions of macOS. If you experience a dark screen when running PyGame, try using the following command to install a working version:_

```bash
pip3 install pygame==2.0.0.dev4
```

This issue is discussed further <a href="https://github.com/pygame/pygame/issues/555#issuecomment-541237897">here</a>.

The game may additionally run slowly on macOS as opposed to a Windows PC. Solutions to this are not well documented, and given the scope of the project a PC may be better suited for the program anyway.

# Usage

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
