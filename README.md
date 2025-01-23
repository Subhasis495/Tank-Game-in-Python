# Tank Game

A simple two-player tank battle game built using Python and Pygame. Players control tanks, move across the terrain, and aim to destroy the opponent's tank by shooting bullets. The game features animations, sound effects, obstacles, and explosions for an engaging gameplay experience.

## Features

- **Two-Player Local Gameplay:** Control two tanks with separate keyboard controls.
- **Realistic Physics:** Includes bullet gravity, barrel rotation, and collision detection.
- **Health System:** Tanks have health bars, and bullets reduce health upon collision.
- **Obstacles:** Static obstacles block tank movement and bullet paths.
- **Sound Effects:** Includes sound effects for firing, tank movement, and game-over events.
- **Explosions:** Animated explosions occur when bullets hit tanks or obstacles.

## Controls

### Player 1 (Red Tank):
- **Move Left:** `A`
- **Move Right:** `D`
- **Rotate Barrel Up:** `W`
- **Rotate Barrel Down:** `S`
- **Shoot:** `SPACE`

### Player 2 (Blue Tank):
- **Move Left:** `Left Arrow`
- **Move Right:** `Right Arrow`
- **Rotate Barrel Up:** `Up Arrow`
- **Rotate Barrel Down:** `Down Arrow`
- **Shoot:** `Enter`

## How to Run

1. **Install Pygame:** Ensure you have Python installed on your system. Install Pygame using pip:
   ```
   pip install pygame
   ```

2. **Add Required Assets:**
   Ensure the following files are present in the same directory as the script:
   - `background.jpg` (background image for the game)
   - `game over.mp3` (sound effect for game over)
   - `tank movement.mp3` (sound effect for tank movement)
   - `firing.mp3` (sound effect for shooting)

3. **Run the Game:**
   Execute the Python script:
   ```bash
   python tank_game.py
   ```

## Future Enhancements

- Add AI-controlled tanks for single-player mode.
- Introduce power-ups like health restoration, shields, or speed boosts.
- Add more diverse terrain and obstacles.
- Implement online multiplayer functionality.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

## Acknowledgements

- Developed using [Pygame](https://www.pygame.org/).
- Special thanks to all contributors and testers.

Enjoy the game! Feel free to contribute and share your feedback!
