# Lab 4: Vibe Coding - Air Hockey

**Student:** SAI KISHAN A

**SRN:** PES1UG24CS608

Original starter: [SETAPESU26/02_air_hockey](https://github.com/SETAPESU26/02_air_hockey).

## Submission files

- [Before video](before.mp4): 10 seconds of the original game, without audio.
- [After video](after.mp4): 10 seconds of corrected gameplay, including scoring, the countdown, and the final result, without audio.
- [AI chat history](chat-history.pdf): the supplied PDF export of the AI conversation.
- [Updated game code](air-hockey/).

## Completed tasks

| Task | Result |
| --- | --- |
| 1. Puck-paddle collision | Reflects using the contact direction, resolves overlap, and uses small movement steps to handle fast shots. |
| 2. Match scoring | Displays both scores and awards a point after the puck passes the goal line through the goal gap. |
| 3. Match timer | Displays a 30-second countdown, stops play at zero, and shows the winner or a draw. |
| 4. Reset after a goal | Returns the puck to the center and immediately serves it for the next point. |

Each coding task has its own commit, following a separate starter-code commit. The recordings and chat export are included in a submission commit.

## Run the game

Requires Python 3.10 or later. From the repository root:

```sh
cd Lab-4/air-hockey
python -m pip install -r requirements.txt
python main.py
```

Use the arrow keys to move the blue paddle on the left. Press **R** to restart the match. Close the game window to exit.
