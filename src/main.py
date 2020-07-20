from agents import AI, Player
from cli import parser
from game import Game


# Main function
def main(args):
    # Set up game
    game = Game()
    game.setup()

    # Dictionary to associate argument with agent
    agents_dict = {
        'player': Player.Player,
        'basic': AI.Basic,
        'q-learning': AI.QLearning,
    }

    # Agent 1 - left paddle
    a1 = agents_dict[args.agent1](game, game.paddle1)

    # Agent 2 - right paddle
    a2 = agents_dict[args.agent2](game, game.paddle2)

    # Game loop
    while True:
        game.advance()
        a1.act()
        a2.act()


if __name__ == '__main__':
    # Parse arguments
    args = parser.parse_args()

    # Run program
    main(args)
