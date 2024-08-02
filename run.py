import random

# the game board as 2D list
# Constants
BOARD_SIZE = 5
INIT_SHIPS = 3
INIT_AMMO = 10

# Global Variables
ammo = INIT_AMMO
ships_left = INIT_SHIPS
turn = 'user'

# This class defines two static string variables, welcome and instructions, which are used to greet the player and provide game instructions.
class Message:
    welcome = ("Welcome to the Battleship game!\n"
               "Your main objective is to find and destroy all the hidden ships on map!\n")
    instructions = ("\nIntroductions:\n"
                     f"You have {INIT_AMMO} ammo and there are {INIT_SHIPS} hidden ships on map.\n"
                     "In order to hit them, you have to enter specific numbers for that location. For example:\n"
                     "For the first row and first column, you have to write 1 and 1.\n"
                     "I wish you good fortune in wars to come!\n")


# Prompts the user for their name at the start of the game.
def get_username():
    """
    Function getting username for welcome message
    """
    while True:
        user_name = input(Message.welcome + "\nEnter your name: ")
        if user_name:
            print(f"Welcome to the Battleship game, {user_name}!")
            return user_name
        else:
            print("Please enter your name.")


# Generates random coordinates for placing ships on the board.
def create_random_ships(num_ships):
    ship_coordinates = [[random.randrange(BOARD_SIZE), random.randrange(BOARD_SIZE)] for _ in range(num_ships)]
    return ship_coordinates

# Prints the current state of the game board to the console.
def display_board(board):
    for row in board:
        print(' '.join(row))


# Captures the user's guess for a ship's location.
def get_user_input(username):
    while True:
        try:
            row = int(input(f"{username}, Enter a row number between 1-{BOARD_SIZE}: ")) - 1
            column = int(input(f"{username}, Enter a column number between 1-{BOARD_SIZE}: ")) - 1
            if row >= 0 and row < BOARD_SIZE and column >= 0 and column < BOARD_SIZE:
                return row, column
            else:
                raise ValueError("Row or Column is out of bounds.")
        except ValueError as ve:
            print("Invalid input. Please enter numbers within the board size.", ve)


# Validates whether a move is valid (within the board boundaries and not previously guessed).
def check_valid_move(row, column, game_board):
    if (game_board[row][column] != "X") and (game_board[row][column] != "-"):
        return True
    else:
        print("You have already shot that place!")
        return False


# Randomly selects a cell on the board for the CPU's guess.
def cpu_guess():
    """
    Generates a random row and column for the CPU's guess.
    """
    return random.randrange(BOARD_SIZE), random.randrange(BOARD_SIZE)

    print("Goodbye.")
    
# Orchestrates the game flow, including initializing the game board, placing ships, and managing turns between the user and the CPU.
def play_game(username):
    global ammo, ships_left, turn
    turn = 'user'
    game_board = [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    cpu_board = [['O'] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    ship_coordinates = create_random_ships(INIT_SHIPS)
    ships_left = INIT_SHIPS

    print(Message.instructions.format(INIT_AMMO=ammo, INIT_SHIPS=ships_left))
    
    display_board(game_board)

    while ammo > 0:
        if turn == 'user':
            row, column = get_user_input(username)
            if row is None:
                continue
            if check_valid_move(row, column, game_board):
                if [row, column] in ship_coordinates:
                    print(f"{username}, Boom! You hit! A ship has exploded! You were granted a new ammo!\n")
                    game_board[row][column] = "X"
                    ships_left -= 1
                    if ships_left == 0:
                        print(f"{username}, Congrats, you won!")
                        play_again(username)
                else:
                    print(f"{username}, You missed!\n")
                    game_board[row][column] = "-"
                    ammo -= 1
                print(f"Ammo left: {ammo}")
                print(f"Ships left: {ships_left}")
                display_board(game_board)
                display_board(cpu_board)
                turn = 'cpu'
        else:
            row, column = cpu_guess()
            if cpu_board[row][column] == "X" or cpu_board[row][column] == "-":
                print("\nCPU has already shot that place!\n")
                turn = 'user'
                continue
            elif [row, column] in ship_coordinates:
                print(f"\nCPU hit! A ship has exploded!\n")
                cpu_board[row][column] = "X"
                ships_left -= 1
                if ships_left == 0:
                    print("CPU won!")
                    play_again(username)
            else:
                print(f"\nCPU missed!\n")
                cpu_board[row][column] = "-"
                ammo -= 1
            print(f"Ammo left: {ammo}")
            print(f"Ships left: {ships_left}")
            display_board(game_board)
            display_board(cpu_board)
            turn = 'user'

# Determine game outcome
    if ships_left == cpu_board.count("X"):
        print("It's a tie!")
    elif ships_left < cpu_board.count("X"):
        print(f"{username}, Congratulations, you won!")
    else:
        print("CPU won!")

    # Ask to play again or quit
    play_again(username)
