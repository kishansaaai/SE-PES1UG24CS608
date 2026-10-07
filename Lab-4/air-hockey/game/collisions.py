"""
collisions: puck-vs-paddle collision handling.
"""


def handle_paddle_collision(puck, paddle):
    """
    If the puck overlaps the paddle, bounce it off.
    Returns True if a collision was handled this frame.
    """
    dx = puck.x - paddle.x
    dy = puck.y - paddle.y
    distance = (dx ** 2 + dy ** 2) ** 0.5

    if distance < puck.radius + paddle.radius:
        puck.vx = -puck.vx
        return True

    return False
