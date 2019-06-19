from threading import Thread
import socket
import datetime
import time
SERVER_IP = "127.0.0.1"

SERVER_PORT = 11112

NUM_OF_LISTENERS = 5


def l_print(message):
    z = time.strftime("%z").split(" ")
    _z = ''
    for item in z:
        _z += item[0]
    x = "{} {}:~: --> ".format(datetime.datetime.now(), _z)
    x = x + message
    print(x)


def w_print(message):
    z = time.strftime("%z").split(" ")
    _z = ''
    for item in z:
        _z += item[0]
    x = "{} {}:~: --> ".format(datetime.datetime.now(), _z)
    x = x + message
    return x

class ServerClass:
    def __init__(self, _ip, _port):
        self.ip = _ip
        self.port = _port
        self.ClientInstanceList = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.chat_log = open("{}CHAT_LOG.txt".format(str(datetime.datetime.now()).replace(":", "-")), 'w')
        self.connected = True

    def delete_client_from_list(self,client):
        self.ClientInstanceList.remove(client)

    def start_server(self):
        self.socket.bind((self.ip,self.port))
        l_print("Starting Server {} on Port {} ".format(self.ip, self.port))

    def accept_client_connection(self):
        while self.connected:
            try:
                self.socket.listen(100)
                conn, a = self.socket.accept()
                ClientInstance(self, conn, a)
                l_print("Client {} Connected to Server {}".format(a, self.ip))
                l_print("CLIENT_LIST: {}".format(self.ClientInstanceList))
            except socket.error:
                self.connected = False
                self.close_server()

    def close_server(self):
        self.socket.close()
        self.chat_log.close()
        l_print("Closed Server {} on Port {}".format(self.ip, self.port))


class ClientInstance(Thread):
    def __init__(self, _parent, _conn, _a):
        Thread.__init__(self)
        self.parent = _parent
        self.conn = _conn
        self.a = _a
        self.start()
        self.connected = True
        self.parent.ClientInstanceList.append(self)

    def logon_msg(self):
        self.conn.send("###############################################################################################"
                       "#\n###Welcome to Or Chat Server V1 -Type Anything and it will be sent to other connected Client"
                       "s###\n#########################################################################################"
                       "#######".encode())

    def r_msg_from_client_send_to_all_clients(self):
        try:
            data = self.conn.recv(1024).decode()
            if len(data) > 0:
                _msg = (self.a[0] + " says::: " + data)
                self.parent.chat_log.write(w_print(_msg))
                self.parent.chat_log.write("\n")
                self.parent.chat_log.flush()
                for client in self.parent.ClientInstanceList:
                    client.conn.send(w_print(_msg).encode())
        except socket.error:
            self.parent.ClientInstanceList.remove(self)
            self.connected = False
            l_print("Client {} is Dead".format(str(self.a)))

    def run(self):
        self.logon_msg()
        while self.connected:
            self.r_msg_from_client_send_to_all_clients()


if __name__ == "__main__":
    ChatServerA = ServerClass(SERVER_IP, SERVER_PORT)
    ChatServerA.start_server()
    ChatServerA.accept_client_connection()
    ChatServerA.close_server()
