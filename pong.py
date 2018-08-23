import argparse

from agents import AI, Player
from game import Game

# Dictionary to associate argument with agent
agents_dict = {
    "player": Player,
    "basic": AI.Basic,
    "q-learning": AI.QLearning,
}

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a1", "--agent1", type=str, choices=[
                    "player", "basic", "q-learning", ], help="Type of player for the left paddle")
parser.add_argument("-a2", "--agent2", type=str, choices=[
                    "player", "basic", "q-learning", ], help="Type of player for the right paddle")
args = parser.parse_args()

# Main function
def main():
    # Set up game
    pong = Game()
    pong.setup()

    # Agent 1 - left paddle
    if args.agent1:
        p1 = agents_dict[args.agent1](pong, pong.paddle1)
    else:
        p1 = AI.Basic(pong, pong.paddle1)

    # Agent 2 - right paddle
    if args.agent2:
        p2 = agents_dict[args.agent2](pong, pong.paddle2)
    else:
        p2 = AI.QLearning(pong, pong.paddle2)

    # Game loop
    while True:
        pong.advance()
        p1.act()
        p2.act()


if __name__ == '__main__':
    main()
