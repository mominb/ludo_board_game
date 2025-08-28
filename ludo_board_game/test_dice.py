import unittest
from unittest.mock import patch

from ludo_board_game.dice import Dice, RollResult


class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    @patch("random.randint", return_value=6)
    def test_roll_six(self, mock_randint):
        result = self.dice.roll()
        self.assertEqual(result, 6)
        self.assertEqual(len(self.dice.roll_results), 1)
        self.assertEqual(self.dice.roll_results[0].result, 6)
        self.assertEqual(self.dice.roll_results[0].used, False)

    @patch("random.randint", side_effect=[6, 6, 6])
    def test_can_roll_false(self, mock_randint):
        for _ in range(3):
            self.dice.roll()
        self.assertFalse(self.dice.can_roll())

    @patch("random.randint", side_effect=[6, 6])
    def test_can_roll_true(self, mock_randint):
        for _ in range(2):
            self.dice.roll()
            self.assertTrue(self.dice.can_roll())
            self.assertFalse(self.dice.voided())

    @patch("random.randint", side_effect=[6, 6, 6])
    def test_voided_true(self, mock_randint):
        for _ in range(3):
            self.dice.roll()
        self.assertTrue(self.dice.voided())

    @patch("random.randint", side_effect=[6, 6, 5])
    def test_voided_false(self, mock_randint):
        for _ in range(3):
            self.dice.roll()
        self.assertFalse(self.dice.voided())

    def test_reset(self):
        self.dice.roll_results = [RollResult(6), RollResult(5)]
        self.dice.reset()
        self.assertEqual(len(self.dice.roll_results), 0)

    def test_results_used(self):
        self.dice.roll_results = [RollResult(6), RollResult(5)]
        for result in self.dice.roll_results:
            result.used = True
        self.assertTrue(self.dice.has_used_all_results())

    def test_str(self):
        self.dice.roll_results = [RollResult(6), RollResult(5)]
        self.assertEqual(str(self.dice), "rollCount: 2, sixes:1")

    def test_can_open_pawn(self):
        self.dice.roll_results = [RollResult(6), RollResult(5)]
        self.assertEqual(self.dice.can_open_pawn(), True)
        self.dice.roll_results = [RollResult(1)]
        self.assertEqual(self.dice.can_open_pawn(), False)


if __name__ == "__main__":
    unittest.main()
