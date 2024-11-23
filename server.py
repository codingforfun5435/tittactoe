import socket
import threading
import json
from queue import Queue
from game_logic import TicTacToe

class GameServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.waiting_players = Queue()
        self.games = {}
        print(f"Server started on port {port}")

    def start(self):
        while True:
            client, addr = self.server.accept()
            print(f"Connected to {addr}")
            threading.Thread(target=self.handle_queue, args=(client,)).start()

    def handle_queue(self, client):
        if self.waiting_players.empty():
            self.waiting_players.put(client)
            self.send_message(client, {"type": "wait", "message": "Waiting for opponent..."})
        else:
            player1 = self.waiting_players.get()
            player2 = client
            game_id = len(self.games)
            self.games[game_id] = TicTacToe()
            
            threading.Thread(target=self.handle_game, 
                           args=(game_id, player1, player2)).start()

    def handle_game(self, game_id, player1, player2):
        players = {player1: "X", player2: "O"}
        current_player = player1
        game = self.games[game_id]

        # Inform players about their symbols
        self.send_message(player1, {"type": "start", "symbol": "X"})
        self.send_message(player2, {"type": "start", "symbol": "O"})

        while True:
            try:
                # Send game state to both players
                state = {
                    "type": "state",
                    "board": game.board,
                    "current_player": game.current_player
                }
                self.send_message(player1, state)
                self.send_message(player2, state)

                if current_player == player1:
                    data = self.receive_message(player1)
                else:
                    data = self.receive_message(player2)

                if data["type"] == "move":
                    position = data["position"]
                    if game.make_move(position):
                        winner = game.check_winner()
                        if winner:
                            end_state = {
                                "type": "end",
                                "board": game.board,
                                "winner": winner
                            }
                            self.send_message(player1, end_state)
                            self.send_message(player2, end_state)
                            break
                        current_player = player2 if current_player == player1 else player1

            except:
                print(f"Game {game_id} ended unexpectedly")
                break

        del self.games[game_id]

    def send_message(self, client, message):
        client.send(json.dumps(message).encode())

    def receive_message(self, client):
        return json.loads(client.recv(1024).decode())

if __name__ == "__main__":
    server = GameServer()
    server.start()