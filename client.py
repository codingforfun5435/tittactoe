import socket
import json
import threading
import sys
from game_logic import TicTacToe

class GameClient:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.game = TicTacToe()
        self.symbol = None
        
    def start(self):
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = json.loads(self.client.recv(1024).decode())
                
                if message["type"] == "wait":
                    print(message["message"])
                
                elif message["type"] == "start":
                    self.symbol = message["symbol"]
                    print(f"Game starting! You are player {self.symbol}")
                
                elif message["type"] == "state":
                    self.game.board = message["board"]
                    self.game.current_player = message["current_player"]
                    self.display_game()
                    
                    if message["current_player"] == self.symbol:
                        self.make_move()
                
                elif message["type"] == "end":
                    self.game.board = message["board"]
                    self.display_game()
                    if message["winner"] == "Tie":
                        print("Game Over! It's a tie!")
                    else:
                        print(f"Game Over! Player {message['winner']} wins!")
                    sys.exit()

            except:
                print("Connection lost")
                break

    def make_move(self):
        while True:
            try:
                position = int(input("Enter position (0-8): "))
                if 0 <= position <= 8:
                    self.send_message({
                        "type": "move",
                        "position": position
                    })
                    break
                else:
                    print("Position must be between 0 and 8")
            except ValueError:
                print("Please enter a valid number")

    def display_game(self):
        self.game.display_board()
        print(f"Current player: {self.game.current_player}")

    def send_message(self, message):
        self.client.send(json.dumps(message).encode())

if __name__ == "__main__":
    client = GameClient()
    client.start()