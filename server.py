#sikirin yonatan 311292122 סיקירין יונתן

import socket
import threading
import random

# Define constants
import time

HOST = '127.0.0.1'  # Standard loopback IP address (localhost)
PORT = 60000  # Port to listen on (non-privileged ports are > 1023)
FORMAT = 'utf-8'  # Define the encoding format of messages from client-server
ADDR = (HOST, PORT)  # Creating a tuple of IP+PORT
BOARD_COLS = 7
BOARD_ROWS = 6


# Function that handles a single client connection
# Operates like an echo-server
def handle_client1(conn, addr):
    print('[CLIENT CONNECTED] on address: ', addr)  # Printing connection address

    class Board:
        def __init__(self):
            self.Board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
            self.turns = 0
            self.last_move = [-1, -1]  # [row,col]
            self.ai_counter = 0
            self.ai_difficulty_hard = True
            self.flag = 0
            self.x_wins = 0
            self.o_wins = 0
            self.all_turns = 0

        def print_stats(self):
            conn.send(f"game took {self.turns} turns".encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            conn.send(f"X won {self.x_wins} times".encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            conn.send(f"0 won {self.o_wins} times".encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            if self.ai_difficulty_hard:
                conn.send("Difficulty was hard".encode(FORMAT))
                conn.send("\n".encode(FORMAT))
            else :
                conn.send("Difficulty was easy".encode(FORMAT))
                conn.send("\n".encode(FORMAT))

        def easy_ai(self):
            x = (random.randint(0, 6))  # Chooses random column places there if possible
            while True:
                for i in range(BOARD_ROWS - 1, -1, -1):
                    if self.Board[i][x] == ' ':  # if there is an empty space
                        return x
                x = (random.randint(0, 6))  # Chooses another random column

        def reset_board(self):
            self.Board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

        def hard_ai(self):  # checks all directions using if statements
            if self.flag == 0:
                x = (random.randint(0, 6))
                self.flag = 1
                return x
            try:
                for i in range(BOARD_ROWS):  # If can win this turn will place in the winning column
                    for j in range(BOARD_COLS):

                        if self.Board[i][j] == '0' and self.Board[i][j + 1] == '0' and self.Board[i][
                            j + 2] == '0' and self.in_bounds(i, j + 3) and self.Board[i][j + 3] == ' ' and \
                                self.Board[i + 1][j + 3] != ' ':

                            return j + 3
                        if self.Board[i][j] == '0' and self.Board[i][j + 1] == '0' and self.Board[i][
                            j + 2] == '0' and self.in_bounds(i, j - 1) and self.Board[i][j - 1] == ' ' and \
                                self.Board[i + 1][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == '0' and self.Board[i + 1][j] == '0' and self.Board[i + 2][
                            j] == '0' and self.in_bounds(i - 1, j) and self.Board[i - 1][j] == ' ':

                            return j
                        if self.Board[i][j] == '0' and self.Board[i + 1][j - 1] == '0' and self.Board[i + 2][
                            j - 2] == '0' and self.in_bounds(i - 1, j + 1) and self.Board[i - 1][j + 1] == ' ' and \
                                self.Board[i][j + 1] != ' ':

                            return j + 1
                        if self.Board[i][j] == '0' and self.Board[i + 1][j + 1] == '0' and self.Board[i + 2][
                            j + 2] == '0' and self.in_bounds(i - 1, j - 1) and self.Board[i - 1][j - 1] == ' ' and \
                                self.Board[i][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == '0' and self.Board[i - 1][j + 1] == '0' and self.Board[i - 2][
                            j + 2] == '0' and self.in_bounds(i + 1, j - 1) and self.Board[i + 1][j - 1] == ' ' and \
                                self.Board[i + 2][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == '0' and self.Board[i - 1][j - 1] == '0' and self.Board[i - 2][
                            j - 2] == '0' and self.in_bounds(i + 1, j + 1) and self.Board[i + 1][j + 1] == ' ' and \
                                self.Board[i + 2][j + 1] != ' ':

                            return j + 1
            except:
                pass
            try:
                for i in range(BOARD_ROWS):  # If can lose next turn will place in the correct column
                    for j in range(BOARD_COLS):

                        if self.Board[i][j] == 'X' and self.Board[i][j + 1] == 'X' and self.Board[i][
                            j + 2] == 'X' and self.in_bounds(i, j + 3) and self.Board[i][j + 3] == ' ' and \
                                self.Board[i + 1][j + 3] != ' ':

                            return j + 3
                        if self.Board[i][j] == 'X' and self.Board[i][j + 1] == 'X' and self.Board[i][
                            j + 2] == 'X' and self.in_bounds(i, j - 1) and self.Board[i][j - 1] == ' ' and \
                                self.Board[i + 1][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == 'X' and self.Board[i + 1][j] == 'X' and self.Board[i + 2][
                            j] == 'X' and self.in_bounds(i - 1, j) and self.Board[i - 1][j] == ' ':

                            return j
                        if self.Board[i][j] == 'X' and self.Board[i + 1][j - 1] == 'X' and self.Board[i + 2][
                            j - 2] == 'X' and self.in_bounds(i - 1, j + 1) and self.Board[i - 1][j + 1] == ' ' and \
                                self.Board[i][j + 1] != ' ':

                            return j + 1
                        if self.Board[i][j] == 'X' and self.Board[i + 1][j + 1] == 'X' and self.Board[i + 2][
                            j + 2] == 'X' and self.in_bounds(i - 1, j - 1) and self.Board[i - 1][j - 1] == ' ' and \
                                self.Board[i][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == 'X' and self.Board[i - 1][j + 1] == 'X' and self.Board[i - 2][
                            j + 2] == 'X' and self.in_bounds(i + 1, j - 1) and self.Board[i + 1][j - 1] == ' ' and \
                                self.Board[i + 2][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == 'X' and self.Board[i - 1][j - 1] == 'X' and self.Board[i - 2][
                            j - 2] == 'X' and self.in_bounds(i + 1, j + 1) and self.Board[i + 1][j + 1] == ' ' and \
                                self.Board[i + 2][j + 1] != ' ':

                            return j + 1
            except:
                pass

            try:
                for i in range(BOARD_ROWS):  # Blocks player from getting 3 in a row
                    for j in range(BOARD_COLS):
                        if self.Board[5][j] == 'X' and self.in_bounds(5, j + 1) and self.Board[5][j + 1] == ' ':

                            return j + 1
                        if self.Board[5][j] == 'X' and self.in_bounds(5, j - 1) and self.Board[5][j - 1] == ' ':

                            return j - 1
                        if self.Board[4][j] == 'X' and self.Board[4][j + 1] == 'X' and self.in_bounds(4, j + 2) and \
                                self.Board[4][j + 2] == ' ' and self.Board[5][j + 2] != ' ':

                            return j + 2
                        if self.Board[4][j] == 'X' and self.Board[4][j - 1] == 'X' and self.in_bounds(4, j - 2) and \
                                self.Board[4][j - 2] == ' ' and self.Board[5][j - 2] != ' ':

                            return j - 2

            except:
                pass
            try:
                for i in range(BOARD_ROWS):   # Blocks player from getting 3 in a row
                    for j in range(BOARD_COLS):
                        if self.Board[i][j] == 'X' and self.Board[i + 1][j] == 'X' and self.Board[i + 2][
                            j] == 'X' and self.in_bounds(i - 1, j) and self.Board[i - 1][j] == ' ':

                            return j
                        if self.Board[i][j] == 'X' and self.Board[i][j + 1] == 'X' and self.in_bounds(i, j + 2) and \
                                self.Board[i][j + 2] == ' ' and self.Board[i + 1][j + 2] != ' ':

                            return j + 2
                        if self.Board[i][j] == 'X' and self.Board[i][j - 1] == 'X' and self.in_bounds(i, j - 2) and \
                                self.Board[i][j - 2] == ' ' and self.Board[i + 1][j - 2] != ' ':

                            return j - 2
                        if self.Board[i][j] == 'X' and self.Board[i + 1][j - 1] == 'X' and self.in_bounds(i - 1,
                                                                                                          j + 1) and \
                                self.Board[i - 1][j + 1] == ' ' and self.Board[i][j + 1] != ' ':

                            return j + 1
                        if self.Board[i][j] == 'X' and self.Board[i + 1][j + 1] == 'X' and self.in_bounds(i - 1,
                                                                                                          j - 1) and \
                                self.Board[i - 1][j - 1] == ' ' and self.Board[i][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == 'X' and self.Board[i - 1][j + 1] == 'X' and self.in_bounds(i + 1,
                                                                                                          j - 1) and \
                                self.Board[i + 1][j - 1] == ' ' and self.Board[i + 2][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == 'X' and self.Board[i - 1][j - 1] == 'X' and self.in_bounds(i + 1,
                                                                                                          j + 1) and \
                                self.Board[i + 1][j + 1] == ' ' and self.Board[i + 2][j + 1] != ' ':

                            return j + 1

            except:
                pass
            try:
                for i in range(BOARD_ROWS):   # Creates pairs where ever it can
                    for j in range(BOARD_COLS):
                        if self.Board[i][j] == '0' and self.Board[i + 1][j - 1] == '0' and self.in_bounds(i - 1,
                                                                                                          j + 1) and \
                                self.Board[i - 1][j + 1] == ' ' and self.Board[i][j + 1] != ' ':

                            return j + 1
                        if self.Board[i][j] == '0' and self.Board[i + 1][j + 1] == '0' and self.in_bounds(i - 1,
                                                                                                          j - 1) and \
                                self.Board[i - 1][j - 1] == ' ' and self.Board[i][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == '0' and self.Board[i - 1][j + 1] == '0' and self.in_bounds(i + 1,
                                                                                                          j - 1) and \
                                self.Board[i + 1][j - 1] == ' ' and self.Board[i + 2][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == '0' and self.Board[i - 1][j - 1] == '0' and self.in_bounds(i + 1,
                                                                                                          j + 1) and \
                                self.Board[i + 1][j + 1] == ' ' and self.Board[i + 2][j + 1] != ' ':

                            return j + 1
                        if self.Board[i][j] == '0' and self.in_bounds(i, j + 1) and self.Board[i][j + 1] == ' ' and \
                                self.Board[i + 1][j + 1] != ' ':

                            return j + 1
                        if self.Board[i][j] == '0' and self.in_bounds(i, j - 1) and self.Board[i][j - 1] == ' ' and \
                                self.Board[i + 1][j - 1] != ' ':

                            return j - 1
                        if self.Board[i][j] == '0' and self.in_bounds(i - 1, j) and self.Board[i - 1][j] == ' ':

                            return j
            except:
                x = (random.randint(0, 6))   # Chooses random column places there if possible
                while True:
                    for i in range(BOARD_ROWS - 1, -1, -1):
                        if self.Board[i][x] == ' ':  # if there is an empty space
                            return x
                    x = (random.randint(0, 6))  # Chooses another random column

        def ai_turn(self): # returns false if its the players turn
            if self.ai_counter % 2 == 0:
                self.ai_counter += 1
                return False
            self.ai_counter += 1
            return True

        def print_board(self):
            conn.send(f"Current Board".encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            for cols in range(BOARD_COLS):
                conn.send(f"  {cols + 1}".encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            for rows in range(BOARD_ROWS):
                conn.send("|".encode(FORMAT))
                for cols in range(BOARD_COLS):
                    conn.send(f"{self.Board[rows][cols]} |".encode(FORMAT))
                conn.send("\n".encode(FORMAT))
            conn.send(f"{'-' * 35} \n".encode(FORMAT))

        def which_turn(self):
            players = ['X', '0']
            return players[self.turns % 2]

        def turn(self, col):
            for i in range(BOARD_ROWS - 1, -1, -1):  # starts from bottom of chosen column
                if self.Board[i][col] == ' ':  # if the is an empty space
                    self.Board[i][col] = self.which_turn()  # places X or O depending on turn
                    self.last_move = [i, col]  # saves the last move to be used in check_winner
                    self.turns += 1  # counts turns
                    self.all_turns += 1
                    return True

            return False

        def in_bounds(self, row, col):  # checks if location is in bounds
            return BOARD_ROWS > row >= 0 <= col < BOARD_COLS

        def check_winner(self):  # checks if the last move won the game
            last_row = self.last_move[0]
            last_col = self.last_move[1]
            last_player = self.Board[last_row][last_col]
            # test all directions
            directions = [[[-1, 0], 0, True],
                          [[1, 0], 0, True],
                          [[0, -1], 0, True],
                          [[0, 1], 0, True],
                          [[-1, -1], 0, True],
                          [[1, 1], 0, True],
                          [[-1, 1], 0, True],
                          [[1, -1], 0, True]]
            for a in range(4):  # moves 4 times in each direction from last move
                for d in directions:
                    r = last_row + (d[0][0] * (a + 1))
                    c = last_col + (d[0][1] * (a + 1))
                    if d[2] and self.in_bounds(r, c) and self.Board[r][
                        c] == last_player:  # if the search is still ture and in bounds and the loacation has the same colored thing add +1 to counter
                        d[1] += 1
                    else:
                        # stop seatrch
                        d[2] = False  # direction becomes False will not continue the search from here again
            for i in range(0, 7, 2):
                if (directions[i][1] + directions[i + 1][
                    1] >= 3):  # if found 4 in a row (counting from zero) declare winner
                    self.print_board()
                    print(f"{last_player} won")
                    conn.send(f"{last_player} won".encode(FORMAT))
                    conn.send("\n".encode(FORMAT))
                    if last_player == 'X':
                        self.x_wins += 1
                    if last_player == '0':
                        self.o_wins += 1
                    self.print_stats()
                    self.reset_board()
                    self.ai_counter = 0
                    self.turns = 0
                    return last_player

            return False

    def play():
        game = Board()
        conn.send("enter 1 to exit \n      2 for a game VS AI \n  ".encode(FORMAT))
        first_choice = conn.recv(1024).decode(FORMAT)
        if first_choice == "1":
            conn.send("Goodbye client".encode(FORMAT))
            return
        if first_choice == "2":
            conn.send("AI difficulty \nenter 1 for hard \n      2 for easy  ".encode(FORMAT))
            x = conn.recv(1024).decode(FORMAT)
            conn.send("how many wins  ".encode(FORMAT))
            num_of_wins = int(conn.recv(1024).decode(FORMAT))
            while num_of_wins <= 0:
                conn.send("re-enter number of wins".encode(FORMAT))
                num_of_wins = int(conn.recv(1024).decode(FORMAT))
            if x == "2":
                game.ai_difficulty_hard = False
            while 2 >= game.x_wins or 2 >= game.o_wins:
                gameOver = False
                while not gameOver:
                    if num_of_wins <= game.x_wins or num_of_wins <= game.o_wins:
                        conn.send(f"all games are complete ({num_of_wins} wins)".encode(FORMAT))
                        conn.send("\n".encode(FORMAT))
                        conn.send(f"X won {game.x_wins} games ".encode(FORMAT))
                        conn.send("\n".encode(FORMAT))
                        conn.send(f"0 won {game.o_wins} games ".encode(FORMAT))
                        conn.send("\n".encode(FORMAT))
                        conn.send(
                            f"there have been {game.all_turns} turns in {num_of_wins} games with an average of {game.all_turns / num_of_wins} turns per game".encode(
                                FORMAT))
                        conn.send("\n".encode(FORMAT))
                        return True
                    game.print_board()
                    valid_move = False
                    if not game.ai_turn():
                        while not valid_move:
                            conn.send(f"{game.which_turn()} Please pick a column 1-7 ".encode(FORMAT))
                            user_move = conn.recv(1024).decode(FORMAT)
                            try:
                                valid_move = game.turn(int(user_move) - 1)
                            except:
                                conn.send(f"Please choose a number between 1 and {BOARD_COLS}".encode(FORMAT))
                        if game.check_winner():
                            gameOver = True

                    else:
                        if game.ai_difficulty_hard:
                            game.turn(game.hard_ai())
                            if game.check_winner():
                                gameOver = True
                        else:
                            game.turn(game.easy_ai())
                            if game.check_winner():
                                gameOver = True
                if not any(' ' in x for x in game.Board):
                    print("The game is a draw..")
                    conn.send("The game is a draw..".encode(FORMAT))
                    game.reset_board()
                    return
        #if first_choice == "3":
           # return

    try:
        play()

    except:
        print("[CLIENT CONNECTION INTERRUPTED] on address: ", addr)


def handle_client_server_full(conn, addr):
    print('[SERVER IS FULL CLIENT ATTEMPTED CONNECTION] on address: ', addr)
    conn.send("server is full  ".encode(FORMAT))
    conn.send("\n".encode(FORMAT))


# Function that handles the second parallel client
# Only when 2 clients are connected simultaneously, this function will handle the second client

# Function that starts the server
def start_server():
    server_socket.bind(ADDR)  # binding socket with specified IP+PORT tuple

    print(f"[LISTENING] server is listening on {HOST}")
    server_socket.listen()  # Server is open for connections

    while True:
        if threading.activeCount() <= 5:
            connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
            thread = threading.Thread(target=handle_client1, args=(connection, address))  # Creating new Thread object.
            thread.start()
        else:
            connection, address = server_socket.accept()  # Waiting for client to connect to server (blocking call)
            thread = threading.Thread(target=handle_client_server_full,
                                      args=(connection, address))  # Creating new Thread object.
            thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}\n")  # printing the amount of threads working
        # on this process (opening another thread for next client to come!)


# Main
if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Opening Server socket
    print("[STARTING] server is starting...")
    start_server()
    print("THE END!")
