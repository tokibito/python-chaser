import socket
BUFSIZE = 4096

class Connection(object):
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send(self, packet):
        return self.socket.send(packet)

    def recv(self):
        return self.socket.recv(BUFSIZE)
