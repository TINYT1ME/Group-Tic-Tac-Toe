import socket
import json
import sys
from game import main
import threading

# Connection information
HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = input("Please enter server ip address: ")
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

board = [
    ["","",""],
    ["","",""],
    ["","",""]
]

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

data_in = client.recv(HEADER)
data_in = json.loads(data_in.decode())
team = data_in.get("team")
print(f"You are on team {team}")

# Create pygame thread
game_thread = threading.Thread(target=main, args=(board, team))
game_thread.start()


while True:
    try:
        data_in = client.recv(HEADER)
        data_in = json.loads(data_in.decode())

        # User prompted to vote piece
        if data_in.get("prompt"):
            x_value = int(input("x: "))
            y_value = int(input("y: "))
            if x_value == -1 or y_value == -1:
                break                
            
            #while x_value == None and y_value == None:
            #    pass

            # Sending back selection
            data_out = json.dumps({"x": x_value, "y": y_value})
            client.send(data_out.encode())
            print("Sent\n")

        # Board update
        if data_in.get("board"):
            temp_board = data_in.get("board")
            for i in range(3):
                for j in range(3):
                    board[i][j] = temp_board[i][j]

            print(data_in.get("msg"))
            for row in board:
                print(" | ".join(row))
                print("----")
            print("")

    except Exception as e:
        if hasattr(e, "KeyboardInterrupt"):
            print("Exiting")
            sys.exit()
        else:
            print(e)
