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