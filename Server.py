import random
import threading
import time
from _thread import start_new_thread
from socket import *
from Style import Style


class Server:

    def __init__(self):

        self.serverIP = 0
        self.serverIP = gethostbyname(gethostname())
        # try to find IP
        if self.serverIP == 0:
            print("sorry you have some problem with your IP address")
            return
        self.broadcast_port = 13147
        self.server_port = 2080
        self.UDPsocket = 0
        self.TCPsocket = 0
        self.style=Style()
        # try to connect sockets
        try:
            self.UDPsocket = socket(AF_INET, SOCK_DGRAM)
            self.TCPsocket = socket(AF_INET, SOCK_STREAM)
        except:
            print("sorry you have some problem with your sockets")
            return

        self.players_list = ["Test_player", "Test_player", "Test_player"]
        self.players_scores = [0, 0, 0, 0]
        self.on_game = False

    def start(self):
        self.UDPsocket.bind((self.serverIP, self.server_port))
        self.TCPsocket.bind((self.serverIP, self.server_port))
        thread = threading.Thread(target=self.connect_TCP)
        thread.start()

    def connect_TCP(self):

        self.style.show("Server started, listening on IP address " + str(self.serverIP))
        threading.Thread(target=self.broadcast_details).start()
        self.TCPsocket.listen()
        while True:
            # client accepted
            connection, addr = self.TCPsocket.accept()
            mutex = threading.Lock()
            mutex.acquire()
            self.shuffle_player()
            mutex.release()

            # new thread
            start_new_thread(self.handler, (connection,))

    def handler(self, socket):

        name = str(socket.recv(1024), 'utf-8')
        self.set_player(name)

        while self.gameStart() == False:
            time.sleep(0.5)

        # send Welcome message
        if self.send_Welcome_Message(socket) == False:
            return

        index = self.players_list.index(name)

        # game start
        start_time = time.time()
        while True:
            if time.time() - start_time > 10:
                break
            data = socket.recv(1024)
            if not data:
                continue
            print(f"Team {name} sent: {str(data, 'utf-8')}")
            # update score
            self.players_scores[index] += 1

        winner_idx, teamScores = self.choose_winner()

        # Game Over send end Message
        if self.send_Finish_Message(socket, winner_idx, ["Group 1", "Group 2"], teamScores) == False:
            return
        socket.close()

    def broadcast_details(self):
        # collect the broadcast details and send to clients

        while True:
            if not self.on_game:
                start_time = time.time()
                server = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
                server.settimeout(0.2)
                server.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                server.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
                try:
                    # send
                    self.send_brodcast(start_time, server)
                except:
                    pass

    def shuffle_player(self):
        # shuffle player list
        if len(self.players_list) > 1:
            random.shuffle(self.players_list)

    def set_player(self, player):
        self.players_list += [player]

    def gameStart(self):
        # return true if the game start else false
        if len(self.players_list) > 1:
            self.on_game = True
            return True
        else:
            self.on_game = False
            return False

    def send_Welcome_Message(self, s):
        # send welcome message to client
        try:
            s.send(bytes("Welcome to Keyboard Spamming Battle Royale.\n"
                         "Group 1:\n==\n"
                         f"{self.players_list[0]}\n{self.players_list[1]}\n"
                         "Group 2:\n==\n"
                         f"{self.players_list[2]}\n{self.players_list[3]}\n"
                         "Start pressing keys on your keyboard as fast as you can!!\n", encoding='utf8'))
            return True
        except:
            print("sending message faild")
            return False

    def send_Finish_Message(self, socket, winner_idx, names, teamScore):
        # try to send welcome message to clients
        try:
            mess = "Game over!\n" \
                      f"Group 1 typed in {teamScore[0]} characters. Group 2 typed in {teamScore[1]} characters.\n" \
                      f"{names[winner_idx]} wins!\n==\n" \
                      f"Congratulations to the winners:\n==\n" \
                      f"{self.players_list[0 + winner_idx * 2]}\n{self.players_list[1 + winner_idx * 2]}\n"
            socket.send(bytes(mess, encoding='utf8'))
            self.on_game = False
            return True
        except:
            print("sending end message faild")
            return False

    def choose_winner(self):
        # calculate the winner
        # winner the team that typing best
        teamScores = [self.players_scores[0] + self.players_scores[1], self.players_scores[2] + self.players_scores[3]]
        winner_idx = 0
        if teamScores[0] == teamScores[1]:
            print("it's a tie")

        elif teamScores[0] < teamScores[1]:
            winner_idx = 1

        return winner_idx, teamScores

    def send_brodcast(self, start_time, server):

        # send brodcast mess every 10 sec
        mess = bytes.fromhex("feedbeef") + bytes.fromhex("02") + self.server_port.to_bytes(2, byteorder='big')
        while time.time() - start_time < 10:
            time.time() - start_time < 10
            server.sendto(mess, ('<broadcast>', self.broadcast_port))
            time.sleep(1)






