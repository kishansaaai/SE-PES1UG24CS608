# Air Hockey Lab

This project is a single-topic Air Hockey game using **Pygame**. It
introduces students to angle-based collision physics, scoring,
round timing, and post-goal state reset, using a small, readable
object-oriented codebase.

---

## What's Provided

A working Air Hockey game with:

- A player paddle (blue, left side) moved with the arrow keys, and a
  computer-controlled paddle on the right
- A puck that bounces off the top and bottom walls and off both
  paddles
- Goals at the center of each end wall

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Arrow keys move your paddle (blue, left side) within
your own half of the table. Press R at any time to restart.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix puck–paddle collision

> The puck does not consistently respond correctly when it collides
> with a paddle, particularly at higher speeds or when it approaches
> at an angle. Fix the collision logic so the puck reliably rebounds
> from the paddles at different speeds and angles without passing
> through or getting stuck inside them.

### Task 2: Implement match scoring

> Add a scoring system where a player earns a point when the puck
> enters the opponent's goal. Display both players' scores during
> play, and determine the winner based on the final score.

### Task 3: Implement a 30-second match timer

> Add a 30-second countdown timer to the match. Display the remaining
> time during gameplay. When the timer reaches zero, stop the match
> and determine the result based on the scores. If both scores are
> equal, display a draw.

### Task 4: Implement puck reset after scoring

> After a goal is scored, reset the puck to the center of the table
> and prepare it for the next point. Make sure the puck's velocity,
> direction, and any other relevant state are correctly reset so each
> new point starts cleanly.

---

## Expected Behavior

- The puck bounces realistically off walls and paddles at any angle,
  and never gets stuck vibrating inside a paddle.
- A point is scored only when the puck fully passes through the goal
  gap - hitting the wall elsewhere bounces the puck back normally.
- After every goal, the puck immediately continues play from the
  center - it should never sit motionless.
- The match runs for exactly 30 seconds. When time runs out, the
  match ends and shows the correct winner - or "Draw" if the score is
  tied.

---

## Folder Structure

```
air-hockey/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── puck.py
│   ├── paddle.py
│   ├── collisions.py
│   ├── ai.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
