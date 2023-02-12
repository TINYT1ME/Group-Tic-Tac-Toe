# Libraries
import socket 
import json
import time
import select
import threading
from random import randint
import time

# Server info
HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Game Board
game_board = [
    ["","",""],
    ["","",""],
    ["","",""]
]

# All connected players
all_players = []

# Dictionary that holds position and # of times that pos was entered
voting = {}

team_to_symb = {
    0: "X",
    1: "O"
}

# Update board
def update_board(team):
    global game_board

    # If dictionary empty
    if not voting:
        game_board[randint(0, 2)][randint(0, 2)] = team_to_symb[team]
    else:
        points = max(voting, key=voting.get)
        game_board[points[1]][points[0]] = team_to_symb[team]

def check_valid(x_value, y_value):
    if (
        (
            int(x_value) >= 0 and
            int(x_value) <= 2
        ) and
        (
            int(y_value) >= 0 and
            int(y_value) <= 2
        )
    ):
        return True
    else:
        return False

# Client handling, new thread per client
def handle_connection(conn):
    global voting
    x_value = None
    y_value = None
    while x_value == None:
        data = conn.recv(HEADER)
        data = json.loads(data.decode())
        x_value = data.get("x")
        y_value = data.get("y")
        if not check_valid(x_value, y_value):
            x_value = None
            data_out = json.dumps({"msg": f"Invalid move plz choose again: ", "prompt": True})
            conn.send(data_out.encode())
        else:
            pos = [x_value, y_value]

            # Adding to voting dictionary
            if (x_value, y_value) in voting:
                voting[(x_value, y_value)] += 1
            else:
                voting[(x_value, y_value)] = 1
            print(voting)
            print(f"\n[CLIENT DATA] {conn} entered: x={x_value}, y={y_value}\n")
    
def countdown(num):
    for i in range(num, 0, -1):
        print("\r", end = '')
        print(i, end='')
        time.sleep(1)

# Server start function
def start():
    global voting
    # TEAM 0 IS X, TEAM 1 is O
    team = 0

    # Server Listening
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}\n")

    # Give 60 seconds at beginning for clients to connect
    t_end = time.time() + 10
    print("[CONNECTIONS] Beginning connections (60 sec)")

    timer = threading.Thread(target=countdown, args=(59,))
    timer.start()
    # Checking for new clients, loop
    while time.time() < t_end:
        team = (team + 1) % 2   # Alternates 0 and 1
        
        conn, addr = server.accept()
        conn.send

        # When client connects, send out team info
        data_out = json.dumps({"team": team})
        conn.send(data_out.encode())
        all_players.append([conn, team])
        print(f"[NEW CLIENT] {addr} on team: {team}")

    print("[CONNECTIONS] Ending new client connections")
    print("===========================================\n\n")

    # game loop
    while True:

        # Sending all players of the team with the current turn, prompt
        for player in all_players:
            if player[1] == team:
                data_out = json.dumps({"team": team, "msg": f"Team {team}, select your move: ", "prompt": True})
                player[0].send(data_out.encode())


        all_threads = []
        for player in all_players:
            if player[1] == team:
                t = threading.Thread(target=handle_connection,
                args=(player[0],))
                t.start()
                all_threads.append(t)                    
                print(all_threads)


        # Allow 15 seconds for players to submit vote
        t_end = time.time() + 15
        while time.time() < t_end:
            pass


        # Update board with most voted position
        update_board(team)

        # Send board to all clients
        for player in all_players:
            data_out = json.dumps({"board": game_board, "msg": f"Team{team} placed piece"})
            player[0].send(data_out.encode())

        print("\n[SWITCHING]\n")
        voting = {}

        team = (team + 1) % 2   # Alternates 0 and 1

    
print("[STARTING] Server is starting")

# Start
start()
