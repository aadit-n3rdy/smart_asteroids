# Smart Asteroids 🚀

A modern twist on the classic Asteroids game where the enemies (asteroids) use a **Genetic Algorithm** to learn and adapt to your playstyle.

## 🧬 Evolutionary AI Framework
This project features a modular evolutionary framework, allowing for plug-and-play AI strategies. The asteroids are controlled by neural networks that evolve over generations.

### Available Strategies
- **Crossover (Sexual Reproduction):** Offspring inherit traits from the two best-performing parents. This allows for faster convergence and the emergence of "Super Asteroids" that combine speed and maneuverability.
- **Tournament Selection:** Pick random groups of asteroids and let them compete. The winner passes on its genes, ensuring behavioral diversity and preventing the AI from becoming too predictable.

## ⚙️ How to Configure
You can swap between evolution strategies by changing a single constant in `src/utils/constants.py`:

```python
# Change this to "crossover" or "tournament"
EVOLUTION_STRATEGY = "crossover"
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- `pygame-ce`
- `numpy`
- `pygame-gui`

### Installation
1. Install dependencies:
   ```bash
   pip install pygame-ce numpy pygame-gui
   ```

2. Run the game:
   ```bash
   python main.py
   ```

## 🎮 Controls
- **Aim:** Move your mouse (the rocket points toward the cursor).
- **Thrust:** Hold **Left Mouse Button (LMB)** to accelerate.
- **Shoot:** Press **Right Mouse Button (RMB)** to fire bullets.
- **Pause:** Press **ESC**.

## 🛠️ Project Structure
- `src/core/`: Game state management and main loop.
- `src/entities/`: Rocket, Asteroid, and Bullet logic.
- `src/evolution/`: All pluggable AI strategies and the factory.
- `src/utils/`: Neural network math and game constants.
- `assets/`: Game images, fonts, and UI themes.
