class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def make_move(self, position):
        if not (0 <= position <= 8):
            return False
        if self.board[position] == " ":
            self.board[position] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        # Check rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != " ":
                return self.board[i]

        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != " ":
                return self.board[i]

        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]

        if " " not in self.board:
            return "Tie"
        
        return None

    def display_board(self):
        print("\nCurrent board:")
        for i in range(0, 9, 3):
            print(f" {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ")
            if i < 6:
                print("-----------")

    def get_valid_moves(self):
        return [i for i, val in enumerate(self.board) if val == " "]

def main():
    game = TicTacToe()
    print("Welcome to Tic Tac Toe!")
    print("\nBoard positions are numbered as follows:")
    print(" 0 | 1 | 2 ")
    print("-----------")
    print(" 3 | 4 | 5 ")
    print("-----------")
    print(" 6 | 7 | 8 ")
    
    while True:
        game.display_board()
        print(f"\nPlayer {game.current_player}'s turn")
        print(f"Valid moves: {game.get_valid_moves()}")
        
        try:
            position = int(input(f"Enter position (0-8): "))
            if not game.make_move(position):
                print("\nInvalid move! Try again.")
                continue
                
            winner = game.check_winner()
            if winner:
                game.display_board()
                if winner == "Tie":
                    print("\nGame Over! It's a tie!")
                else:
                    print(f"\nGame Over! Player {winner} wins!")
                break
                
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\nPlease enter a valid number between 0-8")
            continue

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGame terminated by user. Thanks for playing!")