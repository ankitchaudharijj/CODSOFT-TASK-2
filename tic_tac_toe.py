import random
import time


class TicTacToe:
    def __init__(self):
        # Initialize empty 3x3 board (represented as a list of lists)
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always goes first
        
    def print_board(self):
        """Display the current state of the board in a readable format"""
        print("\n")
        # Print column indices at the top
        print("  0 1 2")
        for row_idx, row in enumerate(self.board):
            # Print row index followed by row contents
            print(f"{row_idx} {row[0]}|{row[1]}|{row[2]}")
            # Print horizontal divider (except after the last row)
            if row_idx < 2:
                print("  -+-+-")
        print("\n")
    
    def is_valid_move(self, row, col):
        """Check if a move is valid (within bounds and the cell is empty)"""
        # Check if indices are within the board bounds
        if not (0 <= row < 3 and 0 <= col < 3):
            return False
        # Check if the selected cell is empty
        return self.board[row][col] == ' '
    
    def make_move(self, row, col, player):
        """Place a player's marker on the board"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def get_available_moves(self):
        """Return a list of all empty cells (available moves)"""
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    moves.append((row, col))
        return moves
    
    def check_winner(self):
        """Check if there's a winner or a tie"""
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] and 
                self.board[0][col] != ' '):
                return self.board[0][col]
        
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] and 
            self.board[0][0] != ' '):
            return self.board[0][0]
        
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] and 
            self.board[0][2] != ' '):
            return self.board[0][2]
        
        # Check for tie (board full with no winner)
        if all(self.board[row][col] != ' ' for row in range(3) for col in range(3)):
            return 'Tie'
        
        # Game is still ongoing
        return None
    
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 'O' if self.current_player == 'X' else 'X'


class AIPlayer:
    def __init__(self, marker):
        self.marker = marker  # 'X' or 'O'
        # Opponent's marker
        self.opponent_marker = 'O' if marker == 'X' else 'X'
    
    def get_best_move(self, game):
        """Find the best move using the Minimax algorithm"""
        best_score = float('-inf')
        best_move = None
        
        # Try all possible moves and pick the one with the highest score
        for move in game.get_available_moves():
            row, col = move
            # Temporarily make the move
            game.board[row][col] = self.marker
            
            # Calculate score for this move using minimax
            score = self.minimax(game, 0, False)
            
            # Undo the move
            game.board[row][col] = ' '
            
            # Update best move if this move has a higher score
            if score > best_score:
                best_score = score
                best_move = move
                
        return best_move
    
    def minimax(self, game, depth, is_maximizing):
        """
        Minimax algorithm implementation
        - game: current game state
        - depth: current depth in the game tree
        - is_maximizing: whether it's the maximizing player's turn
        """
        # Check for terminal state (win/lose/tie)
        result = game.check_winner()
        if result is not None:
            # Return score based on outcome
            if result == self.marker:
                return 10 - depth  # Win (prefer quicker wins)
            elif result == self.opponent_marker:
                return depth - 10  # Loss (prefer longer losses)
            else:
                return 0  # Tie
        
        # Maximizing player's turn (AI)
        if is_maximizing:
            best_score = float('-inf')
            for move in game.get_available_moves():
                row, col = move
                # Try this move
                game.board[row][col] = self.marker
                # Recursively check score for this path
                score = self.minimax(game, depth + 1, False)
                # Undo the move
                game.board[row][col] = ' '
                # Update best score
                best_score = max(score, best_score)
            return best_score
        
        # Minimizing player's turn (opponent)
        else:
            best_score = float('inf')
            for move in game.get_available_moves():
                row, col = move
                # Try this move
                game.board[row][col] = self.opponent_marker
                # Recursively check score for this path
                score = self.minimax(game, depth + 1, True)
                # Undo the move
                game.board[row][col] = ' '
                # Update best score
                best_score = min(score, best_score)
            return best_score


def play_game():
    """Main function to run the game"""
    game = TicTacToe()
    
    # Let player choose their marker
    player_choice = ''
    while player_choice not in ['X', 'O']:
        player_choice = input("Do you want to play as X or O? (X goes first): ").upper()
    
    human_marker = player_choice
    ai_marker = 'O' if human_marker == 'X' else 'X'
    ai = AIPlayer(ai_marker)
    
    print("\nGame started! You are playing as", human_marker)
    print("Enter your move as row column (e.g., '1 2')")
    
    # Main game loop
    while True:
        game.print_board()
        
        # Check for winner before each turn
        winner = game.check_winner()
        if winner:
            if winner == 'Tie':
                print("It's a tie!")
            else:
                print(f"Player {winner} wins!")
            break
        
        # Current player's turn
        if game.current_player == human_marker:
            # Human player's turn
            valid_move = False
            while not valid_move:
                try:
                    move = input(f"Your turn ({human_marker}). Enter row col: ")
                    row, col = map(int, move.split())
                    valid_move = game.make_move(row, col, human_marker)
                    if not valid_move:
                        print("Invalid move. Try again.")
                except (ValueError, IndexError):
                    print("Please enter valid row and column numbers (0-2).")
        else:
            # AI player's turn
            print(f"AI's turn ({ai_marker}). Thinking...")
            # Add a small delay to make it seem like the AI is "thinking"
            time.sleep(0.5)
            row, col = ai.get_best_move(game)
            game.make_move(row, col, ai_marker)
            print(f"AI plays at position ({row}, {col})")
        
        # Switch to the other player
        game.switch_player()
    
    # Show final board state
    game.print_board()
    
    # Ask if player wants to play again
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again.startswith('y'):
        play_game()
    else:
        print("Thanks for playing!")


# Start the game if this script is run directly
if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe!")
    print("Can you beat the AI?")
    play_game()