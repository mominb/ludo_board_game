from functools import reduce
from typing import List

from ludo_board_game.event import (
    GameEnded,
    InvalidMoveOptionSelected,
    PawnFinished,
    PawnKilled,
    PawnMoved,
    PawnOpened,
    PlayerWon,
    TurnSkipped,
)
from ludo_board_game.pawn import Pawn

from .dice import Dice
from .ludo_ui import LudoUI
from .player import Player


class Game:
    # Safe positions on the board where pawns cannot be captured
    # These are strategically placed around the board
    SAFE_POSITIONS: List[int] = [1, 9, 14, 22, 27, 35, 40, 48]

    def __init__(self, playerCount: int, ludoUI: LudoUI) -> None:
        self.ui: LudoUI = ludoUI
        # Create all players for the game
        self.players: List[Player] = []
        self.number_of_players: int = playerCount
        for _ in range(playerCount):
            self.players.append(Player())

        # Set the first player as active (Red player traditionally starts)
        self.active_player: Player = self.players[0]

        # Create dice instance for this game
        self.dice: Dice = Dice()

    def non_active_players(self) -> List[Player]:
        return list(
            filter(lambda p: p.number != self.active_player.number, self.players)
        )

    def find_non_active_pawns_at(self, board_position: int) -> List[Pawn]:
        return reduce(
            lambda list, player: list + player.pawns_at(board_position),
            self.non_active_players(),
            [],
        )

    def kill_pawns(self, landing_position: int) -> None:
        if landing_position > 0 and landing_position not in Game.SAFE_POSITIONS:
            pawns_to_kill = self.find_non_active_pawns_at(landing_position)

            for pawn in pawns_to_kill:
                pawn.position = 0
                self.ui.event_triggered(PawnKilled(pawn.owner, pawn))

    def apply_move_to_pawn(self, pawn: Pawn, steps: int) -> None:
        if not self.dice.is_value_in_unused_results(steps):
            raise ValueError(f"The number {steps} is not available to use")

        elif pawn.is_locked():
            if steps != 6:
                self.ui.event_triggered(InvalidMoveOptionSelected())
                raise ValueError("Cannot open pawn with values other than 6")
            else:
                self.open_pawn(pawn)

        elif pawn.has_finished():
            raise ValueError("Pawn already finished")

        elif not pawn.is_valid_move_with_steps(steps):
            raise ValueError("The number of steps is too large to use for this pawn.")

        else:
            pawn.position += steps
            self.dice.mark_first_matching_result_as_used(steps)
            if pawn.has_finished():
                self.ui.event_triggered(PawnFinished(pawn))
            else:
                self.ui.event_triggered(PawnMoved(pawn))

            self.kill_pawns(pawn.board_absolute_position())

    def open_pawn(self, pawn: Pawn) -> None:
        if not self.dice.is_value_in_unused_results(6):
            raise ValueError("No unused 6 available to open pawn")

        if pawn.is_unlocked():
            raise ValueError("Pawn is already opened")

        pawn.start()

        self.dice.mark_first_matching_result_as_used(6)
        self.ui.event_triggered(PawnOpened(pawn))

    def turn_completed(self) -> bool:
        if not self.dice.can_roll() and self.dice.has_used_all_results():
            return True
        else:
            return False

    def active_player_index(self) -> int:
        for index, player in enumerate(self.players):
            if player.number == self.active_player.number:
                return index
        return 0  # Default to first player if not found

    def change_turn(self) -> None:
        current_player_index = self.active_player_index()
        next_player: Player | None = None

        while not next_player or next_player.has_won():
            next_index = (current_player_index + 1) % self.number_of_players
            next_player = self.players[next_index]
            current_player_index = current_player_index + 1

        self.active_player = next_player
        self.dice.reset()

    def roll_dice(self) -> None:
        # Keep rolling while allowed and not voided
        while self.dice.can_roll() and not self.dice.voided():
            self.ui.prompt_and_roll_dice(self.active_player, self.dice)

    def _players_left(self) -> List[Player]:
        return list(filter(lambda p: not p.has_won(), self.players))

    def _has_game_ended(self) -> bool:
        return len(self._players_left()) <= 1

    def get_available_moves(self) -> List[int]:
        return [result.result for result in self.dice.roll_results if not result.used]

    def is_dice_result_applicable(self, pawns: List[Pawn], moves: List[int]) -> bool:
        for move in moves:
            for pawn in pawns:
                if pawn.is_valid_move_with_steps(move):
                    return True

        return False

    def start(self) -> None:
        position = 1
        while not self._has_game_ended():
            # Rendering state
            self.ui.render_state(self)
            self.roll_dice()

            if self.dice.voided() or (
                not self.dice.can_open_pawn()
                and len(self.active_player.locked_pawns()) == 4
            ):
                self.ui.event_triggered(TurnSkipped(self.active_player))
                self.change_turn()

            else:
                while not self.dice.has_used_all_results():
                    try:
                        pawns = self.active_player.enroute_pawns()
                        moves = self.get_available_moves()

                        if self.dice.can_open_pawn():
                            pawns = self.active_player.locked_pawns() + pawns

                        if self.is_dice_result_applicable(pawns, moves):
                            (pawn, steps) = self.ui.ask_move(
                                pawns,
                                self.get_available_moves(),
                            )

                            self.apply_move_to_pawn(pawn, steps)

                        else:
                            if not self.active_player.has_won():
                                self.ui.event_triggered(TurnSkipped(self.active_player))
                                self.change_turn()
                            break

                    except ValueError:
                        pass

                # Winning Condition
                if self.active_player.has_won():
                    self.active_player.win_position = position
                    position += 1
                    self.ui.event_triggered(PlayerWon(self.active_player))

                # Move on to next players turn
                self.change_turn()

        self.ui.render_state(self)
        self.ui.event_triggered(GameEnded(self))
