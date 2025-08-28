class LudoBoard:
    """A simplified Ludo board using emoji characters."""

    _PAWNS = {"red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡"}

    _LAYOUT = [
        "🟥🟥🟥🟥🟥🟥⬜⬜⬜🟦🟦🟦🟦🟦🟦",
        "🟥⬛⬛⬛⬛🟥⬜🟦🟦🟦⬛⬛⬛⬛🟦",
        "🟥⬛⬛⬛⬛🟥⭐🟦⬜🟦⬛⬛⬛⬛🟦",
        "🟥⬛⬛⬛⬛🟥⬜🟦⬜🟦⬛⬛⬛⬛🟦",
        "🟥⬛⬛⬛⬛🟥⬜🟦⬜🟦⬛⬛⬛⬛🟦",
        "🟥🟥🟥🟥🟥🟥⬜🟦⬜🟦🟦🟦🟦🟦🟦",
        "⬜🟥⬜⬜⬜⬜⬛⬛⬛⬜⬜⬜⭐⬜⬜",
        "⬜🟥🟥🟥🟥🟥⬛⬛⬛🟨🟨🟨🟨🟨⬜",
        "⬜⬜⭐⬜⬜⬜⬛⬛⬛⬜⬜⬜⬜🟨⬜",
        "🟩🟩🟩🟩🟩🟩⬜🟩⬜🟨🟨🟨🟨🟨🟨",
        "🟩⬛⬛⬛⬛🟩⬜🟩⬜🟨⬛⬛⬛⬛🟨",
        "🟩⬛⬛⬛⬛🟩⬜🟩⬜🟨⬛⬛⬛⬛🟨",
        "🟩⬛⬛⬛⬛🟩⬜🟩⭐🟨⬛⬛⬛⬛🟨",
        "🟩⬛⬛⬛⬛🟩🟩🟩⬜🟨⬛⬛⬛⬛🟨",
        "🟩🟩🟩🟩🟩🟩⬜⬜⬜🟨🟨🟨🟨🟨🟨",
    ]

    @staticmethod
    def _yellow_path():
        """Return the yellow path as a list of (x, y) coordinates."""
        p = [(8, 13)]  # launch

        # main track
        p += [(8, y) for y in range(12, 8, -1)]  # up to (8, 9)
        p += [(x, 8) for x in range(9, 15)]  # right to (14, 8)
        p += [(14, y) for y in range(7, 5, -1)]  # up to (14, 6)
        p += [(x, 6) for x in range(13, 8, -1)]  # left to (9, 6)
        p += [(8, y) for y in range(5, -1, -1)]  # up to (8, 0)
        p += [(x, 0) for x in range(7, 5, -1)]  # left to (6, 0)
        p += [(6, y) for y in range(1, 6)]  # down to (6, 5)
        p += [(x, 6) for x in range(5, -1, -1)]  # left to (0, 6)
        p += [(0, y) for y in range(7, 9)]  # down to (0, 8)
        p += [(x, 8) for x in range(1, 6)]  # right to (5, 8)
        p += [(6, y) for y in range(9, 15)]  # down to (6, 14)
        p += [(7, 14)]  # turn into final stretch

        # final stretch
        p += [(7, y) for y in range(13, 7, -1)]  # to (7, 8)

        return p

    @staticmethod
    def _rotate(pt, k, c=(7, 7)):
        """Rotate a point (x, y) k*90° clockwise around center c=(7,7)"""
        x, y = pt
        cx, cy = c
        dx, dy = x - cx, y - cy
        k %= 4
        if k == 0:  # 0°
            return (cx + dx, cy + dy)
        if k == 1:  # 90° CW
            return (cx + dy, cy - dx)
        if k == 2:  # 180°
            return (cx - dx, cy - dy)
        # k == 3:    # 270° CW (90° CCW)
        return (cx - dy, cy + dx)

    @classmethod
    def _generate_paths(cls):
        """Generate game paths for each color (0=launch, 1-50=main track, 51-56=final stretch)"""
        yellow = cls._yellow_path()
        return {
            "yellow": yellow,
            "green": [cls._rotate(p, 1) for p in yellow],  # 90° CW
            "red": [cls._rotate(p, 2) for p in yellow],  # 180°
            "blue": [cls._rotate(p, 3) for p in yellow],  # 270° CW
        }

    _NESTS: dict[str, list[tuple[int, int]]] = {
        "red": [(1, 1), (1, 4), (4, 1), (4, 4)],
        "blue": [(1, 10), (1, 13), (4, 10), (4, 13)],
        "green": [(10, 1), (10, 4), (13, 1), (13, 4)],
        "yellow": [(10, 10), (10, 13), (13, 10), (13, 13)],
    }

    _PATHS: dict[str, list[tuple[int, int]]] = {}

    def __init__(self):
        if self.__class__._PATHS == {}:
            self.__class__._PATHS = self.__class__._generate_paths()

        self._board = [list(row) for row in self._LAYOUT]
        self._reset_board()

    def _reset_board(self):
        # Base layout
        for row in range(15):
            for col in range(15):
                self._board[row][col] = self._LAYOUT[row][col]

        # Place all pawns in their nests
        for color in ["red", "blue", "green", "yellow"]:
            for row, col in self._NESTS[color]:
                self._board[row][col] = self._PAWNS[color]

    def set_pawns(self, player_positions):
        self._reset_board()

        for color, positions in player_positions.items():
            if color not in self._PAWNS:
                raise ValueError(f"Invalid color: {color}")
            if len(positions) != 4:
                raise ValueError(f"Need exactly 4 positions for {color}")

            # Clear current pawns for this color
            for row in range(15):
                for col in range(15):
                    if self._board[row][col] == self._PAWNS[color]:
                        self._board[row][col] = self._LAYOUT[row][col]

            # Place pawns in nests (for None positions)
            nest_count = positions.count(None)
            for i in range(nest_count):
                row, col = self._NESTS[color][i]
                self._board[row][col] = self._PAWNS[color]

            # Place pawns on path (for non-None positions)
            for pos in positions:
                if pos is not None:
                    try:
                        self.__class__.validate_position(pos)
                    except ValueError:
                        continue

                    row, col = self.__class__._PATHS[color][pos]

                    # Check final stretch restriction
                    if pos >= 51 and not self._can_enter_final_stretch(color, row, col):
                        raise ValueError(
                            f"Cannot place {color} pawn in wrong final stretch"
                        )

                    self._board[row][col] = self._PAWNS[color]

    def _can_enter_final_stretch(self, color, row, col):
        """Check if a color can enter a final stretch position."""
        # Check which color's final stretch this position belongs to
        for c, path in self.__class__._PATHS.items():
            if (row, col) in path[51:57]:  # Final stretch positions
                return c == color
        return True  # Not a final stretch position

    @classmethod
    def get_path_length(cls):
        return len(cls._PATHS["yellow"])

    @classmethod
    def validate_position(cls, position):
        path_length = cls.get_path_length()

        if position < 0:
            raise ValueError(f"Position cannot be negative. Got: {position}")

        if position >= path_length:
            raise ValueError(
                f"Position {position} is invalid. Valid range: 0-{path_length - 1}"
            )

        return True

    @classmethod
    def get_position_coordinates(cls, color, position):
        cls.validate_position(position)
        return cls._PATHS[color][position]

    def render(self):
        """Render the board as a string."""
        return "\n".join("".join(row) for row in self._board)
