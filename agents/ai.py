from collections import defaultdict
from random import shuffle

import pygame

from settings import PADDLEHEIGHT, WINDOWHEIGHT, WINDOWWIDTH


class Basic():

    def __init__(self, game, paddle):
        self.game = game
        self.paddle = paddle

    def act(self):

        target = WINDOWHEIGHT/2

        if self.game.ball.velocity.x < 0:
            if self.paddle.x < (WINDOWWIDTH / 2):
                target = self.game.ball.centery
        else:
            if self.paddle.x > (WINDOWWIDTH / 2):
                target = self.game.ball.centery

        if self.paddle.centery < target:
            self.paddle.y += 1
        elif self.paddle.centery > target:
            self.paddle.y -= 1


class ANN():
    pass


class QLearning():
    Q = defaultdict(lambda: defaultdict(int))
    alpha = .1
    gamma = .9
    epsilon = 0.1

    precision = PADDLEHEIGHT / 20

    actions = [-precision, 0, precision]
    living_cost = 1
    movement_cost = 5
    optimism = 0

    last_state = None
    last_action = None
    last_distance_ball = 0

    def __init__(self, game, paddle):
        # Game
        self.game = game
        self.paddle = paddle

        self.state = None
        self.load_state()
        self.weights = [0] * len(self.state)

    def discretize(self, state):
        out = []
        for i in range(0, len(state)):
            out.append(round(state[i] / self.precision) * self.precision)
        return out

    def load_state(self):
        self.state = self.discretize([
            self.paddle.centery,
            self.game.ball.centery,
            self.game.ball.velocity.x,
            self.game.ball.velocity.y])

    def make_key(self, arr):
        arr2 = []
        for i in range(0, len(arr)):
            v = round((int(arr[i]) + 100) / self.precision) * \
                self.precision if type(arr[i]) == "string" else arr[i]
            arr2.append(v)
        return str(arr2)

    def get_q_value(self, s, a):
        s_key = self.make_key(s)
        a_key = str(a)
        return self.Q[s_key][a_key]

    def set_q_value(self, s, a, value):
        s_key = self.make_key(s)
        a_key = str(a)
        self.Q[s_key][a_key] = value

    def V_value(self, s):
        m = -float("inf")
        for i in range(0, len(self.actions)):
            m = max(m, self.get_q_value(s, self.actions[i]))
        return m

    def select_action(self):
        shuffle(self.actions)
        best_action = None
        best_score = -float("inf")
        for i in range(0, len(self.actions)):
            action = self.actions[i]
            score = self.get_q_value(self.state, action) + self.optimism

            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def perform_action(self, action):
        self.paddle.y += action

    def learn_from_action(self, s, a, r, s_prime):
        cur_q_value = self.get_q_value(s, a)
        diff = r + self.gamma * self.V_value(s_prime) - cur_q_value
        value = cur_q_value + self.alpha * diff
        self.set_q_value(s, a, value)

        for i in range(0, len(self.weights)):
            self.weights[i] += self.alpha * diff * s_prime[i]

    def act(self):

        self.load_state()

        # Learn
        reward = 0
        if (self.last_state and self.last_action):

            y_distance = abs(self.paddle.centery - self.game.ball.centery)
            reward -= y_distance

            reward -= self.living_cost
            if self.last_action != 0:
                reward -= self.movement_cost

            self.learn_from_action(
                self.last_state, self.last_action, reward, self.state)

        action = self.select_action()

        self.last_state = self.state
        self.last_action = action

        self.perform_action(action)
