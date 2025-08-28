import unittest

from ludo_board_game.color import Color
from ludo_board_game.player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self):
        Player.reset_player_count()

    def test_player_creation_and_numbering(self):
        # Test that players are numbered sequentially starting from 1
        player1 = Player()
        player2 = Player()
        player3 = Player()

        self.assertEqual(player1.number, 1)
        self.assertEqual(player2.number, 2)
        self.assertEqual(player3.number, 3)
        self.assertEqual(Player.player_count, 3)

    def test_player_color_assignment(self):
        # Test that players get colors in the correct order
        player1 = Player()
        player2 = Player()
        player3 = Player()
        player4 = Player()

        self.assertEqual(player1.color, Color.RED)
        self.assertEqual(player2.color, Color.BLUE)
        self.assertEqual(player3.color, Color.GREEN)
        self.assertEqual(player4.color, Color.YELLOW)

    def test_maximum_player_limit(self):
        # Test that creating more than 4 players raises an error
        Player()
        Player()
        Player()
        Player()

        with self.assertRaises(ValueError) as context:
            Player()

        self.assertEqual(str(context.exception), "Cannot have more than 4 players")

    def test_player_has_four_pawns(self):
        # Test that each player is created with exactly 4 pawns
        player = Player()

        self.assertEqual(len(player.pawns), 4)
        for i, pawn in enumerate(player.pawns):
            self.assertEqual(pawn.number, i + 1)
            self.assertEqual(pawn.owner, player)
            self.assertEqual(pawn.position, 0)  # All pawns start at home

    def test_reset_player_count(self):
        # Test that reset_player_count properly resets the class variable
        Player()
        Player()
        self.assertEqual(Player.player_count, 2)

        Player.reset_player_count()
        self.assertEqual(Player.player_count, 0)

        new_player = Player()
        self.assertEqual(new_player.number, 1)

    def test_player_string_representation(self):
        # Test the __str__ method returns correct format
        player = Player()
        expected = f"Player # 1 having a color of {Color.RED}"
        self.assertEqual(str(player), expected)

    def test_win_position_initialization(self):
        # Test that win_position is initially None
        player = Player()
        self.assertIsNone(player.win_position)

    def test_locked_pawns_all_at_start(self):
        # Test locked_pawns returns all pawns when they're all at position 0
        player = Player()
        locked = player.locked_pawns()

        self.assertEqual(len(locked), 4)
        for pawn in locked:
            self.assertEqual(pawn.position, 0)

    def test_locked_pawns_with_mixed_positions(self):
        # Test locked_pawns returns only pawns at position 0
        player = Player()
        player.pawns[0].position = 1  # Move first pawn
        player.pawns[1].position = 10  # Move second pawn
        # pawns[2] and pawns[3] remain at position 0

        locked = player.locked_pawns()

        self.assertEqual(len(locked), 2)
        self.assertIn(player.pawns[2], locked)
        self.assertIn(player.pawns[3], locked)

    def test_enroute_pawns_none_at_start(self):
        # Test enroute_pawns returns empty list when all pawns are locked
        player = Player()
        enroute = player.enroute_pawns()

        self.assertEqual(len(enroute), 0)

    def test_enroute_pawns_with_active_pawns(self):
        # Test enroute_pawns returns pawns that are unlocked but not finished
        player = Player()
        player.pawns[0].position = 1  # Unlocked, not finished
        player.pawns[1].position = 25  # Unlocked, not finished
        player.pawns[2].position = 0  # Locked
        player.pawns[3].position = 57  # Finished

        enroute = player.enroute_pawns()

        self.assertEqual(len(enroute), 2)
        self.assertIn(player.pawns[0], enroute)
        self.assertIn(player.pawns[1], enroute)

    def test_pawns_on_final_lane_none_initially(self):
        # Test pawns_on_final_lane returns empty list when no pawns are on final lane
        player = Player()
        final_lane = player.pawns_on_final_lane()

        self.assertEqual(len(final_lane), 0)

    def test_pawns_on_final_lane_with_final_lane_pawns(self):
        # Test pawns_on_final_lane returns pawns in the final stretch (52-56)
        player = Player()
        player.pawns[0].position = 52  # On final lane
        player.pawns[1].position = 55  # On final lane
        player.pawns[2].position = 25  # Not on final lane
        player.pawns[3].position = 57  # Finished, not on final lane

        final_lane = player.pawns_on_final_lane()

        self.assertEqual(len(final_lane), 2)
        self.assertIn(player.pawns[0], final_lane)
        self.assertIn(player.pawns[1], final_lane)

    def test_pawn_absolute_positions_all_locked(self):
        # Test pawn_absolute_positions returns all zeros when pawns are locked
        player = Player()
        positions = player.pawn_absolute_positions()

        self.assertEqual(positions, [0, 0, 0, 0])

    def test_pawn_absolute_positions_with_active_pawns(self):
        # Test pawn_absolute_positions calculates correct board positions
        player = Player()
        player.pawns[0].position = 1  # Should be at absolute position 1
        player.pawns[1].position = 10  # Should be at absolute position 10

        positions = player.pawn_absolute_positions()

        # First pawn at position 1 should be at absolute position 1
        # Second pawn at position 10 should be at absolute position 10
        self.assertEqual(positions[0], 1)
        self.assertEqual(positions[1], 10)
        self.assertEqual(positions[2], 0)  # Still locked
        self.assertEqual(positions[3], 0)  # Still locked

    def test_pawns_at_no_pawns_at_position(self):
        # Test pawns_at returns empty list when no pawns are at specified position
        player = Player()
        pawns = player.pawns_at(15)

        self.assertEqual(len(pawns), 0)

    def test_pawns_at_with_pawns_at_position(self):
        # Test pawns_at returns pawns at the specified absolute position
        player = Player()
        player.pawns[0].position = 1  # At absolute position 1
        player.pawns[1].position = 1  # Also at absolute position 1

        pawns = player.pawns_at(1)

        self.assertEqual(len(pawns), 2)
        self.assertIn(player.pawns[0], pawns)
        self.assertIn(player.pawns[1], pawns)

    def test_has_won_false_initially(self):
        # Test has_won returns False when no pawns have finished
        player = Player()

        self.assertFalse(player.has_won())

    def test_has_won_false_with_some_finished(self):
        # Test has_won returns False when less than 4 pawns have finished
        player = Player()
        player.pawns[0].position = 57  # Finished
        player.pawns[1].position = 57  # Finished
        player.pawns[2].position = 57  # Finished
        player.pawns[3].position = 25  # Not finished

        self.assertFalse(player.has_won())

    def test_has_won_true_all_finished(self):
        # Test has_won returns True when all 4 pawns have finished
        player = Player()
        for pawn in player.pawns:
            pawn.position = 57  # All pawns finished

        self.assertTrue(player.has_won())


if __name__ == "__main__":
    unittest.main()
