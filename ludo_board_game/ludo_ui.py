from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Tuple

from .dice import Dice
from .event import Event
from .pawn import Pawn
from .player import Player

if TYPE_CHECKING:
    from .game import Game


class LudoUI(ABC):
    @abstractmethod
    def render_state(self, game: Game) -> None:
        pass

    @abstractmethod
    def event_triggered(self, event: Event) -> None:
        pass

    @abstractmethod
    def prompt_and_roll_dice(self, player: Player, dice: Dice) -> int:
        pass

    @abstractmethod
    def ask_move(self, pawns: List[Pawn], moves: List[int]) -> Tuple[Pawn, int]:
        pass
