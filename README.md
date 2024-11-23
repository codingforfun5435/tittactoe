# Multiplayer Tic Tac Toe

A simple online multiplayer Tic Tac Toe game with matchmaking queue.

## How to Play

1. First, start the server:
```bash
python server.py
```

2. Then, start two client instances in separate terminals:
```bash
python client.py
```

3. The game will automatically match two players when they connect.
4. Players take turns entering numbers 0-8 to make their moves.
5. The game continues until someone wins or it's a tie.

## Features

- Online multiplayer support
- Automatic matchmaking queue
- Real-time game updates
- Clean separation of game logic, client, and server code