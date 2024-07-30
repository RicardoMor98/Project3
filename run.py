import random

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