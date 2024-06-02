# Kaooa: Traditional Abstract Strategy Hunt Game from India

Kaooa, also known as "Vulture and Crows," is a captivating traditional hunt game from India. Like "Len Choa" ("Tiger and Leopards") and "Fox and Geese," it features a dynamic where one player controls a single token against multiple tokens controlled by the opponent, mimicking the thrill of a predator-prey scenario.

[REFRENCE](https://www.whatdowedoallday.com/kaooa/)
## Game Overview

The game is played on a unique pentagram or star-shaped board, adding a touch of aesthetic charm. One player controls the "vulture" token, while the other player controls seven "crow" tokens. The objective for the crows is to surround and blockade the vulture, preventing it from moving, while the vulture aims to capture four crows by jumping over them.

## How to Play

### Materials Needed

- Five-pointed star game board (you can use the provided printable or draw your own)
- One token representing the vulture
- Seven tokens in a different color representing the crows
- Two enthusiastic players

### Objective

- **Crows**: Surround the vulture and block it from moving.
- **Vulture**: Capture four crows by jumping over them.

### Instructions

1. **Initial Setup**:
  - Player 1 (Crows) places one crow token on any intersection of the game board.
  - Player 2 (Vulture) places the vulture token on any vacant spot.

2. **Legal Moves**:
  - Crows: Move one crow token to an adjacent vacant spot per turn. No jumping is allowed.
  - Vulture: Move to an adjacent vacant spot or jump over a crow in a straight line, capturing it. The vulture must jump if the opportunity presents itself. Only one jump per turn.

3. **Drop Phase**:
  - Player 1 (Crows) continues to drop their remaining six crow tokens, one by one, onto vacant spots.
  - Once all seven crows are placed, they can start moving on subsequent turns.

4. **Alternating Turns**:
  - Players alternate turns, with the vulture moving and jumping, and the crows moving or placing new tokens (during the drop phase).

5. **Winning**:
  - The vulture wins if it captures at least four crows.
  - The crows win if they manage to trap the vulture, preventing it from making a legal move.

## Notes

- To avoid draws due to repetitive moves, you can introduce a rule against repeating the same move or declare a draw and start a new game.
- If the vulture captures three crows early, the game may become challenging for the crows, but it is still technically possible for them to block the vulture.
- Encourage players to analyze strategies, such as the advantages of being the crows or the vulture, the impact of starting positions, and the likelihood of winning with perfect play.

Kaooa offers an engaging blend of abstract strategy and imaginative storytelling, providing an enjoyable experience for players of all ages. Dive into this traditional Indian game and immerse yourself in the thrilling hunt between the vulture and the crows!


## Implementation

The game is implemented using the Pygame library, which provides a set of Python modules designed for writing video games. The main components of the implementation are:

1. **Game Board**: The pentagram-shaped game board is created by drawing lines and circles on the Pygame window, representing the intersections and vertices of the board.

2. **Game Pieces**: The crow and vulture tokens are represented as colored circles on the game board. The crows are represented as cyan circles, and the vulture is represented as a pink circle.

3. **Player Classes**:
   - `CrowPlayer` class: Handles the placement and movement of crow tokens on the board.
   - `VulturePlayer` class: Handles the placement and movement of the vulture token on the board.

4. **Game Logic**:
   - The game logic is implemented in the `main` function, which handles the game loop, player turns, and win/lose conditions.
   - Various helper functions are used to determine legal moves, highlight available moves, and detect if the vulture is blocked by crows.

5. **User Input**: The game accepts user input through mouse clicks. Players can place their tokens and move them by clicking on the desired positions on the game board.

6. **Win/Lose Conditions**:
   - The crows win if they manage to trap the vulture, preventing it from making a legal move.
   - The vulture wins if it captures at least four crows by jumping over them.

## How to Run

To run the game, make sure you have Python and Pygame installed on your system. Then, navigate to the project directory and execute the following command:
This will launch the game window, and you can start playing by following the on-screen instructions.

## Customization

You can customize the game by modifying the code in the `main.py` file. For example, you can change the colors of the tokens, adjust the size of the game board, or introduce new game rules.

## Contributing

Contributions to this project are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.