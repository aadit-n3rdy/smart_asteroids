# Smart Asteroids — User Guide

## Objective
Smart Asteroids is an arcade-style space shooter where the goal is to
survive as long as possible by avoiding and destroying asteroids.

Smart Asteroids is designed to explore intelligent gameplay mechanics,
with code supporting both direct player control and algorithmic
decision-making.

---

## Controls

### Aiming
- The ship automatically rotates to face the mouse cursor.

### Movement
- **Left Mouse Button (Hold)** — Accelerate the ship toward the mouse pointer.

### Combat
- **Right Mouse Button (Hold)** — Fire bullets in the direction the ship is facing.
  - The firing rate is limited by a short cooldown.

---

## Main Menu Controls
- **Mouse Cursor** — Navigate the menu.
- **Left Mouse Button (Click)**:
  - **PLAY** — Start the game.
  - **QUIT** — Exit the game.

---

## Pause Menu Controls

### Opening the Pause Menu
- **ESC** — Open the pause menu during gameplay.

### Navigation
- **Mouse Cursor** — Navigate the pause menu.
- **Left Mouse Button (Click)**:
  - **RESUME** — Resume gameplay.
  - **QUIT** — Exit the game.
  - **EXIT TO MENU** — Return to the main menu.

---

## Game Over Screen Controls
- **Mouse Cursor** — Navigate the game over menu.
- **Left Mouse Button (Click)**:
  - **RESTART** — Start a new game.
  - **EXIT TO MENU** — Return to the main menu.

---

## Gameplay Overview
- The player controls a spaceship in open space.
- Asteroids continuously spawn and move across the screen.
- Shooting an asteroid destroys it.
- Asteroids can also be destroyed by colliding with each other.
- If the player's ship collides with an asteroid, the ship is destroyed and the game ends.
- The game transitions to an end screen after the ship is destroyed.
- The player earns **1 point for each asteroid destroyed**.

---

## Intelligent Design
The project includes code related to algorithmic and AI-based decision-making,
reflecting its experimental and educational goals. These systems are not
currently exposed as a selectable gameplay mode.

---

## Tips
- Keep moving to avoid collisions.
- Rotate smoothly instead of making sharp turns.
- Aim slightly ahead of moving asteroids.

---

## Customization
This user guide is written in Markdown to make it easy to update
and extend as new features are added.
