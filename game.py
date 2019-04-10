import sys
from math import sqrt
from random import choice, random

import pygame
from pygame.math import Vector2

from constants import *


# Game Objects
class Paddle(pygame.Rect):
    score = 0

    def __init__(self, left, top, **kwargs):
        super().__init__(left, top, LINETHICKNESS, PADDLEHEIGHT)
        self.color = kwargs.get("color") if kwargs.get("color") else WHITE


class Ball(pygame.Rect):

    def __init__(self, left, top, **kwargs):
        super().__init__(left, top, LINETHICKNESS, LINETHICKNESS)
        self.color = kwargs.get("color") if kwargs.get("color") else WHITE
        self.velocity = Vector2(1, 1)


# Game
class Game():

    def setup(self):
        # Set up game
        pygame.init()

        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption(WINDOWTITLE)

        # Creates Rectangles for ball and paddles.
        self.paddle1 = Paddle(PADDLEOFFSET, (WINDOWHEIGHT - PADDLEHEIGHT) / 2)
        self.paddle2 = Paddle(WINDOWWIDTH - PADDLEOFFSET -
                              LINETHICKNESS, (WINDOWHEIGHT - PADDLEHEIGHT) / 2)
        self.ball = Ball(WINDOWWIDTH/2 - LINETHICKNESS/2,
                         WINDOWHEIGHT/2 - LINETHICKNESS/2)

        # Draws the elements of the game
        self.draw_arena()
        self.draw_paddle(self.paddle1)
        self.draw_paddle(self.paddle2)
        self.draw_ball()
        self.display_score()

        self.events = pygame.event.get()

    def advance(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        self.draw_arena()
        self.draw_paddle(self.paddle1)
        self.draw_paddle(self.paddle2)
        self.draw_ball()
        self.display_score()

        self.move_ball()
        self.check_edge_collision()
        self.check_point_scored()
        self.check_hit_ball()

        pygame.display.update()
        self.FPSCLOCK.tick(FPS)

    # Draws the arena the game will be played in.
    def draw_arena(self):
        self.DISPLAYSURF.fill(BLACK)
        # Draw outline of arena
        pygame.draw.rect(self.DISPLAYSURF, WHITE, ((
            0, 0), (WINDOWWIDTH, WINDOWHEIGHT)), LINETHICKNESS*2)
        # Draw centre line
        pygame.draw.line(self.DISPLAYSURF, WHITE, ((WINDOWWIDTH/2), 0),
                         ((WINDOWWIDTH/2), WINDOWHEIGHT), int(LINETHICKNESS/4))

    # Draws the paddle

    def draw_paddle(self, paddle):
        paddle.top = max(LINETHICKNESS, paddle.top)

        paddle.bottom = min(WINDOWHEIGHT - LINETHICKNESS, paddle.bottom)

        # Draws paddle
        pygame.draw.rect(self.DISPLAYSURF, paddle.color, paddle)

    # draws the ball
    def draw_ball(self):
        self.ball.top = max(LINETHICKNESS, self.ball.top)
        self.ball.bottom = min(WINDOWHEIGHT - LINETHICKNESS, self.ball.bottom)
        self.ball.right = max(LINETHICKNESS, self.ball.right)
        self.ball.left = min(WINDOWWIDTH - LINETHICKNESS, self.ball.left)

        pygame.draw.rect(self.DISPLAYSURF, self.ball.color, self.ball)

    # moves the ball returns new position
    def move_ball(self):
        self.ball.x += self.ball.velocity.x
        self.ball.y += self.ball.velocity.y
        print(self.ball.velocity)

    # Checks for a collision with a wall, and 'bounces' ball off it.
    # Returns new direction
    def check_edge_collision(self):
        if self.ball.top == (LINETHICKNESS) or self.ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
            self.ball.velocity.y *= -1

    # Checks is the ball has hit a paddle, and 'bounces' ball off it.
    def check_hit_ball(self):

        if (self.ball.velocity.x < 0 and self.paddle1.right == self.ball.left and self.paddle1.top - LINETHICKNESS < self.ball.top and self.paddle1.bottom + LINETHICKNESS > self.ball.bottom) or (self.ball.velocity.x > 0 and self.paddle2.left == self.ball.right and self.paddle2.top < self.ball.top and self.paddle2.bottom > self.ball.bottom):
            self.ball.velocity.x *= -1

    # Checks to see if a point has been scored returns new score
    def check_point_scored(self):
        if self.ball.left == LINETHICKNESS:
            self.paddle2.score += 1
            self.ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2
            self.ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2
            self.ball.velocity.x *= -1
        elif self.ball.right == WINDOWWIDTH - LINETHICKNESS:
            self.paddle1.score += 1
            self.ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2
            self.ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2
            self.ball.velocity.x *= -1

    # Displays the current score on the screen
    def display_score(self):
        font = pygame.font.Font(None, 200)
        resultSurf1 = font.render(str(self.paddle1.score), True, WHITE)
        resultRect1 = resultSurf1.get_rect()
        resultRect1.topleft = (SCOREOFFSET, 25)

        resultSurf2 = font.render(str(self.paddle2.score), True, WHITE)
        resultRect2 = resultSurf2.get_rect()
        resultRect2.topleft = (
            WINDOWWIDTH - SCOREOFFSET - resultRect1.width, 25)

        self.DISPLAYSURF.blit(resultSurf1, resultRect1)
        self.DISPLAYSURF.blit(resultSurf2, resultRect2)
