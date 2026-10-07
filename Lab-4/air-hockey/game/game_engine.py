"""
GameEngine: owns the puck, both paddles, and the computer AI, and runs
one frame's worth of game logic.

Starter version: the puck bounces around and paddles can hit it, but
there is no scoring, no match timer, and the reset that happens after
a goal is incomplete. That's what Tasks 2-4 fix/add.
"""

import math
import random
import time

from game.puck import Puck
from game.paddle import Paddle
from game.ai import ComputerAI
from game.collisions import handle_paddle_collision
from game.renderer import WIDTH, HEIGHT, MARGIN, GOAL_TOP, GOAL_BOTTOM

PLAYER_SPEED = 6
PUCK_RADIUS = 12
PADDLE_RADIUS = 28
INITIAL_PUCK_SPEED = 4.5
MATCH_SECONDS = 30


class GameEngine:
    def __init__(self, clock=time.monotonic):
        self._clock = clock          # injectable so the timer can be tested
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

        self.player_score = 0
        self.computer_score = 0
        self.game_over = False
        self.result = ""
        self._start_time = self._clock()

    def _launch_puck(self):
        angle_choices = [0.3, 0.6, -0.3, -0.6]
        direction = random.choice([-1, 1])
        vy_factor = random.choice(angle_choices)
        self.puck.vx = INITIAL_PUCK_SPEED * direction
        self.puck.vy = INITIAL_PUCK_SPEED * vy_factor

    def restart(self):
        """Start a brand-new match (bound to the R key)."""
        self.__init__(self._clock)

    def time_left(self):
        if self.game_over:
            return 0
        return max(0.0, MATCH_SECONDS - (self._clock() - self._start_time))

    def _end_match(self):
        self.game_over = True
        self.puck.vx = self.puck.vy = 0.0
        if self.player_score > self.computer_score:
            self.result = "YOU WIN!"
        elif self.computer_score > self.player_score:
            self.result = "COMPUTER WINS!"
        else:
            self.result = "DRAW"

    def handle_input(self, keys_pressed):
        import pygame
        if keys_pressed[pygame.K_r]:
            self.restart()
            return
        if self.game_over:
            return
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
        if self.game_over:
            return
        if self.time_left() <= 0:
            self._end_match()
            return

        self.computer.vx = self.computer.vy = 0.0
        self.ai.update(self.computer, self.puck)

        # Sub-step the puck so fast shots can't tunnel through a paddle.
        speed = math.hypot(self.puck.vx, self.puck.vy)
        steps = max(1, math.ceil(speed / (self.puck.radius * 0.5)))
        for _ in range(steps):
            self.puck.x += self.puck.vx / steps
            self.puck.y += self.puck.vy / steps
            self.puck.bounce_off_walls(HEIGHT, MARGIN)
            bounds = self._puck_bounds()
            handle_paddle_collision(self.puck, self.player, bounds)
            handle_paddle_collision(self.puck, self.computer, bounds)
            self._handle_goals()

    def _puck_bounds(self):
        """Area the puck's centre may occupy. The end walls don't apply in
        the goal gap, so the puck may travel into a goal there."""
        r = self.puck.radius
        if GOAL_TOP < self.puck.y < GOAL_BOTTOM:
            lo_x, hi_x = -1e9, 1e9
        else:
            lo_x, hi_x = MARGIN + r, WIDTH - MARGIN - r
        return (lo_x, hi_x, MARGIN + r, HEIGHT - MARGIN - r)

    def _handle_goals(self):
        """A goal counts only when the puck is in the goal gap AND has fully
        crossed the end line. Anywhere else the end wall bounces it back."""
        p = self.puck
        in_gap = GOAL_TOP < p.y < GOAL_BOTTOM

        if p.x - p.radius < MARGIN:                      # touching left wall
            if in_gap:
                if p.x + p.radius < MARGIN:              # fully past the line
                    self.computer_score += 1             # went into player's goal
                    self._reset_puck()
            else:
                p.x = MARGIN + p.radius
                p.vx = -p.vx
        elif p.x + p.radius > WIDTH - MARGIN:            # touching right wall
            if in_gap:
                if p.x - p.radius > WIDTH - MARGIN:      # fully past the line
                    self.player_score += 1               # went into computer's goal
                    self._reset_puck()
            else:
                p.x = WIDTH - MARGIN - p.radius
                p.vx = -p.vx

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
        renderer.draw_text(surface, font, f"YOU {self.player_score}", (WIDTH // 4 - 40, 30))
        renderer.draw_text(surface, font, f"CPU {self.computer_score}", (3 * WIDTH // 4 - 40, 30))
        renderer.draw_text(surface, font, f"{math.ceil(self.time_left()):02d}s", (WIDTH // 2 - 22, 30))
        if self.game_over:
            renderer.draw_banner(surface, font, f"{self.result}  -  press R to restart")
