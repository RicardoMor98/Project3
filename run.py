import random

# the game board as 2D list
# Constants
HIT_CHAR = 'X'
MISS_CHAR = 'O'
BLANK_CHAR = '.'
MAX_MISSES = 20
NUM_ROWS = 10
NUM_COLS = 10
MIN_ROW_LABEL = 'A'
MAX_ROW_LABEL = 'J'

# Simplified ship sizes
SHIP_SIZES = {i: 1 for i in range(1, 6)}

# initialize the board
USER_BOARD = [['.' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
CPU_BOARD = [['.' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# implementing a ship class

class Ship:
    def __init__(self, name, position, size):
        self.name = name
        self.position = position
        self.size = size
        self.sunk = False

# game loop  
class Game: 
    def __init__(self, max_misses=MAX_MISSES):
        self.max_misses = max_misses
        self.guesses = []
        self.user_board = USER_BOARD.copy()
        self.cpu_board = CPU_BOARD.copy()
        self.guessed_positions = set()  # Track guessed positions  
    
    def display_board(self, board):
        print("  ", end="")
        for col in range(NUM_COLS):
            print(col+1, end=" ")
        print()
        for row in range(NUM_ROWS):
         print(MIN_ROW_LABEL + str(row+1), end=" | ")
        for col in range(NUM_COLS):
            print(board[row][col], end=" ")
        print("|", MIN_ROW_LABEL + str(row+1))
    
    def initialize_board(self, board):
        return [['.' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]  

    def update_game(self, guess_status, position, board):
        row, column = position
        if guess_status:
            # User hit a ship
            board[row][column] = GREEN + HIT_CHAR + RESET
        else:
            # Missed target or CPU hit
            board[row][column] = BLUE + MISS_CHAR + RESET
            self.guesses.append(position)
            self.guessed_positions.add(position)  # Mark as guessed 

    def is_complete(self):
        if len(self.guesses) == self.max_misses:
            print("Sorry! No guesses left.")
            return True
        return False  

    def get_guess(self):
        while True:
            try:
                row_label = input("Enter a row label (A-J): ").upper()
                row = ord(row_label) - ord('A')
                column = int(input("Enter a column (1-10): "))
                if 0 <= row < NUM_ROWS and 0 <= column < NUM_COLS and (row, column) not in self.guessed_positions:
                    return (row, column)
            except ValueError:
                print("Invalid input. Please enter letters for rows and numbers for columns.")

    def end_program():
        while True:
            user_input = input("Play again? (Y/N) ").upper()
            if user_input in ['Y', 'N']:
                return user_input == 'Y'

    def play_battleship():
            """Controls flow of Battleship games including display of welcome and goodbye messages."""
        # Prompt for username
            username = input("Please enter your username: ")
            print(f"\nWelcome to Battleship, {username}!\n")
            game = Game()
            game.display_board(game.user_board)  # Display initial user board
            game.display_board(game.cpu_board)  # Display initial cpu board

    while not game.is_complete():
        pos = game.get_guess()
        result = game.check_guess(pos, game.cpu_board)  # Check guess against CPU board
        game.update_game(result, pos, game.cpu_board)  # Update game state
        game.display_board(game.user_board)  # Display updated board

    game_over = game.end_program()  # End program based on user choice

    print("Goodbye.")
    
def main():
    play_battleship()

if __name__ == "__main__":
    main()         