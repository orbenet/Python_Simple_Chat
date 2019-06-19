import socket
import threading


class ClientClass:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 11112
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = True

    def connect_to_server(self):
        self.socket.connect((self.ip, self.port))
        print(self.socket.recv(1024).decode())

    def r_message(self):
        self.connected = True
        while self.connected:
            try:
                msg = self.socket.recv(1024).decode()
                print(msg)
            except socket.error:
                self.connected = False
                self.close_connection()

    def start_r_thread(self):
        x = threading.Thread(target=self.r_message)
        x.setName("My_r")
        x.start()

    def send_message(self):
        while self.connected:
            try:
                print("\n")
                msg = input("")
                self.socket.send(msg.encode())
            except socket.error:
                self.connected = False
                self.close_connection()

    def close_connection(self):
        print("Server Cannot Be Reached")
        self.socket.close()


if __name__ == "__main__":
    Client = ClientClass()
    Client.connect_to_server()
    Client.start_r_thread()
    Client.send_message()
