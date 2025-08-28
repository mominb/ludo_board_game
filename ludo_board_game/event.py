from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ludo_board_game.game import Game
    from ludo_board_game.pawn import Pawn
    from ludo_board_game.player import Player


class Event:
    pass


@dataclass
class GameEnded(Event):
    game: Game


@dataclass
class PawnKilled(Event):
    player: Player
    pawn: Pawn


@dataclass
class PlayerWon(Event):
    player: Player


@dataclass
class PawnMoved(Event):
    pawn: Pawn


@dataclass
class PawnOpened(Event):
    pawn: Pawn


@dataclass
class PawnFinished(Event):
    pawn: Pawn


@dataclass
class TurnSkipped(Event):
    player: Player


@dataclass
class InvalidMoveOptionSelected(Event):
    pass
