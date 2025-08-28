import unittest
from unittest.mock import Mock, patch

from ludo_board_game.player import Player

# Import the modules we need to test
from project import get_num_players, print_board, print_pawn_position


class TestMainFunctions(unittest.TestCase):
    def setUp(self):
        Player.reset_player_count()

    @patch("builtins.input")
    def test_get_num_players(self, mock_input):
        mock_input.return_value = "3"

        result = get_num_players()

        self.assertEqual(result, 3)

        # Test invalid input (not between 1 and 4)
        mock_input.side_effect = ["5", "0", "2"]

        result = get_num_players()

        self.assertEqual(result, 2)
        self.assertEqual(mock_input.call_count, 4)

    @patch("builtins.print")
    def test_print_pawn_position(self, mock_print):
        # Test case 1: locked pawn
        mock_pawn = Mock()
        mock_pawn.number = 1
        mock_pawn.is_enroute.return_value = False
        mock_pawn.has_finished.return_value = False
        mock_pawn.is_locked.return_value = True

        print_pawn_position(mock_pawn)
        mock_print.assert_called_with("Pawn # 1 (currently locked)")

        mock_print.reset_mock()

        # Test case 2: pawn en route
        mock_pawn.number = 2
        mock_pawn.is_enroute.return_value = True
        mock_pawn.has_finished.return_value = False
        mock_pawn.is_locked.return_value = False
        mock_pawn.position = 15

        print_pawn_position(mock_pawn)
        mock_print.assert_called_with("Pawn # 2 at position 15")

        mock_print.reset_mock()

        # Test case 3: finished pawn
        mock_pawn.number = 3
        mock_pawn.is_enroute.return_value = False
        mock_pawn.has_finished.return_value = True
        mock_pawn.is_locked.return_value = False

        print_pawn_position(mock_pawn)
        mock_print.assert_called_with("Pawn # 3 (finished)")

    @patch("project.LudoBoard")
    @patch("builtins.print")
    def test_print_board(self, mock_print, mock_ludo_board):
        mock_board_instance = Mock()
        mock_ludo_board.return_value = mock_board_instance
        mock_board_instance.render.return_value = "rendered board"

        mock_game = Mock()

        mock_player = Mock()
        mock_player.color = "RED"

        mock_pawn1 = Mock()
        mock_pawn1.position = 0  # Should become None

        mock_pawn2 = Mock()
        mock_pawn2.position = 5  # Should become 4 (position - 1)

        mock_pawn3 = Mock()
        mock_pawn3.position = 1  # Should become 0 (position - 1)

        mock_player.pawns = [mock_pawn1, mock_pawn2, mock_pawn3]
        mock_game.players = [mock_player]

        print_board(mock_game)

        mock_ludo_board.assert_called_once()

        # Verify set_pawns was called with correct transformed positions
        expected_positions = {"RED": [None, 4, 0]}
        mock_board_instance.set_pawns.assert_called_once_with(expected_positions)

        mock_board_instance.render.assert_called_once()
        mock_print.assert_called_once_with("rendered board")


if __name__ == "__main__":
    unittest.main()
