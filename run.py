import random

# ANSI escape codes for colors
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'  # Reset color

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

def get_random_position():
    """Generates a random location on a board of NUM_ROWS x NUM_COLS."""
    row_choice = random.randint(0, NUM_ROWS - 1)
    col_choice = random.randint(0, NUM_COLS - 1)
    return (row_choice, col_choice)

def play_battleship():
    """Controls flow of Battleship games including display of welcome and goodbye messages."""
    # Prompt for username
    username = input("Please enter your username: ")
    print(f"\nWelcome to Battleship, {username}!\n")
    
    

    
    game = Game()
    game.display_board(USER_BOARD)  # Display initial user board
    game.display_board(CPU_BOARD)  # Display initial cpu board

    while not game.is_complete():
            pos = game.get_guess()
            result = game.check_guess(pos, CPU_BOARD) # Check guess against CPU board
            game.update_game(result, pos, CPU_BOARD)  # Update game state
            game.display_board(game.user_board)  # Display updated board

    game_over = game.end_program() # End program based on user choice

    print("Goodbye.")

# game loop

class Game:
    def __init__(self, max_misses=MAX_MISSES):
        self.max_misses = max_misses
        self.guesses = []
        self.user_board = USER_BOARD.copy()
        self.cpu_board = CPU_BOARD.copy()
        self.guessed_positions = set()  # Track guessed positions

    def display_board(self, board):
        print("\n".join([" ".join([board[i][j] for j in range(NUM_COLS)]) for i in range(NUM_ROWS)]))

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

    def check_guess(self, position, board):
        row, column = position
        if board[row][column] == '.' and position not in self.guessed_positions:
            return True
        return False

    def get_guess(self):
        while True:
            try:
                row = int(input("Enter a row (0-9): ")) - 1
                column = int(input("Enter a column (0-9): ")) - 1
                if 0 <= row < NUM_ROWS and 0 <= column < NUM_COLS and (row, column) not in self.guessed_positions:
                    return (row, column)
            except ValueError:
                print("Invalid input. Please enter numbers.")

    def end_program():
        while True:
            user_input = input("Play again? (Y/N) ").upper()
            if user_input in ['Y', 'N']:
                return user_input == 'Y'

def main():
    play_battleship()

if __name__ == "__main__":
    main()         