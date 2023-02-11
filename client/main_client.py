import socket

# Connection information
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = input("Please enter server ip address")
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

while True:
    msg_recv = client.recv(2048).decode(FORMAT)
    print(msg_recv)
    
