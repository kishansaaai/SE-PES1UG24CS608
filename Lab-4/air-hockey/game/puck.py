"""
Puck: the disc players are trying to hit into the opponent's goal.
"""


class Puck:
    def __init__(self, x, y, radius=12):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0.0
        self.vy = 0.0

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def bounce_off_walls(self, height, margin):
        """Bounce off the top and bottom walls only - left/right are handled
        separately by the game engine, since they contain the goals."""
        if self.y - self.radius < margin:
            self.y = margin + self.radius
            self.vy = -self.vy
        elif self.y + self.radius > height - margin:
            self.y = height - margin - self.radius
            self.vy = -self.vy
