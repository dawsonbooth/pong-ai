from game import Game, Paddle


class Player:
    __slots__ = "game", "paddle", "keypress"

    game: Game
    paddle: Paddle
    keypress: bool

    def __init__(self, game, paddle):
        self.game = game
        self.paddle = paddle
        self.keypress = None

    def act(self):
        if self.keypress is not None:
            if self.keypress:
                self.paddle.move(0, 1)
            else:
                self.paddle.move(0, -1)
