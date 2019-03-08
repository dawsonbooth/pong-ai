import argparse

from agents import AI, Player
from game import Game


# Main function
def main(args):
    # Set up game
    pong = Game()
    pong.setup()

    # Dictionary to associate argument with agent
    agents_dict = {
        'player': Player,
        'basic': AI.Basic,
        'q-learning': AI.QLearning,
    }

    # Agent 1 - left paddle
    p1 = agents_dict[args.agent1](pong, pong.paddle1)

    # Agent 2 - right paddle
    p2 = agents_dict[args.agent2](pong, pong.paddle2)

    # Game loop
    while True:
        pong.advance()
        p1.act()
        p2.act()


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Play pong vs your favorite form of AI')
    parser.add_argument('-a1', '--agent1', nargs='?', type=str,
                        choices=['player', 'basic', 'q-learning', ],
                        default='basic',
                        help='Type of player for the left paddle')
    parser.add_argument('-a2', '--agent2', nargs='?', type=str,
                        choices=['player', 'basic', 'q-learning', ],
                        default='q-learning',
                        help='Type of player for the right paddle')
    args = parser.parse_args()

    # Run program
    main(args)
