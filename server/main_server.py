# Libraries
import socket 
import json
import time
import select
import threading

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

all_players = []

voting = []

def check_valid(inp: str):
    if (
        (
            int(inp[0]) >= 0 and
            int(inp[0]) <= 2
        ) and
        (
            int(inp[2]) >= 0 and
            int(inp[2]) <= 2
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
        pos = [x_value, y_value]
        for vote in voting:
            if vote[0] == pos:
                vote[1] += 1
            else:
                voting.append([pos, 1])
        print(voting)
        print(f"\n[CLIENT DATA] {conn} entered: x={x_value}, y={y_value}\n")
    
# Server start function
def start():
    # TEAM 0 IS X, TEAM 1 is O
    team = 0

    # Server Listening
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}\n")

    # Give 60 seconds at beginning for clients to connect
    t_end = time.time() + 10
    print("[CONNECTIONS] Beginning connections (60 sec)")

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
        # while time.time() < t_end:
        for player in all_players:
            if player[1] == team:
                t = threading.Thread(target=handle_connection,
                args=(player[0],))
                t.start()
                all_threads.append(t)                    
                print(all_threads)

        t_end = time.time() + 15
        while time.time() < t_end:
            pass

        print(voting)

        print("\n[SWITCHING]\n")

        team = (team + 1) % 2   # Alternates 0 and 1

    
print("[STARTING] Server is starting")

# Start
start()
