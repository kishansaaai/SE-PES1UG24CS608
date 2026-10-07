"""
GameEngine: owns the puck, both paddles, and the computer AI, and runs
one frame's worth of game logic.

Starter version: the puck bounces around and paddles can hit it, but
there is no scoring, no match timer, and the reset that happens after
a goal is incomplete. That's what Tasks 2-4 fix/add.
"""

import random

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM

PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5


class GameEngine:
    def __init__(self):
        self.puck = Puck(WIDTH / 2, HEIGHT / 2, PUCK_RADIUS)
        self._launch_puck()

        self.player = Paddle(
            x=WIDTH * 0.15, y=HEIGHT / 2, radius=PADDLE_RADIUS,
            min_x=MARGIN + PADDLE_RADIUS, max_x=WIDTH / 2 - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS, max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )
        self.computer = Paddle(
            x=WIDTH * 0.85, y=HEIGHT / 2, radius=PADDLE_RADIUS,
            min_x=WIDTH / 2 + PADDLE_RADIUS, max_x=WIDTH - MARGIN - PADDLE_RADIUS,
            min_y=MARGIN + PADDLE_RADIUS, max_y=HEIGHT - MARGIN - PADDLE_RADIUS,
        )
        self.ai = ComputerAI()

    def _launch_puck(self):
        angle_choices = [0.3, 0.6, -0.3, -0.6]
        direction = random.choice([-1, 1])
        vy_factor = random.choice(angle_choices)
        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

    def handle_input(self, keys_pressed):
        import pygame
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN]:
            dy += PLAYER_SPEED
        if keys_pressed[pygame.K_LEFT]:
            dx -= PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            dx += PLAYER_SPEED
        self.player.move_by(dx, dy)

    def update(self):
        self.ai.update(self.computer, self.puck)

        self.puck.move()
        self.puck.bounce_off_walls(HEIGHT, MARGIN)

        handle_paddle_collision(self.puck, self.player)
        handle_paddle_collision(self.puck, self.computer)

        self._handle_goals()

    def _handle_goals(self):
        if self.puck.x - self.puck.radius < MARGIN:
            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
                self._reset_puck()
            else:
                self.puck.x = MARGIN + self.puck.radius
                self.puck.vx = -self.puck.vx
        elif self.puck.x + self.puck.radius > WIDTH - MARGIN:
            if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
                self._reset_puck()
            else:
                self.puck.x = WIDTH - MARGIN - self.puck.radius
                self.puck.vx = -self.puck.vx

    def _reset_puck(self):
        self.puck.x, self.puck.y = WIDTH / 2, HEIGHT / 2
        self.puck.vx = 0
        self.puck.vy = 0

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_table(surface)
        renderer.draw_paddle(surface, self.player, renderer.COLOR_PLAYER)
        renderer.draw_paddle(surface, self.computer, renderer.COLOR_COMPUTER)
        renderer.draw_puck(surface, self.puck)
