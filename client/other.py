import game
import threading

board = [
    ["2","5","2"],
    ["2","5","2"],
    ["2","5","1"]
]

t = threading.Thread(target=game.main, args=(board,))
t.start()

board[1][1] = "8"

print(game.get_click())
