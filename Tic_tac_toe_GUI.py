import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import random

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe vs AI")
        self.root.resizable(False, False)
        
        # Game state variables
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.human_turn = True  # Flag to prevent clicks during AI's turn
        
        # Get player's choice of marker
        self.get_player_choice()
        
        # Create the AI player
        self.ai = AIPlayer(self.ai_marker)
        
        # Set up the GUI elements
        self.setup_gui()
        
        # AI goes first if it's X
        if self.ai_marker == 'X':
            self.root.after(500, self.ai_make_move)

    def get_player_choice(self):
        """Ask the player to choose X or O"""
        choice = simpledialog.askstring("Choose Marker", 
                                        "Do you want to play as X or O? (X goes first)",
                                        initialvalue="X")
        
        # Default to X if dialog is cancelled or input is invalid
        if choice is None or choice.upper() not in ['X', 'O']:
            choice = 'X'
        
        self.human_marker = choice.upper()
        self.ai_marker = 'O' if self.human_marker == 'X' else 'X'
        self.current_player = 'X'  # X always goes first

    def setup_gui(self):
        """Set up the game board and GUI elements"""
        # Frame for the game title
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=10)
        
        game_title = tk.Label(title_frame, text="Tic-Tac-Toe", font=('Arial', 20, 'bold'))
        game_title.pack()
        
        # Frame for player info
        info_frame = tk.Frame(self.root)
        info_frame.pack(pady=5)
        
        player_info = tk.Label(info_frame, 
                               text=f"You: {self.human_marker}  |  AI: {self.ai_marker}")
        player_info.pack()
        
        # Status label to show whose turn it is
        self.status_label = tk.Label(self.root, 
                                     text=f"Player {self.current_player}'s turn", 
                                     font=('Arial', 12))
        self.status_label.pack(pady=5)
        
        # Frame for the game board
        board_frame = tk.Frame(self.root)
        board_frame.pack(pady=10)
        
        # Create the 3x3 grid of buttons
        for row in range(3):
            for col in range(3):
                # Create a button for each cell
                self.buttons[row][col] = tk.Button(board_frame, 
                                                   text=' ', 
                                                   font=('Arial', 20, 'bold'),
                                                   width=5, height=2,
                                                   command=lambda r=row, c=col: self.make_move(r, c))
                self.buttons[row][col].grid(row=row, column=col, padx=2, pady=2)
        
        # Add a restart button
        restart_button = tk.Button(self.root, text="Restart Game", 
                                  command=self.restart_game)
        restart_button.pack(pady=10)

    def make_move(self, row, col):
        """Handle a player's move when they click a button"""
        # Check if the game is over or it's not the human's turn
        if self.game_over or not self.human_turn:
            return
        
        # Check if the cell is already occupied
        if self.board[row][col] != ' ':
            return
        
        # Make the move
        self.board[row][col] = self.human_marker
        self.buttons[row][col].config(text=self.human_marker)
        
        # Check for a winner or tie
        if self.check_game_over():
            return
        
        # Switch to AI's turn
        self.current_player = self.ai_marker
        self.status_label.config(text=f"Player {self.current_player}'s turn")
        self.human_turn = False
        
        # Let the AI make its move after a short delay
        self.root.after(500, self.ai_make_move)

    def ai_make_move(self):
        """Have the AI make its move"""
        # Get the best move from the AI
        row, col = self.ai.get_best_move(self)
        
        # Make the move
        self.board[row][col] = self.ai_marker
        self.buttons[row][col].config(text=self.ai_marker)
        
        # Check for a winner or tie
        if self.check_game_over():
            return
        
        # Switch back to human's turn
        self.current_player = self.human_marker
        self.status_label.config(text=f"Player {self.current_player}'s turn")
        self.human_turn = True

    def check_game_over(self):
        """Check if the game is over (win or tie)"""
        winner = self.check_winner()
        
        if winner:
            self.game_over = True
            if winner == 'Tie':
                messagebox.showinfo("Game Over", "It's a tie!")
            else:
                if winner == self.human_marker:
                    messagebox.showinfo("Game Over", "You win!")
                else:
                    messagebox.showinfo("Game Over", "AI wins!")
            return True
        
        return False

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

    def get_available_moves(self):
        """Return a list of all empty cells (available moves)"""
        moves = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    moves.append((row, col))
        return moves

    def restart_game(self):
        """Reset the game to start a new round"""
        # Reset the game state
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.current_player = 'X'  # X always goes first
        
        # Reset the GUI
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=' ')
        
        self.status_label.config(text=f"Player {self.current_player}'s turn")
        
        # Set human_turn based on marker selection
        self.human_turn = (self.human_marker == 'X')
        
        # AI goes first if it's X
        if self.ai_marker == 'X':
            self.root.after(500, self.ai_make_move)


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
        
        # If something went wrong, pick a random move (shouldn't happen with proper implementation)
        if best_move is None and game.get_available_moves():
            best_move = random.choice(game.get_available_moves())
                
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


def main():
    """Main function to run the game"""
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()


# Start the game if this script is run directly
if __name__ == "__main__":
    main()