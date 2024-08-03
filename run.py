import random

# Class and Initializes the board size, ship size, and sets up two 7x7 grids
class Board:
    def __init__(self):
        self.board_size = 7
        self.ship_size = 5
        self.player_board = [
            [" " for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        self.computer_board = [
            [" " for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        self.player_turns = 15
        self.computer_turns = 15
        self.player_ships = 5
        self.computer_ships = 5
        self.player_score = 0
        self.computer_score = 0

# Username Input ensures that the user enters a valid username with at least 3 characters
    def get_username(self):
        while True:
            username = input("Enter your username: ")
            if len(username) < 3:
                print("Please enter a minimum of 3 chars")
            else:
                return username

# Display Board this method displays the board in a readable format
    def display_board(self, board, is_player=True):
        print("   0 1 2 3 4 5 6")
        for i, row in enumerate(board):
            if not is_player:
                row = [" " if cell == "S" else cell for cell in row]
            print(f"{i} |{'|'.join(row)}|")

# Placing Ships randomly places ships ('S') on the board ensures no two ships occupy the same spot
    def place_ships(self, board, ships):
        for _ in range(ships):
            row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            while board[row][col] == "S":
                row, col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
            board[row][col] = "S"

# Input Validation validates that the entered coordinates (row and column) are within the board boundaries
    def validate_input(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size

# Shooting Logic handles the logic for making a shot 
    def make_shot(self, board, row, col, player):
        if board[row][col] == "S": # If a ship is hit ('S')
            print(f"\n{player} Sunk a Battleship!")
            board[row][col] = "H" # it's marked as 'H' (hit)
            return True
        else:
            print(f"\n{player} Shot in the ocean!")
            board[row][col] = "M" # it's marked as 'M' (miss)
            return False

# Instructions provides the user with instructions on how to play the game
    def display_instructions(self):
        print("Welcome to the Battleship game!\n"
              "Your main objective is to find and destroy all the hidden ships on the map!\n")
        print("How to play:")
        print("1. The game consists of two boards, one for each player.")
        print("2. The boards are marked with the numbers 0 - 6.")
        print("3. You have a total of 15 turns to sink 5 hidden ships.")
        print("4. Guess a row and a column between 0 and 6.")
        print("5. If you HIT a ship, you will see 'H'.")
        print("6. If you MISS a ship, you will see 'M'.")
        print("7. Your ships are displayed as 'S'.")
        print("8. Type 'exit' to quit the game at any time.")
        print("\nI wish you good fortune in wars to come!\n")

# Main Loop the game runs in a loop until either the player or computer runs out of turns or loses all ships
    def play_game(self):
        self.display_instructions()
        player_name = self.get_username()

        self.place_ships(self.player_board, self.player_ships)
        self.place_ships(self.computer_board, self.computer_ships)

        player_guessed_coordinates = set()
        computer_guessed_coordinates = set()

# Player Turn the player inputs row and column values to guess the location of the computer's ships
        while (
            self.player_turns > 0
            and self.computer_turns > 0
            and self.player_ships > 0
            and self.computer_ships > 0
        ):
            print(f"\n{player_name}'s Board:")
            self.display_board(self.player_board)
            print("\nCPU's Board:")
            self.display_board(self.computer_board, False)
#  The input is validated to ensure it's within the board and not a repeated guess
            while True:
                row_input = input("Enter row (0-6) or type 'exit' to quit: ") 
                if row_input.lower() == "exit":
                    return

                col_input = input("Enter column (0-6): ")

                try:
                    row = int(row_input)
                    col = int(col_input)

                    if not self.validate_input(row, col):
                        print("Invalid coordinates. Try again.")
                        continue

                    if (row, col) in player_guessed_coordinates:
                        print("You already tried this coordinate. Try again.")
                        continue

                    player_guessed_coordinates.add((row, col))
                    player_hit = self.make_shot(self.computer_board, row, col, player_name)

                    if player_hit:
                        self.computer_ships -= 1
                        self.player_score += 1
                    break

                except ValueError:
                    print("Invalid input. Please enter a number.")
# Computer Turn the computer randomly selects a position to attack on the player's board
            comp_row, comp_col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)

            while (comp_row, comp_col) in computer_guessed_coordinates:
                comp_row, comp_col = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)

            computer_guessed_coordinates.add((comp_row, comp_col))
            comp_hit = self.make_shot(self.player_board, comp_row, comp_col, 'CPU')
# The program checks to make sure the guess hasn't been made before and processes the hit or miss.
            if comp_hit:
                self.player_ships -= 1
                self.computer_score += 1

            self.player_turns -= 1
            self.computer_turns -= 1

            print(f"""\nTurns left: {player_name} = {self.player_turns}, CPU = {self.computer_turns}
Scores:     {player_name} = {self.player_score}, CPU = {self.computer_score}""")
# End Game after the main loop ends
        print("\nGame Over!")
        print(f"{player_name}'s Board:")
        self.display_board(self.player_board)
        print("\nCPU's Board:")
        self.display_board(self.computer_board, is_player=False)
# the game checks who the winner is, displays the final boards, and the results
        if self.player_ships == 0:
            print("\nSorry, better luck next time. CPU sunk all your ships!")
        elif self.computer_ships == 0:
            print(f"\nCongratulations, {player_name}! You sunk all the CPU's ships!")
        else:
            print("\nIt's a draw! Both players have ships remaining.")

        print(f"\nScores: {player_name} = {self.player_score}, CPU: {self.computer_score}")
# Replay Option
        while True:
            play_again = input("\nDo you want to play again? (yes/no): ")
            if play_again.lower() in ["yes", "no"]:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if play_again.lower() == "yes":
            self.reset_game()
            self.play_game()
        else:
            print("Thank you for playing! Goodbye.")

    def reset_game(self):
        self.player_board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.computer_board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.player_turns = 15
        self.computer_turns = 15
        self.player_ships = 5
        self.computer_ships = 5
        self.player_score = 0
        self.computer_score = 0

if __name__ == "__main__":
    game = Board()
    game.play_game()
