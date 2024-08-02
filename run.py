import random

class Board:
    def __init__(self):
        # Initialize the game board with default settings and parameters
        self.board_size = 7
        self.ship_size = 5
        self.player_board = [
            [" " for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        self.computer_board = [
            [" " for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        self.player_turns = 15
        self.computer_turns = 15
        self.player_ships = 5  # Track remaining ships for each player
        self.computer_ships = 5
        self.player_score = 0  # Track the player's score
        self.computer_score = 0  # Track the computer's score


     def get_username(self):
        input_is_valid = False
        username = ""
        while input_is_valid is False:
            user_input = input("Enter your username: ")
            if len(user_input) < 3:
                print("Please enter a minimum of 3 chars")
            else:
                input_is_valid = True
                username = user_input
        return username

    def display_board(self, board, is_player=True):
        # Display the game board, including player's and computer's boards
        print("   0 1 2 3 4 5 6")
        for i, row in enumerate(board):
            if not is_player:
                # If it's the computer's board, hide the ships
                row = [" " if cell == "S" else cell for cell in row]
            print(f"{i} |{'|'.join(row)}|")

    def place_ships(self, board, ships):
        # Randomly place ships on the board, ensuring no overlap
        for _ in range(ships):
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            while board[row][col] == "S":
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
            board[row][col] = "S"

     def validate_input(self, row, col):
        # Check if the input coordinates are within the valid range
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    def make_shot(self, board, row, col, player):
        # Process player's or computer's shot on the board & update accordingly
        if board[row][col] == "S":
            print(f"\n{player} Sunk a Battleship!")
            board[row][col] = "H"
            return True
        else:
            print(f"\n{player} Shot in the ocean!")
            board[row][col] = "M"
            return False

    def display_instructions(self):
        # Display comprehensive game instructions and information
        print("Welcome to the Battleship game!\n"
        "Your main objective is to find and destroy all the hidden ships on the map!\n")
        print("How to play:")
        print("1. The game consists of two boards, one for each player.")
        print("2. The boards marked with the numbers 0 - 6.")
        print("3. You have a total of 15 turns to sink 5 hidden ships.")
        print("4. Guess a row and a column between 0 and 6.")
        print("5. If you HIT a ship, you will see 'H'.")
        print("6. If you MISS a ship, you will see 'M'.")
        print("7. Your ships are displayed as 'S'.")
        print("8. Type 'exit' to quit the game at any time.")
        print("\nI wish you good fortune in wars to come!\n")

def play_game(self):
        # Main game loop where players take turns and outcomes are determined
        while True:
            self.display_instructions()
            player_name = self.get_username()

            self.place_ships(self.player_board, self.player_ships)
            self.place_ships(self.computer_board, self.computer_ships)

            player_guessed_coordinates = set()
            computer_guessed_coordinates = set()

            while (
                self.player_turns > 0
                and self.computer_turns > 0
                and self.player_ships > 0
                and self.computer_ships > 0
            ):
                print(f"\n{player_name}'s Board:")
                self.display_board(self.player_board)
                print("\nCPU's Board:")
                self.display_board(self.computer_board, False)
    