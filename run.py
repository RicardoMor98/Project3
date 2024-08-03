import random

class Game:
    def __init__(self):
        # Initialize the game parameters
        self.size = 7  # Board size is 7x7
        self.ships = 5  # Number of ships for each player
        # Initialize the boards for the player and the computer
        self.p_board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.c_board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        # Set the initial number of turns and hits
        self.p_turns = 15  # Player's available turns
        self.c_turns = 15  # Computer's available turns
        self.p_hits = 0  # Player's successful hits on computer's ships
        self.c_hits = 0  # Computer's successful hits on player's ships

    # Get and validate the player's name
    def get_name(self):
        while True:
            name = input("Enter your name: ")
            if len(name) >= 3:  # Ensure the name has at least 3 characters
                return name
            print("Name must be at least 3 characters.")  # Prompt user again if name is too short

    # Display the board
    def show_board(self, board, hide_ships=False):
        # Print column headers (0 to 6)
        print("   " + " ".join(map(str, range(self.size))))
        # Print each row of the board with its index
        for i, row in enumerate(board):
            # If hiding ships, replace 'S' with empty space
            display_row = [" " if hide_ships and cell == "S" else cell for cell in row]
            print(f"{i} |" + "|".join(display_row) + "|")  # Format and print the row

    # Randomly place ships on the board
    def place_ships(self, board):
        for _ in range(self.ships):
            # Generate random row and column for ship placement
            r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            # Ensure the spot is empty before placing the ship
            while board[r][c] == "S":
                r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            board[r][c] = "S"  # Place the ship ('S') at the generated coordinates

    # Check if the player's input coordinates are valid (within the board boundaries)
    def is_valid(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    # Handle the logic for firing at a specific board position
    def fire(self, board, r, c, player):
        if board[r][c] == "S":  # If the shot hits a ship
            print(f"{player} hit a ship!")
            board[r][c] = "H"  # Mark the hit spot with 'H'
            return True
        else:
            print(f"{player} missed.")  # If the shot misses
            board[r][c] = "M"  # Mark the miss with 'M'
            return False

    # Main game loop where the game is played
    def play(self):
        print("Welcome to Battleship!")  # Introductory message
        print("Destroy all enemy ships in 15 turns.\n")
        print("Your main objective is to find and destroy all the hidden ships on the map!\n")
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

        name = self.get_name()  # Get player's name
        self.place_ships(self.p_board)  # Place player's ships on the board
        self.place_ships(self.c_board)  # Place computer's ships on the board

        p_guesses = set()  # Track player's guesses to avoid duplicates
        c_guesses = set()  # Track computer's guesses to avoid duplicates

        # Loop continues as long as both players have turns left and haven't sunk all ships
        while self.p_turns > 0 and self.c_turns > 0 and self.p_hits < self.ships and self.c_hits < self.ships:
            print(f"\n{name}'s Board:")  # Display player's board
            self.show_board(self.p_board)
            print("\nComputer's Board:")  # Display computer's board (with ships hidden)
            self.show_board(self.c_board, hide_ships=True)

            # Player's turn to guess coordinates
            while True:
                try:
                    r = int(input("Enter row (0-6) or 'exit' to quit: "))  # Get row input
                    c = int(input("Enter column (0-6): "))  # Get column input

                    # Validate the coordinates and check if they were already guessed
                    if not self.is_valid(r, c) or (r, c) in p_guesses:
                        print("Invalid or repeated guess. Try again.")
                        continue

                    p_guesses.add((r, c))  # Record the guess
                    if self.fire(self.c_board, r, c, name):  # Check if the guess hits a ship
                        self.p_hits += 1  # Increment player's hit count if successful
                    break
                except ValueError:
                    print("Please enter valid numbers.")  # Handle non-integer inputs

            # Computer's turn to randomly guess coordinates
            c_r, c_c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while (c_r, c_c) in c_guesses:  # Ensure the computer doesn't repeat guesses
                c_r, c_c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            c_guesses.add((c_r, c_c))  # Record the computer's guess

            if self.fire(self.p_board, c_r, c_c, "Computer"):  # Check if the computer's guess hits a ship
                self.c_hits += 1  # Increment computer's hit count if successful

            # Decrease remaining turns after each round
            self.p_turns -= 1
            self.c_turns -= 1

            # Display remaining turns and current scores
            print(f"\nTurns left: {self.p_turns} | {name}'s hits: {self.p_hits} | Computer's hits: {self.c_hits}")

        # End the game and announce the results
        self.end_game(name)

    # Determine the game outcome and offer a replay option
    def end_game(self, name):
        print("\nGame Over!")  # End game message
        self.show_board(self.p_board)  # Display player's final board
        self.show_board(self.c_board)  # Display computer's final board

        # Determine who won based on the number of hits
        if self.p_hits == self.ships:
            print(f"\nCongrats, {name}! You sank all the computer's ships!")
        elif self.c_hits == self.ships:
            print("\nThe computer sank all your ships. Better luck next time!")
        else:
            print("\nIt's a draw!")  # In case of a tie

        # Offer the player a chance to replay the game
        if input("\nPlay again? (yes/no): ").lower() == "yes":
            self.__init__()  # Reset the game state
            self.play()  # Start a new game

# Start the game if the script is run directly
if __name__ == "__main__":
    Game().play()
