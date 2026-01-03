# Smart Asteroids - Project Structure

```
smart_asteroids/
│
├── main.py                    # 🚀 Entry point - Initializes pygame and manages game states
├── README.txt                 # 📖 Project documentation
├── .gitignore                 # Git ignore rules
│
├── src/                       # 📦 Source code package
│   ├── __init__.py           # Package initialization
│   │
│   ├── entities/             # 🎮 Game Entities Module
│   │   ├── __init__.py       # Exports: rocket, asteroid, bullet, ROCKET_STATUS, ASTEROID_STATUS
│   │   ├── rocket.py         # Player-controlled rocket class
│   │   ├── asteroid.py       # AI-controlled asteroid class with neural network
│   │   └── bullet.py         # Bullet projectile class
│   │
│   ├── ai/                   # 🤖 Artificial Intelligence Module
│   │   ├── __init__.py       # Exports: neural_network
│   │   └── neural_network.py # Neural network implementation for asteroid AI
│   │
│   ├── ui/                   # 🖥️  User Interface Module
│   │   ├── __init__.py       # Exports: main_menu
│   │   └── main_menu.py      # Main menu UI implementation
│   │
│   └── core/                 # ⚙️  Core Game Logic Module
│       ├── __init__.py       # Exports: GAME_STATES, constants, game
│       ├── constants.py      # Game constants and configuration
│       ├── game_states.py    # Game state enumeration
│       └── game.py           # Main game loop, pause menu, game over menu
│
└── assets/                   # 🎨 Game Assets
    ├── images/               # Image assets
    │   ├── asteroid.png      # Asteroid sprite
    │   └── rocket2.png       # Rocket sprite
    │
    ├── fonts/                # Font assets
    │   └── ARCADECLASSIC.TTF # Arcade Classic font
    │
    └── themes/               # UI Theme files (pygame-gui)
        ├── main_menu_theme.json
        ├── pause_menu_theme.json
        └── game_over_theme.json
```

## Module Dependencies

```
main.py
  └── src.core (GAME_STATES, constants, game)
  └── src.ui (main_menu)

src.core.game
  └── src.core (constants, game_states)
  └── src.entities (rocket, asteroid)

src.entities.rocket
  └── src.core.constants
  └── src.entities.bullet

src.entities.asteroid
  └── src.ai.neural_network
  └── src.entities.rocket
  └── src.core.constants
  └── src.entities.bullet

src.entities.bullet
  └── src.core.constants

src.ui.main_menu
  └── src.core (constants, game_states)
```

## Module Responsibilities

### `src.entities/`
- **rocket.py**: Player-controlled spaceship with mouse-based movement and shooting
- **asteroid.py**: AI-controlled asteroids with neural network for intelligent movement
- **bullet.py**: Projectiles fired by the rocket

### `src.ai/`
- **neural_network.py**: Neural network implementation used by asteroids for AI behavior

### `src.ui/`
- **main_menu.py**: Main menu screen with play/quit options

### `src.core/`
- **constants.py**: Game configuration (window size, speeds, etc.) and asset path helper
- **game_states.py**: Enumeration of game states (MAIN_MENU, IN_GAME, QUIT)
- **game.py**: Main game loop, pause menu, and game over screen

### `assets/`
- **images/**: Sprite images for game entities
- **fonts/**: Font files for UI text
- **themes/**: JSON theme files for pygame-gui styling

## Import Examples

```python
# From main.py
from src.core.game_states import GAME_STATES
from src.ui import main_menu
from src.core import game, constants

# From game.py
from src.entities import rocket, asteroid
from src.core import constants, GAME_STATES

# From entities
from src.core.constants import window_width, get_asset_path
from src.entities import bullet
from src.ai.neural_network import neural_network
```

