import math

# Class to handle the game logic and board management
class TicTacToe:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 'X'

    @staticmethod
    def initialize_board():
        return [[' ' for _ in range(3)] for _ in range(3)]

    def print_board(self):
        for row in self.board:
            print("|".join(row))
            print("-" * 5)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
        else:
            raise ValueError("The cell is already occupied.")

    def check_winner(self, player):
        # Check rows, columns, and diagonals
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([self.board[row][col] == player for row in range(3)]):
                return True
        if all([self.board[i][i] == player for i in range(3)]) or all([self.board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    def is_draw(self):
        return all([cell != ' ' for row in self.board for cell in row])

    def get_available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def is_game_over(self):
        return self.check_winner('X') or self.check_winner('O') or self.is_draw()

# Class to handle AI logic using Minimax with Alpha-Beta Pruning
class AI:
    def get_best_move(self, board):
        best_move = None
        best_value = -math.inf
        for (i, j) in self.get_available_moves(board):
            board[i][j] = 'O'
            move_value = self.minimax(board, 0, False)
            board[i][j] = ' '
            if move_value > best_value:
                best_value = move_value
                best_move = (i, j)
        return best_move

    def minimax(self, board, depth, is_maximizing, alpha=-math.inf, beta=math.inf):
        if self.check_winner(board, 'O'):
            return 1
        if self.check_winner(board, 'X'):
            return -1
        if self.is_draw(board):
            return 0

        if is_maximizing:
            max_eval = -math.inf
            for (i, j) in self.get_available_moves(board):
                board[i][j] = 'O'
                eval = self.minimax(board, depth + 1, False, alpha, beta)
                board[i][j] = ' '
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for (i, j) in self.get_available_moves(board):
                board[i][j] = 'X'
                eval = self.minimax(board, depth + 1, True, alpha, beta)
                board[i][j] = ' '
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    @staticmethod
    def check_winner(board, player):
        # Check rows, columns, and diagonals
        for row in board:
            if all([cell == player for cell in row]):
                return True
        for col in range(3):
            if all([board[row][col] == player for row in range(3)]):
                return True
        if all([board[i][i] == player for i in range(3)]) or all([board[i][2 - i] == player for i in range(3)]):
            return True
        return False

    @staticmethod
    def is_draw(board):
        return all([cell != ' ' for row in board for cell in row])

    @staticmethod
    def get_available_moves(board):
        return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']

# Main function to run the game
def main():
    game = TicTacToe()
    ai = AI()

    print("Welcome to Tic-Tac-Toe!")
    print("You are 'X' and the AI is 'O'.")
    game.print_board()

    while not game.is_game_over():
        if game.current_player == 'X':
            row, col = get_human_move(game)
            game.make_move(row, col)
        else:
            print("AI's turn (O):")
            row, col = ai.get_best_move(game.board)
            game.make_move(row, col)

        game.print_board()

        if game.check_winner('X'):
            print("Congratulations! You win!")
            return
        elif game.check_winner('O'):
            print("AI wins! Better luck next time.")
            return
        elif game.is_draw():
            print("It's a draw!")
            return

def get_human_move(game):
    while True:
        try:
            row, col = map(int, input("Enter row and column (0, 1, or 2): ").split())
            if (row, col) in game.get_available_moves():
                return row, col
            else:
                print("Invalid move. The cell is already occupied or out of bounds.")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")

if __name__ == "__main__":
    main()
