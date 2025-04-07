class ChessPiece:
    def __init__(self, color, symbol):
        self.color = color  # 'white' or 'black'
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def is_valid_move(self, board, start, end):
        """Check if the move is valid for this piece (simplified)."""
        return True


class ChessBoard:
    def __init__(self):
        self.board = self.initialize_board()
        self.move_count = 0

    def initialize_board(self):
        """Create the initial setup of the chessboard."""
        empty_row = [None] * 8
        board = [empty_row[:] for _ in range(8)]

        # Pawns
        for i in range(8):
            board[1][i] = ChessPiece('black', 'p')
            board[6][i] = ChessPiece('white', 'P')

        # Rooks
        board[0][0] = board[0][7] = ChessPiece('black', 'r')
        board[7][0] = board[7][7] = ChessPiece('white', 'R')

        # Knights
        board[0][1] = board[0][6] = ChessPiece('black', 'n')
        board[7][1] = board[7][6] = ChessPiece('white', 'N')

        # Bishops
        board[0][2] = board[0][5] = ChessPiece('black', 'b')
        board[7][2] = board[7][5] = ChessPiece('white', 'B')

        # Queens
        board[0][3] = ChessPiece('black', 'q')
        board[7][3] = ChessPiece('white', 'Q')

        # Kings
        board[0][4] = ChessPiece('black', 'k')
        board[7][4] = ChessPiece('white', 'K')

        return board

    def display(self):
        """Display the board in text format."""
        print("  a b c d e f g h")
        for row_index, row in enumerate(self.board):
            print(8 - row_index, end=" ")
            for cell in row:
                print(cell.symbol if cell else '.', end=" ")
            print()
        print()

    def move_piece(self, start, end):
        """Move a piece if the move is valid."""
        start_row, start_col = start
        end_row, end_col = end
        piece = self.board[start_row][start_col]

        if not piece:
            print("No piece at the starting position.")
            return False
        if not piece.is_valid_move(self.board, start, end):
            print("Invalid move for this piece.")
            return False

        target_piece = self.board[end_row][end_col]
        if target_piece and target_piece.color == piece.color:
            print("Cannot capture your own piece.")
            return False

        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None
        self.move_count += 1
        return True


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.current_turn = 'white'

    def parse_position(self, position):
        """Convert chess notation (e.g., 'e2') into board indices."""
        if len(position) != 2 or position[0] not in 'abcdefgh' or position[1] not in '12345678':
            return None
        col = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return row, col

    def play(self):
        while True:
            self.board.display()
            print(f"Ход {'Белых' if self.current_turn == 'white' else 'Черных'}")

            start = input("Введите позицию фигуры для хода (например, e2): ")
            start = self.parse_position(start)
            if not start:
                print("Неверный ввод. Попробуйте снова.")
                continue

            end = input("Введите целевую позицию (например, e4): ")
            end = self.parse_position(end)
            if not end:
                print("Неверный ввод. Попробуйте снова.")
                continue

            if self.board.move_piece(start, end):
                self.current_turn = 'black' if self.current_turn == 'white' else 'white'


if __name__ == "__main__":
    game = ChessGame()
    game.play()

