
# Crossy Road Clone (Python/Pygame)

A faithful clone of Crossy Road featuring infinite procedural generation, precise collision mechanics, and smooth interpolations.

## Architecture

The project is structured into modular components:

- **Core**:
  - `main.py`: Entry point.
  - `game.py`: Main game loop and state management (Menu, Playing, GameOver).
  - `config.py`: Centralized constants (screen size, colors, speeds).

- **World Generation**:
  - `world_generator.py`: Manages the infinite scrolling and lane creation.
  - `lane.py`: Logic for different lane types (Road, River, Rail, Grass) and spawning entities.

- **Entities**:
  - `player.py`: Handles discrete grid movement with smooth visual hopping interpolation.
  - `entity.py`: Base class for all world objects.
  - `vehicles.py`: Dynamic obstacles (Cars, Trains).
  - `environment.py`: Static (Trees) and semi-dynamic (Logs) obstacles.

- **Systems**:
  - `collision_manager.py`: Handles complex interactions (death conditions, log riding, blocking).
  - `camera.py`: Smooth following camera logic.
  - `input_manager.py`: Abstraction for keyboard input.
  - `asset_manager.py`: Procedurally generates "voxel-style" sprites using Pygame drawing primitives.
  - `ui.py`: Handles score and game-over rendering.

## How to Run

1.  Ensure Python and Pygame are installed:
    ```bash
    pip install pygame
    ```
2.  Run the game:
    ```bash
    python main.py
    ```

## Controls

- **Arrow Keys** or **WASD**: Move (Up, Down, Left, Right)
- **Enter/Space**: Confirm / Restart
- **Esc**: Quit
