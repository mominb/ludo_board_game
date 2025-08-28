from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING, List

from .color import Color
from .dice import Dice

if TYPE_CHECKING:
    from .pawn import Pawn


class Player:
    player_count: int = 0
    colors: List[Color] = [color for color in Color]  # Available colors list
    dice: Dice = Dice()  # Shared dice object

    number: int
    color: Color
    win_position: int | None
    pawns: List[Pawn]

    def __init__(self) -> None:
        # Import here to avoid circular dependency
        from .pawn import Pawn

        # Increment and assign player number
        Player.player_count = self.number = Player.player_count + 1

        # Ludo supports maximum 4 players
        if Player.player_count > 4:
            raise ValueError("Cannot have more than 4 players")

        # Assign color based on player number (index 0-3)
        self.color = Player.colors[self.number - 1]
        self.win_position = None  # Tracks finishing order when player wins

        # Create 4 pawns for this player
        self.pawns = []
        for _ in range(4):
            self.pawns.append(Pawn(self))

    @classmethod
    def reset_player_count(cls) -> None:
        cls.player_count = 0

    def __str__(self) -> str:
        return f"Player # {self.number} having a color of {self.color}"

    def enroute_pawns(self) -> List[Pawn]:
        open_pawns = []
        for pawn in self.pawns:
            if pawn.is_unlocked() and not pawn.has_finished():
                open_pawns.append(pawn)
        return open_pawns

    def locked_pawns(self) -> List[Pawn]:
        closed_pawns = []
        for pawn in self.pawns:
            if pawn.position == 0:
                closed_pawns.append(pawn)
        return closed_pawns

    def pawns_on_final_lane(self) -> List[Pawn]:
        return [pawn for pawn in self.pawns if pawn.on_final_lane()]

    def pawn_absolute_positions(self) -> List[int]:
        return reduce(
            lambda list, pawn: list + [pawn.board_absolute_position()], self.pawns, []
        )

    def pawns_at(self, absolute_position: int) -> List[Pawn]:
        pawns = []

        # Check each pawn's position against the target position
        for my_pawn_index, my_pawn_position in enumerate(
            self.pawn_absolute_positions()
        ):
            if absolute_position == my_pawn_position:
                pawns.append(self.pawns[my_pawn_index])

        return pawns

    def has_won(self) -> bool:
        count = 0
        for pawn in self.pawns:
            if pawn.has_finished():
                count += 1

        return count >= 4
