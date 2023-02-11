class Game:
    def __init__(self):
        # Current team to play a turn
        self.current_team = 'white'
        self.teams = ('white', 'black')
        self.moves = [None, None]
        self.game_over = False
        self.notation = {"a": 0, "b": 1, "c": 2,
                         "d": 3, "e": 4, "f": 5, "g": 6, "f": 7}
        # uppercase = white, lowercase = black
        self.board = [
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ]

    def get_board(self):
        return self.board

    def print_board(self):
        for row in self.board:
            for square in row:
                print(square, end=' ')
            print()

    def get_team_move(self):
        # Prompt the user for input
        start_input = input(
            "Enter the starting position of the piece to move (e.g. 'a2'): ")
        end_input = input(
            "Enter the ending position of the piece to move (e.g. 'a4'): ")

        # Validate the input
        if len(start_input) != 2 or len(end_input) != 2:
            print(
                "Invalid input. The input should be in algebraic notation the form of 'a2', 'b3', etc.")
            return self.get_team_move()

        # Chess notation to (row, col)
        start_row = int(start_input[1]) - 1
        start_col = self.notation[start_input[0]]
        end_row = int(end_input[1]) - 1
        end_col = self.notation[end_input[0]]

        if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
            print("Invalid input. The positions must be on the chessboard (a1 to h8).")
            return self.get_team_move()

        return (start_row, start_col), (end_row, end_col)

    def validate_move(self, current_team, start, end):
        # Converts the input to row and colum indices
        start_row, start_col = start[0], start[1]
        end_row, end_col = end[0], end[1]
        board = self.board

        print(start, end)
        # Checks if there is a chess piece
        piece = board[start_row][start_col]

        if piece == ' ':
            print("There is no piece at " + start + ".")
            return False

        if (piece.isupper() and end_row > start_row) or (piece.islower() and end_row < start_row):
            return False

        # Check that the player is moving their own piece
        piece = board[start[0]][start[1]]
        if current_team == 'white' and piece.isupper() or current_team == 'black' and piece.islower():
            return False

        # Pawn
        if piece.upper() == 'P':
            if start_col == end_col and board[end_row][end_col] != ' ':
                return False
            if start_col != end_col and board[end_row][end_col] == ' ':
                return False
            if abs(end_col - start_col) > 1:
                return False
            if abs(end_row - start_row) == 1 and board[end_row][end_col] == ' ':
                return False

        # Rook
        if piece.upper() == 'R':
            # Checks if the rook is moving either horizontally or vertically
            if start_row != end_row and start_col != end_col:
                return False

            # Checks if there are no pieces blocking the rook's path
            if start_row == end_row:
                # The rook is moving horizontally
                for col in range(min(start_col, end_col) + 1, max(start_col, end_col)):
                    if board[start_row][col] != ' ':
                        return False
            else:
                # The rook is moving vertically
                for row in range(min(start_row, end_row) + 1, max(start_row, end_row)):
                    if board[row][start_col] != ' ':
                        return False

        # Knight
        if piece.upper() == 'N':
            # Checks if the move is an L-shaped pattern
            row_diff = abs(end_row - start_row)
            col_diff = abs(end_col - start_col)
            if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
                return False

            # Checks if the destination square is either unoccupied or occupied by an opponent's piece
            if board[end_row][end_col] != ' ' and board[end_row][end_col].isupper() == board[start_row][start_col].isupper():
                return False

        # Bishop
        if piece.upper() == 'B':
            # Checks if the bishop is moving diagonally
            if abs(end_row - start_row) != abs(end_col - start_col):
                return False

            # Checks if there are no pieces blocking the bishop's path
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step

            while row != end_row and col != end_col:
                if board[row][col] != ' ':
                    return False

                row += row_step
                col += col_step

        # Queen
        if piece.upper() == 'Q':
            # Checks if the queen is moving horizontally, vertically, or diagonally
            if (start_row != end_row and start_col != end_col) and (abs(end_row - start_row) != abs(end_col - start_col)):
                return False

            # Checks if there are no pieces blocking the queen's path
            if start_row == end_row:
                # horizontal move
                col_step = 1 if end_col > start_col else -1
                col = start_col + col_step

                while col != end_col:
                    if board[start_row][col] != ' ':
                        return False
                    col += col_step
            elif start_col == end_col:
                # vertical move
                row_step = 1 if end_row > start_row else -1
                row = start_row + row_step

                while row != end_row:
                    if board[row][start_col] != ' ':
                        return False
                    row += row_step
            else:
                # diagonal move
                row_step = 1 if end_row > start_row else -1
                col_step = 1 if end_col > start_col else -1
                row, col = start_row + row_step, start_col + col_step

                while row != end_row and col != end_col:
                    if board[row][col] != ' ':
                        return False
                    row += row_step
                    col += col_step

            # Checks if the destination square is either unoccupied or occupied by an opponent's piece
            if board[end_row][end_col] != ' ' and board[end_row][end_col].isupper() == board[start_row][start_col].isupper():
                return False

        # King
        if piece.upper() == 'K':
            # Checks if the king is moving to an adjacent square
            row_diff = abs(end_row - start_row)
            col_diff = abs(end_col - start_col)
            if not (row_diff <= 1 and col_diff <= 1 and row_diff + col_diff != 0):
                return False

            # Checks if the destination square is either unoccupied or occupied by an opponent's piece
            if board[end_row][end_col] != ' ' and board[end_row][end_col].isupper() == board[start_row][start_col].isupper():
                return False

        return True

    # Moves the piece, updates the board
    # Parameters
    # board - self.board
    # player - "white" or "black"
    # start, end - each represents a (row, column) tuple (i.e. (1,0) = 'a2')
    def move_piece(self, board, current_team, start, end):
        # Converts the input to row and colum indices
        start_row, start_col = 8 - int(start[1]), ord(start[0]) - ord('a')
        end_row, end_col = 8 - int(end[1]), ord(end[0]) - ord('a')

        # Moves the piece if it's valid
        piece = board[start_row][start_col]

        board[end_row][end_col] = piece
        board[start_row][start_col] = ' '

    # Alternates the turn
    def switch_team_turn(self):
        self.current_team = self.teams[0] if self.current_team == self.teams[1] else self.teams[1]

    def is_in_check(self, board, player):
        # Find the location of the player's king
        for row in range(8):
            for col in range(8):
                if board[row][col] == ('K' if player == 'white' else 'k'):
                    king_row, king_col = row, col

        # Check if any of the opponent's pieces can attack the king
        opponent = 'black' if player == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != ' ' and piece.isupper() == (opponent == 'white'):
                    if self.validate_move(board, (row, col), (king_row, king_col)):
                        return True

        # If there's no opponent pieces can attack the king, the player is not in check
        return False

    def has_legal_moves(self, board, player):
        # Checks if any of the player's pieces have a legal move
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != ' ' and piece.isupper() == (player == 'white'):
                    for row2 in range(8):
                        for col2 in range(8):
                            if self.validate_move(board, (row, col), (row2, col2)):
                                return True

        # If no pieces have a legal move, the game is over
        return False

    def is_in_check(self, board, player):
        # Find the location of the player's king
        for row in range(8):
            for col in range(8):
                if board[row][col] == ('K' if player == 'white' else 'k'):
                    king_row, king_col = row, col

        # Check if any of the opponent's pieces can attack the king
        opponent = 'black' if player == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece != ' ' and piece.isupper() == (opponent == 'white'):
                    if self.validate_move(board, (row, col), (king_row, king_col)):
                        return True

        # If no opponent pieces can attack the king, the player is not in check
        return False

    def is_game_over(self, board, player):
        # Check if the current player is in check
        if self.is_in_check(board, player):
            # If the player is in check, check if there are any legal moves available
            if self.has_legal_moves(board, player):
                # If there are legal moves available, the game is not over
                return False
            else:
                # If there are no legal moves available, the game is in checkmate
                return True
        else:
            # If the player is not in check, check if there are any legal moves available
            if self.has_legal_moves(board, player):
                # If there are legal moves available, the game is not over
                return False
            else:
                # If there are no legal moves available, the game is in stalemate
                return True

    # Runs the game

    def run(self):
        while not self.game_over:
            # Prints the board and ask the current player for their move
            self.print_board()
            print(f"It is {self.current_team}'s team turn.")
            start, end = self.get_team_move()

            print(self.board)
            # Validates the move and updates the board if it is valid
            if self.validate_move(current_team=self.current_team, start=start, end=end):
                self.move_piece(
                    board=self.board, current_team=self.current_team, start=start, end=end)

                # Check if the game is over
                if self.is_game_over(self.board, self.current_team):
                    self.print_board()
                    print(f"The {self.current_team} team wins!")
                    game_over = True
                else:
                    # Alternate between players
                    self.switch_team_turn()
            else:
                print("Invalid move.")


game = Game()

game.run()
