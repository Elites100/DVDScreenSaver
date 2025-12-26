DVD Bouncing Screensaver (Python Version)
A nostalgic recreation of the classic bouncing DVD logo screensaver built using Python and Pygame. This version includes a dynamic color-changing feature and a musical reward for hitting the elusive "perfect corner."

Features
Dynamic Color Shifts: The logo changes to a random color every time it bounces off a boundary.

Corner Hit Celebration: Plays a specific song or sound effect when the logo hits a perfect corner.

Collision Logic: Uses simple physics to calculate trajectory and wall collisions.

Customizable: Easily change the logo image, movement speed, and audio files.

Prerequisites
Before running this project, ensure you have Python installed and the Pygame library:

Bash

pip install pygame
How it Works
Movement: The logo's position is updated each frame by adding a velocity vector [vx, vy].

Boundary Detection: If the logo's rect hits the edge of the window, the corresponding velocity is inverted (e.g., vx *= -1).

Corner Detection: A "perfect corner" is detected when both the horizontal and vertical boundaries are triggered in the same frame.

Color Change: A new random RGB tuple is applied to the logo surface using Pygame's BLEND_RGB_ADD or by loading a pre-colored sprite.

Controls
ESC: Exit the screensaver.
