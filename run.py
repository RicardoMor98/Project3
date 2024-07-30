import random

# user name imput

def get_user_name():
    return input("Please enter your name: ")

user_name = get_user_name()
print(f"Welcome {user_name} to Battleship!")

# the game board as 2D list

BOARD_SIZE = 10
EMPTY = '.'
SHIP = 'S'
HIT = 'X'
MISS = 'O'

# initialize the board

board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# placing the ships

def place_ship(board, x, y, length):
    for i in range(length):
        if x+i < BOARD_SIZE:
            board[x+i][y] = SHIP

def random_ship_placement(board):
    import random
    for _ in range(5):  # Max 5 ships
        length = random.randint(1, 3)  # Max length 3
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)
        place_ship(board, x, y, length)

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
    user_name = get_user_name()
    game_loop(user_name)