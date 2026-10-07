"""
Paddle: a player's or the computer's mallet, confined to their own half
of the table.
"""


class Paddle:
    def __init__(self, x, y, radius, min_x, max_x, min_y, max_y):
        self.x = x
        self.y = y
        self.radius = radius
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def clamp(self):
        self.x = max(self.min_x, min(self.max_x, self.x))
        self.y = max(self.min_y, min(self.max_y, self.y))

    def move_by(self, dx, dy):
        self.x += dx
        self.y += dy
        self.clamp()

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.clamp()
