from Client import Client
from Server import Server


def main():
    server=Server()
    server.start()
    client=Client("adir_ben_team")
    client.start_client()
    

if __name__ == '__main__':
    main()