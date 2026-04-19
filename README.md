# Space Defender

A 2D space shooter built with Python and Pygame. Enemies spawn from multiple directions, rocks must be avoided, and a boss fight triggers every three levels.

## About me
- I started learning Python in December 2025 and this is my first larger project I independently developed from start to finish. My original vision included 3D elements, but realizing that requires deeper knowledge I'm still working towards.
---

## Gameplay

- Control a ship on the screen and shoot down incoming enemies
- Enemies and rocks spawn from the top, left, and right
- Rocks cannot be destroyed, must be avoided
- Every 3rd level a Boss appears: it descends from the top, moves horizontally, and fires projectiles aimed for the ships postion
- Boss HP scales with the level
- Getting hit triggers a 2-second invincibility period (ship blinks)
- 3 lives total, the game ends when all are lost

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move ship (4 directions) |
| Space | Fire |
| ESC | Pause / close highscore screen |
| P | Quit to main menu |
| Q | Quit game |

## Features

- Procedural enemy spawning with configurable wave size and spawn interval
- Speed scaling per level (`sdeedup_scale` factor applied to ship, bullets, and aliens)
- Persistent highscore and best level saved to `highscore.json`
- Background music with in-game toggle 
- All objects drawn with Pygame primitives 

## Project Structure

```
space_defender/
├── space_defender.py   # Main game loop & event handling
├── settings.py         # All configurable constants + dynamic scaling
├── ship.py             # Player ship (movement, invincibility, drawing)
├── fleet.py            # Wave management, spawning, collision detection
├── obstacle.py         # Enemy and Rock sprite classes
├── boss.py             # Boss + BossBullet logic
├── ammunition.py       # Bullet firing, updating, collision with aliens
├── bullets.py          # Player bullet sprite
├── scoreboard.py       # Score, level, lives display + JSON persistence
├── hud.py              # Pause screen and highscore overlay
├── menu.py             # Main menu with interactive buttons
├── game_state.py       # Session stats (score, level, lives)
├── key_events.py       # Keyboard input handling
├── highscore.json      # Persistent save data
├── images/             # Background and menu screen assets
└── sounds/             # Music and laser sound
```

## Installation

```bash
pip install pygame
cd pip install -r
requirements.txt
```

Requires Python 3.10+ and Pygame 2.x.
