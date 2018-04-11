import socket

BUFFER_SIZE = 4096


class Connection:
    def __init__(self, host, port, socket=None):
        self.host = host
        self.port = port
        self.socket = None

    def make_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, packet):
        return self.socket.send(packet)

    def recv(self):
        return self.socket.recv(BUFFER_SIZE)
