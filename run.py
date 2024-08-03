import random


class Game:
    """Class representing the Battleship game."""

    def __init__(self):
        """Initialize the game with the board size, number of ships,
        player/computer boards, turns, and hits."""
        self.size = 7  # Board size (7x7)
        self.ships = 5  # Number of ships per player
        self.p_board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.c_board = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.p_turns = 15  # Player's available turns
        self.c_turns = 15  # Computer's available turns
        self.p_hits = 0  # Player's hits
        self.c_hits = 0  # Computer's hits

    def get_name(self):
        """Prompt the player to input their name with at least 3 characters."""
        while True:
            name = input('Enter your name: ')
            if len(name) >= 3:
                return name
            print('Name must be at least 3 characters.')

    def show_board(self, board, hide_ships=False):
        """Display the game board. Optionally hide the ships."""
        print('   ' + ' '.join(map(str, range(self.size))))  # Column headers
        for i, row in enumerate(board):
            display_row = [
                ' ' if hide_ships and cell == 'S' else cell for cell in row
            ]
            print(f'{i} |' + '|'.join(display_row) + '|')  # Print row

    def place_ships(self, board):
        """Randomly place ships on the board."""
        for _ in range(self.ships):
            r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while board[r][c] == 'S':
                r, c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            board[r][c] = 'S'

    def is_valid(self, r, c):
        """Check if coordinates are within board bounds."""
        return 0 <= r < self.size and 0 <= c < self.size

    def fire(self, board, r, c, player):
        """Handle firing at a position. Return True if a ship is hit."""
        if board[r][c] == 'S':
            print(f'{player} hit a ship!')
            board[r][c] = 'H'
            return True
        print(f'{player} missed.')
        board[r][c] = 'M'
        return False

    def play(self):
        """Main game loop where players take turns."""
        print('Welcome to Battleship!')
        print('Your objective is to sink all ships!')
        print('1. The game consists of two boards (7x7).')
        print('2. You have 15 turns to sink 5 ships.')
        print('3. Guess a row and column (0-6).')
        print('4. "H" for hit, "M" for miss.')
        print('5. Type "exit" to quit the game.')
        print('\nGood luck!\n')

        name = self.get_name()
        self.place_ships(self.p_board)
        self.place_ships(self.c_board)

        p_guesses = set()
        c_guesses = set()

        while (
            self.p_turns > 0
            and self.c_turns > 0
            and self.p_hits < self.ships
            and self.c_hits < self.ships
        ):
            print(f'\n{name}\'s Board:')
            self.show_board(self.p_board)
            print('\nCPU\'s Board:')
            self.show_board(self.c_board, hide_ships=True)

            while True:
                try:
                    r = input('Enter row (0-6) or "exit" to quit: ')
                    if r.lower() == 'exit':
                        self.end_game(name)
                        return
                    r = int(r)
                    c = int(input('Enter column (0-6): '))
                    if not self.is_valid(r, c) or (r, c) in p_guesses:
                        print('Invalid or repeated guess. Try again.')
                        continue

                    p_guesses.add((r, c))
                    if self.fire(self.c_board, r, c, name):
                        self.p_hits += 1
                    break
                except ValueError:
                    print('Enter valid numbers.')

            c_r, c_c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            while (c_r, c_c) in c_guesses:
                c_r, c_c = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            c_guesses.add((c_r, c_c))

            if self.fire(self.p_board, c_r, c_c, 'CPU'):
                self.c_hits += 1

            self.p_turns -= 1
            self.c_turns -= 1

            print(f'\nTurns left: {self.p_turns} | {name}\'s hits: {self.p_hits} | CPU\'s hits: {self.c_hits}')

        self.end_game(name)

    def end_game(self, name):
        """Display the final boards and announce the result."""
        print('\nGame Over!')
        self.show_board(self.p_board)
        self.show_board(self.c_board)

        if self.p_hits > self.c_hits:
            print(f'\nCongrats, {name}! You sank all the CPU\'s ships!')
        elif self.c_hits > self.p_hits:
            print('\nCPU sank all your ships. Better luck next time!')
        else:
            print('\nIt\'s a draw!')

        if input('\nPlay again? (yes/no): ').lower() == 'yes':
            self.__init__()
            self.play()


if __name__ == '__main__':
    Game().play()
