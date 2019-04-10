import pygame


class Player():
    def __init__(self, game, paddle):
        self.game = game
        self.paddle = paddle

    def act(self):
        for event in self.game.events:
            if event.type == pygame.MOUSEMOTION:
                mousey = event.pos[1]
                self.paddle.y = mousey
