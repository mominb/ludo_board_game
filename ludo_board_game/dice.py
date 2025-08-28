import random
from typing import List, Tuple


class Dice:
    def __init__(self) -> None:
        # Stores all roll results for the current turn
        # Each RollResult tracks the number rolled and if it's been used
        self.roll_results: List["RollResult"] = []

    def __str__(self) -> str:
        (rolls, sixes) = self._stats()
        return f"rollCount: {rolls}, sixes:{sixes}"

    def _stats(self) -> Tuple[int, int]:
        rolls = len(self.roll_results)
        # Count how many 6s were rolled this turn
        sixes = list(map(lambda r: r.result, self.roll_results)).count(6)
        return (rolls, sixes)

    def can_roll(self) -> bool:
        (rolls, sixes) = self._stats()
        # Can roll if under 3 rolls and every roll so far was a 6
        return rolls < 3 and sixes == rolls

    def voided(self) -> bool:
        (rolls, sixes) = self._stats()
        return rolls == 3 and sixes == 3

    def roll(self) -> int:
        if not self.can_roll():
            raise ValueError("Cannot roll because stats", self._stats())

        # Generate random number 1-6
        number = random.randint(1, 6)

        # Store the roll result for tracking
        self.roll_results.append(RollResult(number))

        return number

    def unused_results(self) -> List["RollResult"]:
        return list(filter(lambda r: not r.used, self.roll_results))

    def has_used_all_results(self) -> bool:
        return len(self.unused_results()) == 0

    def is_value_in_unused_results(self, value: int) -> bool:
        for roll_result in self.roll_results:
            if roll_result.result == value and not roll_result.used:
                return True
        return False

    def mark_first_matching_result_as_used(self, value: int) -> bool:
        for roll_result in self.roll_results:
            if roll_result.result == value and not roll_result.used:
                roll_result.used = True
                return True
        return False

    def reset(self) -> None:
        self.roll_results = []

    def can_open_pawn(self) -> bool:
        if self.voided():
            return False

        for roll_result in self.roll_results:
            if roll_result.result == 6 and not roll_result.used:
                return True
        return False


class RollResult:
    def __init__(self, result: int) -> None:
        if result < 1 or result > 6:
            raise ValueError(
                f"Dice result must be an integer between 1 and 6, got {result}"
            )

        self.result: int = result
        self.used: bool = False

    def __str__(self) -> str:
        status = "used" if self.used else "unused"
        return f"{self.result} ({status})"
