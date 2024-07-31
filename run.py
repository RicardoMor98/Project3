import random

# ANSI escape codes for colors
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'  # Reset color

# welcome user to the game

print("Welcome to Battleship!")

# the game board as 2D list

# Constants
HIT_CHAR = 'x'
MISS_CHAR = 'o'
BLANK_CHAR = '.'
HORIZONTAL = 'h'
VERTICAL = 'v'
MAX_MISSES = 10
NUM_ROWS = 10
NUM_COLS = 10
ROW_IDX = 0
COL_IDX = 1
MIN_ROW_LABEL = ''
MAX_ROW_LABEL = ' '

# Game states
EMPTY = '.'
SHIP = 'S'
HIT = 'H'
MISS = 'M'
SUNK = 'X'

# initialize the board

BOARD_SIZE = NUM_ROWS
board = [[EMPTY for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# displaying the board

def get_user_name():
    return input("Please enter your name: ")

def update_board(board, x, y, hit, shot_by_cpu=False):
    if hit:
        if shot_by_cpu:
            board[x][y] = "\033[91mX\033[0m"  # Red for CPU hit
        else:
            board[x][y] = "\033[92mX\033[0m"  # Green for user hit
    else:
        board[x][y] = "\033[94mO\033[0m"  # Blue for miss

# Displaying the board
def display_board(board) :
    print(' ', end='')
    for col in range(NUM_COLS):
        print(col+1, end=' ')
    print('\n', end='')

    for row in range(NUM_ROWS):
        print(MIN_ROW_LABEL + str(row+1), end=' ')
        for col in range(NUM_COLS):
            print(board[row][col], end=' ')
        print('\n', end='')

    # Add padding to the top and bottom of the board
    top_bottom_padding = '\n' + '-' * (NUM_COLS * 3 + 6) + '\n'
    print(top_bottom_padding, end='')


    # Add padding to the right and left of the board
    left_right_padding = '+' + '-' * (NUM_COLS * 3 + 6) + '+'
    print(left_right_padding)

# placing the ships

def place_ship(board, x, y, length):
    for i in range(length):
        if x+i < BOARD_SIZE and y+i < BOARD_SIZE:  # Check both row and column
            board[x+i][y+i] = SHIP

def place_ship_by_user(board):
        for i in range(5):
            while True:
                try:
                    x = int(input("Enter the starting row for the ship (0-9): "))
                    y = int(input("Enter the starting column for the ship (0-9): "))
                    length = int(input("Enter the length of the ship (1-3): "))
                    direction = input("Enter the direction (horizontal/vertical): ")  # Added direction input
                    if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE and length > 0 and length <= 3:
                        if direction.lower() == 'horizontal' and all(board[x+i][y] == EMPTY for i in range(length)):
                            for i in range(length):
                                board[x+i][y] = SHIP
                            print("Ship successfully placed.")
                            display_board(board)  # Show the updated board
                            break
                        elif direction.lower() == 'vertical' and all(board[x][y+i] == EMPTY for i in range(length)):
                                for i in range(length):
                                    board[x][y+i] = SHIP
                                print("Ship successfully placed.")
                                display_board(board)  # Show the updated board
                                break
                        else:
                                print("Ship cannot fit at this location. Try again.")
                    else:
                                print("Invalid input. Please try again.")
                except ValueError:
                                print("Invalid input. Please enter numbers.")

def place_cpu_ships(board):
    for _ in range(5):  # Place 5 ships for the CPU
        random_ship_placement(board)

def random_ship_placement(board):
    ship_lengths = [3, 2, 1]
    directions = ['horizontal', 'vertical']
    
    for length in ship_lengths:
        while True:
            x = random.randint(0, BOARD_SIZE - length)
            y = random.randint(0, BOARD_SIZE - length)
            direction = random.choice(directions)
            
            if direction == 'horizontal' and all(board[x+i][y] == EMPTY for i in range(length)):
                for i in range(length):
                    board[x+i][y] = SHIP
                break
            elif direction == 'vertical' and all(board[x][y+i] == EMPTY for i in range(length)):
                for i in range(length):
                    board[x][y+i] = SHIP
                break

# coordinates guess

def guess_coordinate(board, player):
    while True:
        try:
            x, y = map(int, input(f"{player}, enter coordinates (row column): ").split())
            if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE:
                return x, y
            else:
                print("Coordinates out of bounds. Try again.")
        except ValueError:
            print("Invalid input. Please enter numbers.")

def has_ships_remaining(board):
    return any(cell == SHIP for row in board for cell in row)

# game loop 

def game_loop(user_name):
    user_ships_placed = False
    cpu_ships_placed = False
    turn = 'user'
    shots_fired = 0  # Track shots fired
    max_shots = 15  # Maximum allowed shots
    ships_sunk = False  # Track if all ships have been sunk

    # User places their ships
    place_ship_by_user(board)
    user_ships_placed = True

    # CPU places its ships
    place_cpu_ships(board)
    cpu_ships_placed = True

    while not user_ships_placed or not cpu_ships_placed:
        if not user_ships_placed:
            print(f"{user_name}, please place your ships.")
            place_ship_by_user(board)
            user_ships_placed = True
        if not cpu_ships_placed:
            place_cpu_ships(board)
            cpu_ships_placed = True

    while shots_fired < max_shots:
        if turn == 'user':
            user_guess = guess_coordinate(board, 'user')
            user_hit = board[user_guess[0]][user_guess[1]] == SHIP
            update_board(board, *user_guess, user_hit)
            if user_hit:
                print(f"{user_name}, you hit the target!")
            else:
                print(f"{user_name}, you missed the target!")
            ships_sunk = not has_ships_remaining(board)
            if ships_sunk:
                print(f"All your ships have been sunk, {user_name}!")
                play_again = input("Do you want to play again? (yes/no): ")
                if play_again.lower() == 'yes':
                    game_loop(user_name)  # Restart the game
                else:
                    break  # Exit the game
            turn = 'cpu'
        elif turn == 'cpu':
            cpu_guess = (random.randint(0, NUM_ROWS - 1), random.randint(0, NUM_COLS - 1))
            cpu_hit = board[cpu_guess[0]][cpu_guess[1]] == SHIP
            update_board(board, *cpu_guess, cpu_hit, shot_by_cpu=True)
            if cpu_hit:
                print("CPU hit your ship!")
            else:
                print("CPU missed the target!")
            ships_sunk = not has_ships_remaining(board)
            if ships_sunk:
                print("All your ships have been sunk!")
                play_again = input("Do you want to play again? (yes/no): ")
                if play_again.lower() == 'yes':
                    game_loop(user_name)  # Restart the game
                else:
                    break  # Exit the game
            turn = 'user'
        display_board(board)
        shots_fired += 1  # Increment shots fired

    # Determine winner based on remaining ships
    if has_ships_remaining(board):
        print("The game ends in a draw.")
    else:
        print("Congratulations, you won the Battleship!")

        
# run game

if __name__ == "__main__":
    user_name = input("Please enter your name: ")
    game_loop(user_name)