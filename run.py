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
       print(' '.join([f"\033[94m{cell}\033[0m" if cell == SHIP else f"\033[91m{cell}\033[0m" if cell == HIT else f"\033[92m{cell}\033[0m" if cell == MISS else cell for cell in row]))
# added colors to the ships, hit, and miss


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
            if x >= 0 and x < BOARD_SIZE and y >= 0 and y < BOARD_SIZE and length > 0 and length <= 3:
                for i in range(length):
                    if x + i < len(board) and y < len(board[0]):
                        board[x + i][y] = SHIP
                print("Ship successfully placed.")
                display_board(board)  # Show the updated board
                break
            else:
                print("Invalid input. Please try again.")
        except ValueError:
            print("Invalid input. Please enter numbers.")

def random_ship_placement(board):
    ship_lengths = [3, 2, 1]
    for length in ship_lengths:
        while True:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            direction = random.choice(['horizontal', 'vertical'])
            
            if direction == 'horizontal':
                if x + length <= BOARD_SIZE:
                    for i in range(length):
                        if board[x + i][y] != SHIP:
                            board[x + i][y] = SHIP
                            break
                    else:
                        continue
            elif direction == 'vertical':
                 if y + length <= BOARD_SIZE:
                    for i in range(length):
                        if board[x][y + i] != SHIP:
                            board[x][y + i] = SHIP
                            break
                    else:
                        continue   
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
    ships_sunk = False  # Track if all ships have been sunk
    
    while not user_ships_placed or not cpu_ships_placed:
        if not user_ships_placed:
            print(f"{user_name}, please place your ships.")
            place_ship_by_user(board)
            user_ships_placed = True
        if not cpu_ships_placed:
            random_ship_placement(board)
            cpu_ships_placed = True

    while True:
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
            cpu_guess = (random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1))
            cpu_hit = board[cpu_guess[0]][cpu_guess[1]] == SHIP
            update_board(board, *cpu_guess, cpu_hit)
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

        
# run game

if __name__ == "__main__":
    user_name = get_user_name()  # Get user name here
    game_loop(user_name)  # Pass user_name to game_loop