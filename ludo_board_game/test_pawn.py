import unittest

from ludo_board_game.player import Player


class TestPawn(unittest.TestCase):
    def setUp(self):
        Player.reset_player_count()  # Reset player count before each test
        self.player_one = Player()
        self.player_two = Player()

    def test_has_started(self):
        self.assertEqual(self.player_one.pawns[0].is_unlocked(), False)
        self.player_one.pawns[0].position = 1
        self.assertEqual(self.player_one.pawns[0].is_unlocked(), True)

    def test_has_finished(self):
        self.assertEqual(self.player_one.pawns[0].has_finished(), False)
        self.player_one.pawns[0].position = 57
        self.assertEqual(self.player_one.pawns[0].has_finished(), True)

    def test_board_position(self):
        self.player_two.pawns[1].position = 10
        self.assertEqual(self.player_two.pawns[1].board_absolute_position(), 23)


if __name__ == "__main__":
    unittest.main()
