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

    def cpu_guess(self):
        return random.randrange(BOARD_SIZE), random.randrange(BOARD_SIZE)

    def user_guess(self, username):
        row, column = self.get_user_input(username)
        if self.check_valid_move(row, column, self.game_board):
            if [row, column] in self.create_random_ships(INIT_SHIPS):
                print(f"{username}, Boom! You hit! A ship has exploded! You were granted a new ammo!\n")
                self.cpu_board[row][column] = "X"
                self.ships_left -= 1
                if self.ships_left == 0:
                    print(f"{username}, Congrats, you won!")
                    self.play_again(username)
            else:
                print(f"{username}, You missed!\n")
                self.cpu_board[row][column] = "-"
                self.user_ammo -= 1
            print(f"Ammo left: {self.user_ammo}")
            print(f"Ships left: {self.ships_left}")
            self.display_board(self.cpu_board, is_player=False, label="CPU's Board:")
        else:
            print("Invalid move. Try again.")

    def cpu_action(self, username):
        row, column = self.cpu_guess()
        if self.cpu_board[row][column] == "X" or self.cpu_board[row][column] == "-":
            print("\nCPU has already shot that place!\n")
            self.user_guess(username)
        elif [row, column] in self.create_random_ships(INIT_SHIPS):
            print(f"\nCPU hit! A ship has exploded!\n")
            self.game_board[row][column] = "X"
            self.ships_left -= 1
            if self.ships_left == 0:
                print("CPU won!")
                self.play_again(username)
        else:
            print(f"\nCPU missed!\n")
            self.game_board[row][column] = "-"
            self.cpu_ammo -= 1
        print(f"Ammo left: {self.cpu_ammo}")
        print(f"Ships left: {self.ships_left}")
        self.display_board(self.game_board, is_player=True, label=f"{username}'s Board:")

    def play_game(self, username):
        self.place_ships(self.game_board, INIT_SHIPS)
        print(Message.instructions.format(user_ammo=self.user_ammo, INIT_SHIPS=self.ships_left))
        print("User's Board:")
        self.display_board(self.game_board)
        print("\nCPU's Board:")
        self.display_board(self.cpu_board, is_player=False)
        
        while self.user_ammo > 0 and self.cpu_ammo > 0:
            if self.turn == 'user':
                self.user_guess(username)
            else:
                self.cpu_action(username)
            self.turn = 'user' if self.turn == 'cpu' else 'cpu'
            
            # Check if the current player has run out of ammo or ships
            if self.user_ammo <= 0 or self.cpu_ammo <= 0 or self.ships_left <= 0:
                break
            
            # Prompt the player to continue, restart, or quit after both players have taken their turns
            continue_playing = "C"
            if self.turn == 'user':
                continue_playing = input("Do you want to continue playing? <C>ontinue, <R>estart, or <Q>uit? >: ").upper()
            if continue_playing == "Q":
                self.__init__()
                username = self.get_username()
                self.play_game(username)
            elif continue_playing == "R":
                self.__init__()
                self.play_game(username)  # Restart the game

        # Determine game outcome
        if self.ships_left == self.cpu_board.count("X"):
            print("It's a tie!")
        elif self.ships_left < self.cpu_board.count("X"):
            print(f"{username}, Congratulations, you won!")
        else:
            print("CPU won!")

        # Ask to play again or quit
        self.play_again(username)

    def play_again(self, username):
        try_again = input(f"Do you want to play again? <Y>es or <N>o? >: ").lower()
        if try_again == "y":
            self.__init__()
            self.play_game(username)
        else:
            print(f"Goodbye, {username}!")

if __name__ == "__main__":
    game = BattleshipGame()
    username = game.get_username()
    game.play_game(username)
