# Libraries
import socket 
import threading

# Server info
HEADER = 64
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

# Client handling, new thread per client
def handle_client(conn, addr, team: int):
    print(f"New client connected: {addr}")

    # Sending team to user
    conn.send((f"You are on team {team}").encode())

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # Checking if user wants to disconnect
            if msg == "q":
                connected = False

    conn.close()
        

# Server start function
def start():
    # TEAM 0 IS X, TEAM 1 is O
    team = 0

    # Server Listening
    server.listen()
    print(f"Server is listening on {SERVER}\n")

    # Checking for new clients, loop
    while True:
        team = (team + 1) % 2   # Alternates 0 and 1

        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr, team))
        thread.start()
        print(f"Connection count: {threading.active_count() - 1}")


print("Server is starting")

# Start
start()
