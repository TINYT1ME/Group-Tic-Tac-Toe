import socket
import json
import sys
from game import main
import threading
import tkinter as tk
from tkinter import simpledialog
import time

root = tk.Tk()
root.withdraw()

# Connection information
HEADER = 1024
PORT = 5050
FORMAT = "utf-8"
SERVER = input("Please enter server ip address: ")
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

board = [["", "", ""], ["", "", ""], ["", "", ""]]


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


data_in = client.recv(HEADER)
data_in = json.loads(data_in.decode())
team = data_in.get("team")
print(f"You are on team {team}")

# Countdown
countdown_counter = 15


def countdown_pygame():
    global countdown_counter
    if countdown_counter <= 0:
        countdown_counter += 15
    else:
        countdown_counter -= 1
    time.sleep(1)


# Create pygame thread
game_thread = threading.Thread(target=main, args=(board, team, countdown_counter))
game_thread.start()

timer_thread = threading.Thread(target=countdown_pygame)
timer_thread.start()


while True:
    try:
        data_in = client.recv(HEADER)
        data_in = json.loads(data_in.decode())

        # If winner
        if data_in.get("winner"):
            temp = simpledialog.askstring(
                    "", f"Winner is: {data_in.get('winner')}", parent=root
                )
            pygame.quit()
            sys.exit()
        # User prompted to vote piece
        if data_in.get("prompt"):
            x_value = int(
                simpledialog.askstring(data_in.get("msg"), "X Val:", parent=root)
            )
            y_value = int(
                simpledialog.askstring(data_in.get("msg"), "Y Val:", parent=root)
            )
            if x_value == -1 or y_value == -1:
                break

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
            print("board updated")

    except Exception as e:
        if hasattr(e, "KeyboardInterrupt"):
            print("Exiting")
            sys.exit()
        else:
            print(e)
sys.exit()
