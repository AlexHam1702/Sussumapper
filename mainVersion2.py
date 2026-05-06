import os  # operating system utilities (not heavily used here)
import sys  # system-specific parameters and functions
from enum import Enum  # enum base class for Player and GameMode
from typing import Optional, Tuple, List  # typing hints for readability
from copy import deepcopy  # for creating board copies during analysis
from colorama import Fore, Back, Style, init  # colorful terminal output support

# Initialize colorama for cross-platform color support
init(autoreset=True)  # automatically reset colors after each print

class Player(Enum):
    HUMAN = 1  # human player marker (X)
    AI = -1  # AI player marker (O)
    EMPTY = 0  # empty cell placeholder

class GameMode(Enum):
    HUMAN_VS_AI = 1  # one human versus the computer
    HUMAN_VS_HUMAN = 2  # two humans play locally
    AI_VS_AI = 3  # watch two AIs battle

class TicTacToe:
    def __init__(self, board_size: int = 5, win_count: int = 5):
        self.board_size = board_size  # size of the tic‑tac‑toe grid
        self.win_count = win_count  # how many in a row to win
        self.board = [[Player.EMPTY for _ in range(board_size)] for _ in range(board_size)]  # 2D board init
        self.ai_depth = 5  # default search depth for AI minimax
        self.history = []  # list of moves made (row, col, player)
    
    def display_board(self):
        """Display the current game board"""
        print("\n")
        for i, row in enumerate(self.board):
            print(f" {i} | ", end="")
            for j, cell in enumerate(row):
                if cell == Player.HUMAN:
                    print(f"{Fore.GREEN}X{Style.RESET_ALL}", end=" ")
                elif cell == Player.AI:
                    print(f"{Fore.RED}O{Style.RESET_ALL}", end=" ")
                else:
                    print(".", end=" ")
            print()
        print(f"{Fore.CYAN}    " + "-" * (self.board_size * 2 - 1))
        print("    ", end="")
        for j in range(self.board_size):
            print(j, end=" ")
        print(f"{Style.RESET_ALL}\n")
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if a move is valid"""
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row][col] == Player.EMPTY  # valid iff cell is empty and inside bounds
        return False
    
    def make_move(self, row: int, col: int, player: Player) -> bool:
        """Make a move on the board"""
        if self.is_valid_move(row, col):
            self.board[row][col] = player  # place the player's mark
            self.history.append((row, col, player))  # record move for replay/undo
            return True
        return False  # move was invalid
    
    def check_winner(self) -> Optional[Player]:
        """Check if there's a winner"""
        # Check rows
        for row in self.board:
            if all(cell == row[0] and cell != Player.EMPTY for cell in row):
                return row[0]  # horizontal win detected
        
        # Check columns
        for col in range(self.board_size):
            column = [self.board[row][col] for row in range(self.board_size)]
            if all(cell == column[0] and cell != Player.EMPTY for cell in column):
                return column[0]  # vertical win detected
        
        # Check diagonals
        diag1 = [self.board[i][i] for i in range(self.board_size)]
        if all(cell == diag1[0] and cell != Player.EMPTY for cell in diag1):
            return diag1[0]  # main diagonal win
        
        diag2 = [self.board[i][self.board_size - 1 - i] for i in range(self.board_size)]
        if all(cell == diag2[0] and cell != Player.EMPTY for cell in diag2):
            return diag2[0]  # anti‑diagonal win
        
        return None
    
    def is_board_full(self) -> bool:
        """Check if board is full"""
        return all(cell != Player.EMPTY for row in self.board for cell in row)  # true when no empty spaces remain
    
    def evaluate(self) -> int:
        """Evaluation function for game state"""
        winner = self.check_winner()
        if winner == Player.AI:
            return 100  # favorable board for AI
        elif winner == Player.HUMAN:
            return -100  # favorable board for human
        return 0  # neutral board
    
    def get_available_moves(self) -> List[Tuple[int, int]]:
        """Get all available moves"""
        moves = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == Player.EMPTY:
                    moves.append((i, j))
        return moves
    
    def minimax(self, depth: int, is_ai_turn: bool, alpha: int = -float('inf'), beta: int = float('inf')) -> Tuple[int, Optional[Tuple[int, int]]]:
        """Minimax algorithm with alpha-beta pruning"""
        winner = self.check_winner()  # terminal state check
        if winner == Player.AI:
            return 100 + depth, None  # deeper win is slightly preferred
        elif winner == Player.HUMAN:
            return -100 - depth, None  # deeper loss is slightly worse
        elif self.is_board_full():
            return 0, None  # draw
        elif depth == 0:
            return self.evaluate(), None  # heuristic at depth limit
        
        available_moves = self.get_available_moves()
        best_move = None
        
        if is_ai_turn:
            max_eval = -float('inf')
            for move in available_moves:
                self.board[move[0]][move[1]] = Player.AI
                eval_score, _ = self.minimax(depth - 1, False, alpha, beta)
                self.board[move[0]][move[1]] = Player.EMPTY
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in available_moves:
                self.board[move[0]][move[1]] = Player.HUMAN
                eval_score, _ = self.minimax(depth - 1, True, alpha, beta)
                self.board[move[0]][move[1]] = Player.EMPTY
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def get_best_ai_move(self) -> Optional[Tuple[int, int]]:
        """Get the best move for AI"""
        _, best_move = self.minimax(self.ai_depth, True)  # start minimax search for best AI move
        return best_move
    
    def show_winning_sequence(self, ai_wins: bool):
        """Display ideal winning sequence"""
        board_copy = deepcopy(self.board)
        sequence = []
        current_player = Player.AI if ai_wins else Player.HUMAN
        opponent = Player.HUMAN if ai_wins else Player.AI
        
        self.board = board_copy
        while not self.check_winner() and not self.is_board_full():
            if current_player == Player.AI:
                _, move = self.minimax(self.ai_depth, True)
            else:
                _, move = self.minimax(self.ai_depth, False)
            
            if move is None:
                break
            
            self.board[move[0]][move[1]] = current_player
            sequence.append((move, current_player))
            current_player, opponent = opponent, current_player
        
        self.board = board_copy
        return sequence
    
    def set_difficulty(self, depth: int):
        """Set AI difficulty level"""
        self.ai_depth = max(1, min(depth, 9))
        print(f"{Fore.YELLOW}Difficulty set to depth: {self.ai_depth}{Style.RESET_ALL}")
    
    def reset_game(self):
        """Reset the game board"""
        self.board = [[Player.EMPTY for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.history = []

import time

def play_game(mode: GameMode, game: TicTacToe):
    """Main game loop"""
    print(f"\n{Fore.CYAN}=== Game Started: {mode.name} ==={Style.RESET_ALL}")
    game.reset_game()
    
    while True:
        game.display_board()
        
        # 1. Check for Terminal State
        winner = game.check_winner()
        if winner:
            if winner == Player.AI:
                print(f"{Fore.RED}AI wins!{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}Player wins!{Style.RESET_ALL}")
            break
        
        if game.is_board_full():
            print(f"{Fore.YELLOW}It's a draw!{Style.RESET_ALL}")
            break
        
        # 2. Handle Game Modes
        if mode == GameMode.HUMAN_VS_AI:
            # Human Turn (X)
            print(f"{Fore.GREEN}Your turn (X):{Style.RESET_ALL}")
            while True:
                try:
                    row, col = map(int, input(f"Enter row and column (0-{game.board_size - 1}): ").split())
                    if game.make_move(row, col, Player.HUMAN):
                        break
                except:
                    print("Invalid input!")
            
            # AI Turn (O) - Only if game isn't over
            if not game.check_winner() and not game.is_board_full():
                move = game.get_best_ai_move()  # compute best move via minimax
                if move:
                    game.make_move(move[0], move[1], Player.AI)
                    print(f"{Fore.RED}AI plays at ({move[0]}, {move[1]}){Style.RESET_ALL}")

        elif mode == GameMode.HUMAN_VS_HUMAN:
            player = Player.HUMAN if len(game.history) % 2 == 0 else Player.AI
            symbol = "X" if player == Player.HUMAN else "O"
            color = Fore.GREEN if player == Player.HUMAN else Fore.RED
            print(f"{color}Player {symbol} turn:{Style.RESET_ALL}")
            while True:
                try:
                    row, col = map(int, input("Enter row and column (0-2): ").split())
                    if game.make_move(row, col, player):
                        break
                except:
                    print("Invalid input!")

        elif mode == GameMode.AI_VS_AI:
            # Determine which AI is moving based on history length
            # Even turns = AI 1 (acting as HUMAN/X), Odd turns = AI 2 (acting as AI/O)
            is_first_ai_turn = (len(game.history) % 2 == 0)  # alternate which AI acts as X or O
            current_player = Player.HUMAN if is_first_ai_turn else Player.AI
            
            symbol = 'X' if is_first_ai_turn else 'O'
            color = Fore.GREEN if is_first_ai_turn else Fore.RED
            print(f"{color}AI ({symbol}) is thinking...{Style.RESET_ALL}")
            time.sleep(1) # Slows down the spam so you can watch
            
            # We call minimax. For X, we want to minimize score; for O, we maximize.
            _, move = game.minimax(game.ai_depth, not is_first_ai_turn)
            
            if move:
                game.make_move(move[0], move[1], current_player)

def main():
    """Main program"""
    game = TicTacToe()
    
    while True:
        print(f"\n{Fore.CYAN}=== Tic Tac Terminal ===")
        print(f"Learn to play Tic Tac Toe with an unbeatable AI opponent!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Human vs AI")
        print(f"{Fore.YELLOW}2. Human vs Human")
        print(f"{Fore.RED}3. AI vs AI")
        print(f"{Fore.MAGENTA}4. Set Difficulty")
        print(f"{Fore.LIGHTRED_EX}5. Exit{Style.RESET_ALL}")
        
        choice = input("Select option: ")  # user selects game mode or action
        
        if choice == "1":
            play_game(GameMode.HUMAN_VS_AI, game)
        elif choice == "2":
            play_game(GameMode.HUMAN_VS_HUMAN, game)
        elif choice == "3":
            play_game(GameMode.AI_VS_AI, game)
        elif choice == "4":
            depth = int(input("Enter depth (1-9): "))
            game.set_difficulty(depth)
        elif choice == "5":
            break

if __name__ == "__main__":
    main()