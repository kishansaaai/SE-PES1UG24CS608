"""
collisions: puck-vs-paddle collision handling.
"""

MAX_PUCK_SPEED = 14.0


def handle_paddle_collision(puck, paddle, bounds=None):
    """
    If the puck overlaps the paddle, push it out and reflect it about the
    contact normal (relative to the paddle's own velocity, so a moving
    paddle "hits" the puck). Returns True if a collision was handled.

    bounds = (min_x, max_x, min_y, max_y) is the area the puck's centre may
    occupy. If pushing the puck straight out would put it inside a wall
    (paddle pinning it against a wall/corner), the puck is slid along the
    wall instead so it can never stay stuck inside the paddle.
    """
    dx = puck.x - paddle.x
    dy = puck.y - paddle.y
    distance = (dx ** 2 + dy ** 2) ** 0.5
    min_dist = puck.radius + paddle.radius

    if distance >= min_dist:
        return False

    # Contact normal (paddle centre -> puck centre).
    if distance > 1e-9:
        nx, ny = dx / distance, dy / distance
    else:
        # Perfectly concentric: fall back to opposite of puck motion.
        speed = (puck.vx ** 2 + puck.vy ** 2) ** 0.5
        if speed > 1e-9:
            nx, ny = -puck.vx / speed, -puck.vy / speed
        else:
            nx, ny = 1.0, 0.0

    # 1) Resolve penetration so the puck can never stay inside the paddle.
    old_x, old_y = puck.x, puck.y
    new_x = paddle.x + nx * min_dist
    new_y = paddle.y + ny * min_dist
    if bounds is not None:
        new_x, new_y = _fit_in_bounds(new_x, new_y, old_x, old_y, paddle, min_dist, bounds)
    puck.x, puck.y = new_x, new_y
    # Recompute the normal from the final position (it may have slid).
    nx, ny = (puck.x - paddle.x) / min_dist, (puck.y - paddle.y) / min_dist

    # 2) Reflect the velocity relative to the paddle, only if approaching.
    pvx = getattr(paddle, "vx", 0.0)
    pvy = getattr(paddle, "vy", 0.0)
    rvx, rvy = puck.vx - pvx, puck.vy - pvy
    vn = rvx * nx + rvy * ny
    if vn < 0:
        rvx -= 2 * vn * nx
        rvy -= 2 * vn * ny
        puck.vx, puck.vy = rvx + pvx, rvy + pvy

    # 3) Cap speed so fast hits can't tunnel through things next frame.
    speed = (puck.vx ** 2 + puck.vy ** 2) ** 0.5
    if speed > MAX_PUCK_SPEED:
        scale = MAX_PUCK_SPEED / speed
        puck.vx *= scale
        puck.vy *= scale

    return True


def _fit_in_bounds(x, y, old_x, old_y, paddle, min_dist, bounds):
    """If (x, y) is outside bounds, return the nearest in-bounds spot that is
    still exactly min_dist from the paddle (found by sliding along walls)."""
    lo_x, hi_x, lo_y, hi_y = bounds
    eps = 1e-6
    if lo_x <= x <= hi_x and lo_y <= y <= hi_y:
        return x, y

    candidates = []
    for fy in (lo_y, hi_y):
        h2 = min_dist ** 2 - (fy - paddle.y) ** 2
        if h2 >= 0:
            for sign in (-1, 1):
                candidates.append((paddle.x + sign * h2 ** 0.5, fy))
    for fx in (lo_x, hi_x):
        h2 = min_dist ** 2 - (fx - paddle.x) ** 2
        if h2 >= 0:
            for sign in (-1, 1):
                candidates.append((fx, paddle.y + sign * h2 ** 0.5))

    valid = [c for c in candidates
             if lo_x - eps <= c[0] <= hi_x + eps and lo_y - eps <= c[1] <= hi_y + eps]
    if not valid:
        return max(lo_x, min(hi_x, x)), max(lo_y, min(hi_y, y))
    return min(valid, key=lambda c: (c[0] - old_x) ** 2 + (c[1] - old_y) ** 2)
