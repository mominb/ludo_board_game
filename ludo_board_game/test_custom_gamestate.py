from ludo_board_game.game import Game
from ludo_board_game.player import Player
from project import LudoTerminalUI, print_board


def setup_endgame_state():
    # Reset player count and create a 2-player game
    Player.reset_player_count()
    game = Game(3, LudoTerminalUI())

    # Set up Player 1 (Red) - 3 pawns won, 1 at home
    player1 = game.players[0]
    player1.pawns[0].position = 57  # Won position (adjust if needed)
    player1.pawns[1].position = 57  # Won position
    player1.pawns[2].position = 57  # Won position
    player1.pawns[3].position = 51  # At home/nest

    # Set up Player 2 (Blue) - 3 pawns won, 1 at home
    player2 = game.players[1]
    player2.pawns[0].position = 57  # Won position
    player2.pawns[1].position = 57  # Won position
    player2.pawns[2].position = 57
    player2.pawns[3].position = 51  # At home/nest

    # Set up Player 3  - 3 pawns won, 1 at home
    player2 = game.players[2]
    player2.pawns[0].position = 57  # Won position
    player2.pawns[1].position = 57  # Won position
    player2.pawns[2].position = 57  # Won position
    player2.pawns[3].position = 51  # At home/nest

    print("Current game state:")

    for i, player in enumerate(game.players):
        positions = [pawn.position for pawn in player.pawns]
        print(f"Player {i + 1} ({player.color}): Pawns at positions {positions}")

    print("\nShowing board state:")
    try:
        print_board(game)
    except Exception as e:
        print(f"Board display error: {e}")

    print("\nStarting the game...")
    input("Press Enter to begin...")

    return game


if __name__ == "__main__":
    game = setup_endgame_state()
    game.start()
