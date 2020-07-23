import sys
from math import sqrt
from random import choice, random

import arcade

from settings import *


class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError(f"not valid key '{key}'")


class Rectangle:
    def __init__(self, x, y, width, height, color=WHITE):
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.left = self.x - self.width / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y - self.height / 2
        self.top = self.y + self.height / 2

        self.color = color

    def draw(self):
        arcade.draw_rectangle_filled(
            self.x, self.y, self.width, self.height, WHITE)

    def move(self, del_x, del_y):
        # Horizontal
        self.x += del_x
        self.left += del_x
        self.right += del_x

        # Vertical
        self.y += del_y
        self.bottom += del_y
        self.top += del_y

    def teleport(self, x, y):
        self.x = x
        self.y = y

        self.left = self.x - self.width / 2
        self.right = self.x + self.width / 2
        self.bottom = self.y - self.height / 2
        self.top = self.y + self.height / 2


class Paddle(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = 0


class Ball(Rectangle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity = Vector2(1, 1)


class Arena():
    def __init__(self, paddle1, paddle2):
        self.paddle1 = paddle1
        self.paddle2 = paddle2

    def draw(self):
        # Draw outline of arena
        arcade.draw_rectangle_outline(
            WINDOWWIDTH / 2, WINDOWHEIGHT / 2, WINDOWWIDTH, WINDOWHEIGHT, WHITE, LINETHICKNESS*2)
        # Draw centre line
        arcade.draw_rectangle_filled(
            WINDOWWIDTH / 2, WINDOWHEIGHT / 2, LINETHICKNESS/4, WINDOWHEIGHT, WHITE)

        arcade.draw_text(str(self.paddle1.score), WINDOWWIDTH / 2 - FONTSIZE,
                         WINDOWHEIGHT - FONTSIZE, WHITE, FONTSIZE, align="center", anchor_x="center", anchor_y="center")
        arcade.draw_text(str(self.paddle2.score), WINDOWWIDTH / 2 + FONTSIZE,
                         WINDOWHEIGHT - FONTSIZE, WHITE, FONTSIZE, align="center", anchor_x="center", anchor_y="center")


class Game(arcade.Window):
    def __init__(self, agent1, agent2):
        super().__init__(WINDOWWIDTH, WINDOWHEIGHT, WINDOWTITLE)

        self.paddle1 = Paddle(
            PADDLEOFFSET, WINDOWHEIGHT / 2, LINETHICKNESS, PADDLEHEIGHT)
        self.paddle2 = Paddle(WINDOWWIDTH - PADDLEOFFSET,
                              WINDOWHEIGHT / 2, LINETHICKNESS, PADDLEHEIGHT)
        self.ball = Ball(WINDOWWIDTH/2, WINDOWHEIGHT/2,
                         LINETHICKNESS, LINETHICKNESS)
        self.arena = Arena(self.paddle1, self.paddle2)

        self.agent1 = agent1(self, self.paddle1)
        self.agent2 = agent2(self, self.paddle2)

    def setup(self):
        # Schedule advance
        arcade.schedule(self.advance, 1 / FPS)

    def on_key_press(self, key, modifiers):

        if self.agent1.__class__.__name__ == "Player":
            if key == arcade.key.UP:
                self.agent1.keypress = True
            elif key == arcade.key.DOWN:
                self.agent1.keypress = False
        if self.agent2.__class__.__name__ == "Player":
            if key == arcade.key.UP:
                self.agent2.keypress = True
            elif key == arcade.key.DOWN:
                self.agent2.keypress = False

    def on_key_release(self, key, modifiers):

        if self.agent1.__class__.__name__ == "Player":
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.agent1.keypress = None
        if self.agent2.__class__.__name__ == "Player":
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.agent2.keypress = None

    def on_draw(self):
        arcade.start_render()

        self.arena.draw()
        self.paddle1.draw()
        self.paddle2.draw()
        self.ball.draw()

    def advance(self, delta_time: float):
        self.ball.move(*self.ball.velocity)
        self.agent1.act()
        self.agent2.act()
        self.check_edge_collision()
        self.check_point_scored()
        self.check_hit_ball()

    # Checks for a collision with a wall, and 'bounces' ball off it.
    # Returns new direction
    def check_edge_collision(self):
        b = self.ball
        if b.top > WINDOWHEIGHT - LINETHICKNESS:
            b.teleport(b.x, min(b.y, WINDOWHEIGHT - (b.height / 2)))
            self.ball.velocity.y *= -1
        elif b.bottom < LINETHICKNESS:
            b.teleport(b.x, max(b.y, b.height / 2))
            self.ball.velocity.y *= -1

    # Checks is the ball has hit a paddle, and 'bounces' ball off it.
    def check_hit_ball(self):
        p1 = self.paddle1
        p2 = self.paddle2
        b = self.ball
        p1_hits_b = b.left < p1.right and b.right > p1.left and (
            (b.bottom < p1.top and b.bottom > p1.bottom) or (b.top > p1.bottom and b.top < p1.top))
        p2_hits_b = b.left < p2.right and b.right > p2.left and (
            (b.bottom < p2.top and b.bottom > p2.bottom) or (b.top > p2.bottom and b.top < p2.top))
        if p1_hits_b:
            b.teleport(p1.right + b.width / 2, b.y)
            b.velocity.x *= -1
        elif p2_hits_b:
            b.teleport(p2.left - b.width / 2, b.y)
            b.velocity.x *= -1

    # Checks to see if a point has been scored returns new score
    def check_point_scored(self):
        p1 = self.paddle1
        p2 = self.paddle2
        b = self.ball
        if b.left < LINETHICKNESS:
            p2.score += 1
            b.teleport(WINDOWWIDTH/2, WINDOWHEIGHT/2)
            b.velocity.x *= -1
        elif b.left > WINDOWWIDTH - LINETHICKNESS:
            p1.score += 1
            b.teleport(WINDOWWIDTH/2, WINDOWHEIGHT/2)
            b.velocity.x *= -1
