from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .player import Player


class Pawn:
    # Class constants defining the Ludo board layout
    MAX_STEPS_TO_HOME: int = 57  # Total steps from start to finish
    MAX_STEPS_ON_BOARD: int = MAX_STEPS_TO_HOME - 6  # Steps on main board (51)

    def __init__(self, player: Player) -> None:
        # Each player's pawns are numbered 1-4
        self.number: int = len(player.pawns) + 1
        self.owner: Player = player  # Reference to the player who owns this pawn
        self.position: int = 0  # Start at home (position 0)

    def __str__(self) -> str:
        return (
            f"Pawn # {self.number} owned by {self.owner} has position {self.position}"
        )

    def is_locked(self) -> bool:
        return self.position == 0

    def is_unlocked(self) -> bool:
        return self.position >= 1

    def has_finished(self) -> bool:
        return self.position >= Pawn.MAX_STEPS_TO_HOME

    def is_enroute(self) -> bool:
        return self.is_unlocked() and not self.has_finished()

    def on_final_lane(self) -> bool:
        return (
            self.is_unlocked()
            and self.position > Pawn.MAX_STEPS_ON_BOARD
            and self.position < 57
        )

    def is_valid_move_with_steps(self, steps: int) -> bool:
        if self.is_locked():
            return steps == 6
        elif self.has_finished():
            return False
        else:
            return self.position + steps <= 57

    def board_absolute_position(self) -> int:
        if self.is_enroute():
            # Each player's starting position is offset by 13 spaces
            player_offset = (self.owner.number - 1) * 13
            # Calculate absolute position with wraparound
            absolute_position = ((player_offset + self.position - 1) % 52) + 1
            return absolute_position

        return 0  # Not on main board (at home or on colored path)

    def start(self) -> None:
        self.position = 1
