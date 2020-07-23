import arcade

from agents import AI, Player
from cli import parser
from game import Game


# Main function
def main(args):
    # Dictionary to associate argument with agent
    agents_dict = {
        'player': Player.Player,
        'basic': AI.Basic,
        'q-learning': AI.QLearning,
    }

    # Agent 1 - left paddle
    a1 = agents_dict[args.agent1]

    # Agent 2 - right paddle
    a2 = agents_dict[args.agent2]

    # Set up game
    game = Game(a1, a2)
    game.setup()

    # Run game
    arcade.run()


if __name__ == '__main__':
    # Parse arguments
    args = parser.parse_args()

    # Run program
    main(args)
