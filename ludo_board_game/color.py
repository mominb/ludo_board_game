from enum import Enum


class Color(Enum):
    RED = 1  # Player 1's color
    BLUE = 2  # Player 2's color
    GREEN = 3  # Player 3's color
    YELLOW = 4  # Player 4's color

    def __str__(self) -> str:
        return self.name.lower()
