import argparse

parser = argparse.ArgumentParser(description="Play pong vs your favorite form of AI")
parser.add_argument(
    "-a1",
    "--agent1",
    nargs="?",
    type=str,
    choices=[
        "player",
        "basic",
        "q-learning",
    ],
    default="player",
    help="Type of agent for the left paddle",
)
parser.add_argument(
    "-a2",
    "--agent2",
    nargs="?",
    type=str,
    choices=[
        "player",
        "basic",
        "q-learning",
    ],
    default="q-learning",
    help="Type of agent for the right paddle",
)
