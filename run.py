import random

class Game:
    def __init__(self):
        # Initialize the game parameters
        self.size = 7 
        self.ships = 5  
        # Initialize the boards for the player and the computer
        self.p_board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.c_board = [[" " for _ in range(self.size)] for _ in range(self.size)]
        # Set the initial number of turns and hits
        self.p_turns = 15  
        self.c_turns = 15  
        self.p_hits = 0  
        self.c_hits = 0  


# Username Input ensures that the user enters a valid username with at least 3 characters
    def get_name(self):
        while True:
            name = input("Enter your name: ")
            if len(name) >= 3:
                return name
            print("Name must be at least 3 characters.")

# Display Board this method displays the board in a readable format
    def show_board(self, board, hide_ships=False):
        print("   " + " ".join(map(str, range(self.size))))
        for i, row in enumerate(board):
            display_row = [" " if hide_ships and cell == "S" else cell for cell in row]
            print(f"{i} |" + "|".join(display_row) + "|")

# Placing Ships randomly places ships ('S') on the board ensures no two ships occupy the same spot
   def place_ships(self, board):
        for _ in range(self.ships):
            r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while board[r][c] == "S":
                r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            board[r][c] = "S"

# Input Validation validates that the entered coordinates (row and column) are within the board boundaries
    def is_valid(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

# Handle the logic for firing at a specific board position 
    def fire(self, board, r, c, player):
        if board[r][c] == "S":
            print(f"{player} hit a ship!")
            board[r][c] = "H"
            return True
        else:
            print(f"{player} missed.")
            board[r][c] = "M"
            return False

# Main Loop the game runs in a loop until either the player or computer runs out of turns or loses all ships
    def play(self):
        print("Welcome to Battleship!")
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

        name = self.get_name()
        self.place_ships(self.p_board)
        self.place_ships(self.c_board)

        p_guesses = set()
        c_guesses = set()
# Loop continues as long as both players have turns left and haven't sunk all ships
        while self.p_turns > 0 and self.c_turns > 0 and self.p_hits < self.ships and self.c_hits < self.ships:
            print(f"\n{name}'s Board:")
            self.show_board(self.p_board)
            print("\nComputer's Board:")
            self.show_board(self.c_board, hide_ships=True)

# Player Turn the player inputs row and column values to guess the location of the computer's ships
        while True:
                try:
                    r = int(input("Enter row (0-6) or 'exit' to quit: "))
                    c = int(input("Enter column (0-6): "))
# Validate the coordinates and check if they were already guessed
                    if not self.is_valid(r, c) or (r, c) in p_guesses:
                        print("Invalid or repeated guess. Try again.")
                        continue

                    p_guesses.add((r, c))
                    if self.fire(self.c_board, r, c, name):
                        self.p_hits += 1
                    break
                except ValueError:
                    print("Please enter valid numbers.")
 # Computer's turn to randomly guess coordinates
            c_r, c_c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while (c_r, c_c) in c_guesses:
                c_r, c_c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            c_guesses.add((c_r, c_c))

            if self.fire(self.p_board, c_r, c_c, "Computer"):
                self.c_hits += 1
# Decrease remaining turns after each round
            self.p_turns -= 1
            self.c_turns -= 1
# Display remaining turns and current scores
            print(f"\nTurns left: {self.p_turns} | {name}'s hits: {self.p_hits} | Computer's hits: {self.c_hits}")

        self.end_game(name)
 # Determine the game outcome and offer a replay option
             def end_game(self, name):
        print("\nGame Over!")
        self.show_board(self.p_board)
        self.show_board(self.c_board)
 # Determine who won based on the number of hits
        if self.p_hits == self.ships:
            print(f"\nCongrats, {name}! You sank all the computer's ships!")
        elif self.c_hits == self.ships:
            print("\nThe computer sank all your ships. Better luck next time!")
        else:
            print("\nIt's a draw!")
# Offer the player a chance to replay the game
        if input("\nPlay again? (yes/no): ").lower() == "yes":
            self.__init__()
            self.play()
# Start the game if the script is run directly
if __name__ == "__main__":
    Game().play()