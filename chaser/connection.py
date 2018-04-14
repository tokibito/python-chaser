import socket

BUFFER_SIZE = 512


class Connection:
    """接続とデータ送受信を管理するクラス
    """
    def __init__(self, host, port, socket=None):
        self.host = host
        self.port = port
        self.socket = None

    def make_socket(self):
        """ソケットオブジェクトを生成します
        """
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """ソケットオブジェクトを生成し、ホストに接続します
        """
        self.socket = self.make_socket()
        self.socket.connect((self.host, self.port))

    def send(self, packet):
        """データを送信します
        """
        return self.socket.send(packet)

    def recv(self):
        """データを受信します
        """
        return self.socket.recv(BUFFER_SIZE)
