"""
ComputerAI: controls the computer's paddle.

Tracks the puck's vertical position, but not perfectly - it only
re-aims periodically (a small reaction delay) and aims with a bit of
imprecision, so it can be beaten with a well-placed or fast shot
instead of blocking everything by default.
"""

import random

SPEED = 3.5
REACTION_DELAY_FRAMES = 6   # only re-aims every few frames, not every frame
TRACKING_ERROR = 18         # px of aiming imprecision


class ComputerAI:
    def __init__(self, speed=SPEED):
        self.speed = speed
        self.reaction_delay = REACTION_DELAY_FRAMES
        self.tracking_error = TRACKING_ERROR
        self._delay_counter = 0
        self._target_y = None

    def update(self, paddle, puck):
        if self._target_y is None or self._delay_counter <= 0:
            error = random.uniform(-self.tracking_error, self.tracking_error)
            self._target_y = puck.y + error
            self._delay_counter = self.reaction_delay
        else:
            self._delay_counter -= 1

        if self._target_y < paddle.y - 2:
            paddle.move_by(0, -self.speed)
        elif self._target_y > paddle.y + 2:
            paddle.move_by(0, self.speed)
