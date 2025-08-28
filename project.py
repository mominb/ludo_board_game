from typing import List

import inflect

from ludo_board_game.dice import Dice
from ludo_board_game.event import (
    Event,
    GameEnded,
    InvalidMoveOptionSelected,
    PawnFinished,
    PawnKilled,
    PawnMoved,
    PawnOpened,
    PlayerWon,
    TurnSkipped,
)
from ludo_board_game.game import Game
from ludo_board_game.ludo_board import LudoBoard
from ludo_board_game.ludo_ui import LudoUI
from ludo_board_game.pawn import Pawn
from ludo_board_game.player import Player

# Library for converting numbers to words (e.g., "3" -> "three")
p = inflect.engine()


def main() -> None:
    # Reset player count to ensure clean start
    from ludo_board_game.player import Player

    Player.reset_player_count()
    game = Game(get_num_players(), DummyTestUI())

    input("Press Enter to start game.\n")
    game.start()


def get_num_players() -> int:
    number: int | None = None

    while True:
        number = int(input("How many players? \n").strip())
        if number >= 2 and number <= 4:
            return number
        else:
            print(
                "\033[31mInvalid Input (Number of Players should be between 2-4)\033[0m"
            )


def print_board(game: Game) -> None:
    board = LudoBoard()
    players_pos = {}

    for player in game.players:
        color_str = str(player.color)
        positions: List[int | None] = []
        for pawn in player.pawns:
            if pawn.position == 0:
                positions.append(None)
            elif pawn.position >= 0:
                positions.append(pawn.position - 1)
        players_pos[color_str] = positions

    board.set_pawns(players_pos)
    print(board.render())


def print_pawn_position(pawn: Pawn) -> None:
    if pawn.is_enroute():
        print(f"Pawn # {pawn.number} at position {pawn.position}")
    elif pawn.has_finished():
        print(f"Pawn # {pawn.number} (finished)")
    elif pawn.is_locked():
        print(f"Pawn # {pawn.number} (currently locked)")


class LudoTerminalUI(LudoUI):
    # Prints message according to what event is triggered
    def event_triggered(self, event: Event) -> None:
        match event:
            case PawnKilled(player, pawn):
                print(
                    f"\033[31mPlayer # {player.number} ({player.color})'s pawn {pawn.number} was killed!\033[0m"
                )
            case PlayerWon(player):
                print(
                    f"\033[33m🎉 PLAYER #{player.number} ({player.color}) HAS WON THE GAME! 🎉\033[0m"
                )
            case PawnMoved(pawn):
                print(f"\033[32mPawn is now at position {pawn.position}.\033[0m")
                print()
            case PawnOpened(pawn):
                print("\033[32mPawn opened successfully!\033[0m\n")
            case PawnFinished(pawn):
                print(
                    f"\033[32mPlayer # {pawn.owner.number} ({pawn.owner.color})'s pawn {pawn.number} has finished !\033[0m"
                )
            case TurnSkipped(player):
                print(
                    f"Player # {player.number} ({player.color}) 's turn was skipped as no moves were possible"
                )
                print()
            case InvalidMoveOptionSelected():
                print("\033[31mSelect valid option\033[0m")
            case GameEnded(game):
                print("Final Result:")
                for player in game.players:
                    if player.win_position is None:
                        print(
                            f"    \033[91mPlayer # {player.number} ({player.color}) lost the game\033[0m"
                        )
                    else:
                        print(
                            f"    \033[33mPlayer # {player.number} ({player.color}) won at position {player.win_position} !!!\033[0m"
                        )

    # Gets user input to roll dice and display related messages
    def prompt_and_roll_dice(self, player: Player, dice: Dice) -> int:
        input(f"Player #{player.number} \033[33mpress Enter to roll dice\033[0m\n")
        result = dice.roll()
        print(f"\033[32mYou rolled a {result} !!!\033[0m\n")
        if dice.voided():
            print("\033[31mSorry your turn is voided 😔\033[0m\n\n\n")

        return result

    # Gets user to select a pawn and to apply a move to it
    def ask_move(self, pawns: list[Pawn], moves: list[int]) -> tuple[Pawn, int]:
        move_choice = moves[0]
        total_moves = ", ".join(map(str, moves))
        pawns.sort(key=lambda p: p.number)
        while True:
            print("=" * 40)
            print(
                f"Choose one of following pawns to apply the dice roll of {move_choice} out of ({total_moves}): "
            )
            for pawn in pawns:
                print_pawn_position(pawn)
            print()

            pawn_choice = int(input("Choose a pawn to move."))
            print()
            print("=" * 40)

            selected_pawn = next((p for p in pawns if p.number == pawn_choice), None)

            if selected_pawn:
                return selected_pawn, move_choice

            else:
                print("\033[31mInvalid Option: select a pawn from the list\033[0m")

    # Reprints game state
    def render_state(self, game: Game) -> None:
        print_board(game)
        if not game._has_game_ended():
            print(
                f"\033[33mPLAYER # {game.active_player.number}'S ({game.active_player.color}) TURN\033[0m\n"
            )


class DummyTestUI(LudoTerminalUI):
    def prompt_and_roll_dice(self, player: Player, dice: Dice) -> int:
        result = dice.roll()
        print(f"\033[32mYou rolled a {result} !!!\033[0m\n")
        if dice.voided():
            print("\033[31mSorry your turn is voided 😔\033[0m\n\n\n")

        return result

    def ask_move(self, pawns: list[Pawn], moves: list[int]) -> tuple[Pawn, int]:
        for move in moves:
            for pawn in pawns:
                if pawn.is_valid_move_with_steps(move):
                    return (pawn, move)

        return (pawns[0], moves[0])

    def render_state(self, game: Game) -> None:
        return super().render_state(game)


if __name__ == "__main__":
    main()
