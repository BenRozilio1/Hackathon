import socket
import threading
from socket import *
import getch

class Client():
    def __init__(self, team_name):
        self.broadcast = 13147
        self.IP = gethostname()
        self.team_name = team_name
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.run = False

    def start(self):
        #starting a new client thread
        thread = threading.Thread(target=self.listen_broadcast())
        thread.start()

    def listen_broadcast(self):
        # client accepting the udp massage
        print("Client started - listening for broadcasts...")
        try:
            self.udp_socket.bind(('', self.broadcast))
        except:
            self.listen_broadcast()
        port_tcp = self.find_tcp()
        self.connect_server_tcp(port_tcp)

    def find_tcp(self):
        # trying to finding udp port
        try:
            message = self.udp_socket.recvfrom(1024)
            port_tcp = message[0][5:]
            port_tcp = int.from_bytes(port_tcp, byteorder='big', signed=False)
            return port_tcp
        except:
            print("can't connect to udp socket")

    def recieve_from_server(self, client_socket):
        # this function charge on recieve massage from server
        data = client_socket.recv(1024)
        msge = str(data, 'utf-8')
        print(msge)
        self.run=False


    def connection_tcp(self,port_tcp):
        # create a tcp connection
        client_socket = socket(AF_INET, SOCK_STREAM)
        print(f"Client connecting to server port: {port_tcp}")
        client_socket.connect((self.IP, port_tcp))
        client_socket.send(bytes(self.team_name, encoding='utf8'))
        recived_data = str(client_socket.recv(1024), 'utf-8')
        print(recived_data)
        return client_socket




    def connect_server_tcp(self, port_tcp):
        # connecting to server and send him chars
        client_socket=self.connection_tcp(port_tcp)
        client_socket.settimeout(0.0)
        self.run = True
        while self.run:
            try:
                self.recieve_from_server(client_socket)
            except:
                try:
                    chr = getch.getch()
                    try:
                        client_socket.send(bytes(chr, encoding='utf8'))
                    except:
                        self.recieve_from_server(client_socket)
                except:
                    continue
                    #trying again
        client_socket.close()

    def start_client(self):
        self.start()