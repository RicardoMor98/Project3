import random

# welcome user to the game

print(f"Welcome to Battleship!")

# the game board as 2D list

BOARD_SIZE = 10
EMPTY = '.'
SHIP = 'S'
HIT = 'X'
MISS = 'O'

# initialize the board

board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# displaying the board

def get_user_name():
    return input("Please enter your name: ")

def update_board(board, x, y, hit):
    if hit:
        board[x][y] = HIT
    else:
        board[x][y] = MISS

def display_board(board):
    for row in board:
        print(' '.join(row))

# placing the ships

def place_ship(board, x, y, length):
    for i in range(length):
        if x+i < BOARD_SIZE:
            board[x+i][y] = SHIP

def place_ship_by_user(board):
    while True:
        try:
            x = int(input("Enter the starting row for the ship (0-9): "))
            y = int(input("Enter the starting column for the ship (0-9): "))
            length = int(input("Enter the length of the ship (1-3): "))
            if x >= 0 and x < len(board) and y >= 0 and y < len(board[0]) and length > 0 and length <= 3:
                for i in range(length):
                    if x + i < len(board) and y < len(board[0]):
                        board[x + i][y] = SHIP
                print("Ship successfully placed.")
                break
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers.")

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

# game loop 

def game_loop(user_name):
    user_ships_placed = False
    cpu_ships_placed = False
    
    while not user_ships_placed or not cpu_ships_placed:
        if not user_ships_placed:
            print(f"{user_name}, please place your ships.")
            place_ship(board, 5, 5, 3)  # Example ship placement
            user_ships_placed = True
        if not cpu_ships_placed:
            random_ship_placement(board)
            cpu_ships_placed = True

    while True:
        user_guess = guess_coordinate(board, 'user')
        cpu_guess = guess_coordinate(board, 'cpu')
        
        user_hit = board[user_guess[0]][user_guess[1]] == SHIP
        cpu_hit = board[cpu_guess[0]][cpu_guess[1]] == SHIP
        
        update_board(board, *user_guess, user_hit)
        update_board(board, *cpu_guess, cpu_hit)
        
        display_board(board)
        
        if user_hit:
            print(f"{user_name}, you hit the target!")
        else:
            print(f"{user_name}, you missed the target!")

        if cpu_hit:
            print("CPU hit your ship!")
        else:
            print("CPU missed the target!")
        
        if all(cell == HIT for row in board for cell in row):
            print(f"All your ships have been sunk, {user_name}!")
            break
        
# run game

if __name__ == "__main__":
    user_name = get_user_name()  # Get user name here
    game_loop(user_name)  # Pass user_name to game_loop