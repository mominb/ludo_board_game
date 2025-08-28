from ludo_board_game.ludo_board import LudoBoard


class LudoDemo:
    def __init__(self):
        self.board = LudoBoard()
        self.player_emojis = {"red": "🔴", "blue": "🔵", "green": "🟢", "yellow": "🟡"}

    def show_menu(self):
        """Display the player selection menu."""
        print("\nLUDO BOARD INTERACTIVE DEMO")
        print("=" * 40)
        print("Select a player to test their complete path:")
        print()
        print("1. 🔴 Red Player")
        print("2. 🔵 Blue Player")
        print("3. 🟢 Green Player")
        print("4. 🟡 Yellow Player")
        print("q. Quit")
        print()

    def get_player_choice(self):
        while True:
            choice = input("Enter your choice (1-4 or q): ").strip().lower()

            if choice == "q":
                return None
            elif choice == "1":
                return "red"
            elif choice == "2":
                return "blue"
            elif choice == "3":
                return "green"
            elif choice == "4":
                return "yellow"
            else:
                print("Invalid choice. Please enter 1-4 or 'q' to quit.")

    def run_player_demo(self, player_color):
        try:
            path_length = LudoBoard.get_path_length()
        except ValueError as e:
            print(f"Error: {e}")
            return

        current_position = 0

        while current_position <= path_length:
            if current_position < path_length:
                # Pawn is still on the board
                pawn_positions: dict[str, list[int | None]] = {
                    "red": [None, None, None, None],
                    "blue": [None, None, None, None],
                    "green": [None, None, None, None],
                    "yellow": [None, None, None, None],
                }
                # Set the active player's pawn position
                pawn_positions[player_color] = [current_position, None, None, None]

                try:
                    # Validate position before setting pawns
                    LudoBoard.validate_position(current_position)
                    self.board.set_pawns(pawn_positions)

                    # Display current state
                    print(f"Position {current_position}/{path_length - 1}:")
                    if current_position == 0:
                        print(f"{player_color.title()} pawn at LAUNCH position")
                    elif current_position < 51:
                        print(f"{player_color.title()} pawn on main track")
                    else:
                        print(f"{player_color.title()} pawn in FINAL STRETCH")

                    print()
                    print(self.board.render())

                    coordinates = self.board.get_position_coordinates(
                        player_color, current_position
                    )
                    print(f"Coordinates: {coordinates}")

                except ValueError as e:
                    print(f"Error at position {current_position}: {e}")
                    break
                except Exception as e:
                    print(f"Unexpected error at position {current_position}: {e}")
                    break

            else:
                # Pawn has reached final destination
                pawn_positions = {
                    "red": [None, None, None, None],
                    "blue": [None, None, None, None],
                    "green": [None, None, None, None],
                    "yellow": [None, None, None, None],
                }

                self.board.set_pawns(pawn_positions)
                print(f"WINNER! {player_color.title()} pawn has reached HOME!")
                print(
                    "The pawn has completed its journey and disappeared from the board."
                )
                print()
                print(self.board.render())
                print()
                break

            # Wait for user input
            user_input = (
                input("\nPress Enter to continue (or 'menu' to return): ")
                .strip()
                .lower()
            )
            if user_input == "menu":
                return

            # Move to next position
            current_position += 1
            print("\n" + "=" * 50 + "\n")

        try:
            path_length = LudoBoard.get_path_length()
            print(
                f"   • Final stretch: positions 51-{path_length - 1} ({path_length - 51} steps)"
            )
            print(f"   • Total journey: {path_length} steps to reach home")
        except ValueError as e:
            print(f"   • Error getting path info: {e}")

        input("\nPress Enter to return to menu...")

    def run(self):
        try:
            while True:
                self.show_menu()
                player_choice = self.get_player_choice()

                if player_choice is None:
                    break

                self.run_player_demo(player_choice)

        except KeyboardInterrupt:
            print("Demo interrupted")


def main():
    demo = LudoDemo()
    demo.run()


if __name__ == "__main__":
    main()
