# Ludo Board Game

## Video Demo

URL HERE

## Description

This project is a complete implementation of the classic Ludo board game in Python, featuring both terminal-based and automated gameplay modes. The game supports 2-4 players and includes a comprehensive object-oriented design with full test coverage, type annotations, and modern Python development practices.

## Project Overview

Ludo is a strategy board game for two to four players, in which the players race their four tokens from start to finish according to dice rolls. This implementation recreates the traditional game experience in a terminal environment with colorful emoji-based graphics and interactive gameplay.

The project demonstrates advanced Python programming concepts including object-oriented design, abstract base classes, event-driven architecture, comprehensive testing, and type safety. It serves as an excellent example of how to structure a complex game application with clean, maintainable code.

## File Structure and Components

### Core Game Files (`ludo_board_game/` package)

**`game.py`** - The heart of the application containing the `Game` class that manages the entire game state, turn logic, and game flow. This class coordinates between players, handles dice rolls, validates moves, and determines win conditions. It implements the main game loop and ensures proper rule enforcement throughout gameplay.

**`player.py`** - Defines the `Player` class representing each game participant. Each player has a unique color, manages four pawns, and tracks their progress toward victory. The class includes methods for checking win conditions and managing player state transitions.

**`pawn.py`** - Contains the `Pawn` class representing individual game pieces. Each pawn tracks its position on the board, knows its movement rules, and can determine valid moves. The class encapsulates the complex movement logic including starting positions, safe zones, and finishing mechanics.

**`dice.py`** - Implements the `Dice` class providing randomized dice rolls with special game rules. Includes logic for consecutive sixes, turn voiding, and other Ludo-specific dice mechanics that affect gameplay flow.

**`color.py`** - Defines the `Color` enum representing the four player colors (Red, Blue, Green, Yellow) used throughout the game for player identification and board visualization.

**`event.py`** - Contains event classes using Python's dataclass decorator to represent different game events such as pawn movements, kills, wins, and turn changes. This event-driven design allows for clean separation of game logic and user interface concerns.

**`ludo_board.py`** - Implements the `LudoBoard` class responsible for rendering the game board using emoji characters. Creates an attractive visual representation of the 15x15 Ludo board with colored regions for each player and special squares marked.

**`ludo_ui.py`** - Defines the abstract `LudoUI` base class that establishes the interface contract for different user interaction modes. This abstraction enables multiple UI implementations while maintaining consistent game logic.

### Main Application Files

**`project.py`** - The main application entry point containing two UI implementations: `LudoTerminalUI` for interactive human gameplay and `DummyTestUI` for automated testing. The terminal UI provides a rich interactive experience with colored output, player prompts, and game state visualization. The file also includes utility functions for board printing and user input validation.

**`test_project.py`** - Comprehensive unit tests for the main application functions using Python's unittest framework with mocking. Tests cover user input validation, board rendering, and pawn position display functionality, ensuring reliability and correctness.

### Configuration and Requirements

**`requirements.txt`** - Specifies all project dependencies including development tools (black, mypy, pylint), testing frameworks (pytest, coverage), and the inflect library for number-to-word conversion. Maintains version constraints for reproducible builds.

**`mypy.ini`** - Configuration file for MyPy static type checker, ensuring type safety throughout the codebase and catching potential runtime errors during development.

## Design Decisions and Architecture

The project employs several key design patterns and architectural decisions:

**Object-Oriented Design**: Each game concept is represented by a dedicated class with clear responsibilities. This approach makes the code modular, testable, and easy to understand.

**Event-Driven Architecture**: Game events are represented as data classes, allowing for clean separation between game logic and presentation. This design makes it easy to add new UI implementations or game features.

**Abstract Base Classes**: The `LudoUI` abstract class enables multiple interface implementations. Currently, there's an interactive terminal UI and an automated testing UI, but this design allows for easy addition of graphical or web-based interfaces.

**Type Safety**: Comprehensive type annotations throughout the codebase catch errors early and improve code documentation. The project uses modern Python type hints including union types and generic collections.

**Comprehensive Testing**: Unit tests cover critical functionality with mocking to isolate components. This ensures reliability and makes refactoring safer.

**Modular Package Structure**: The core game logic is separated into a package, while the main application provides the user interface. This separation allows the game engine to be reused in different contexts.

The choice to use emoji characters for the board representation provides an engaging visual experience while maintaining compatibility with any terminal that supports Unicode. The color-coded output enhances usability and makes game state immediately apparent to players.



## How to Run

The game can be run in two different modes:

### Interactive Terminal Mode (LudoTerminalUI)

To start an interactive game with human players, run:

```bash
python project.py
```

This mode provides a full interactive experience where:

- Players manually roll dice by pressing Enter
- Players choose which pawns to move and which dice values to use
- The game displays a colorful board representation after each move
- Players input the number of participants (2-4 players)
- Rich terminal output with colored messages and board visualization

### Automated Demo Mode (DummyTestUI)

The game also includes an automated demo mode that runs without user input:

```python
# In project.py, the DummyTestUI class automatically:
# - Rolls dice without user interaction
# - Makes optimal moves automatically
# - Provides a fast demonstration of gameplay
# - In project.py instead of giving LudoTerminalUI as argument to game, give DummyTestUI
```


This mode is primarily used for testing and demonstration purposes, allowing you to see a complete game played automatically with accelerated speed.

### Running Tests

To run the test suite:

```bash
python -m pytest test_project.py -v
```

The game supports 2-4 players and provides an engaging terminal-based Ludo experience with full rule implementation and colorful visual feedback.
