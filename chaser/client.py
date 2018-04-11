import logging
from . import const
from .connection import Connection

logger = logging.getLogger(__name__)


class Client:
    """コマンド送受信クライアント
    """
    def __init__(self, host, port, username, connection=None):
        self.host = host
        self.port = port
        self.connection = None
        self._username = username

    def connect(self):
        if self.connection is None:
            self.connection = Connection(self.host, self.port)
            self.connection.connect()

    def send_command(self, command):
        if self.connection is None:
            self.connect()
        logging.info('send command [%s]', command)
        return self.connection.send(command + b'\r\n')

    def _receive(self):
        if self.connection is None:
            self.connect()
        buffer = self.connection.recv().strip()
        logging.info('data received [%s]', buffer)
        return buffer

    def receive(self):
        """
        データをサーバーから受信します

        :returns (byte, list(int) or None): 制御情報とマップ情報
        """
        buffer = self._receive()
        control = buffer[:1]
        # 制御情報のみの場合
        if control in [const.GAME_FINISHED, const.TURN_START]:
            return control, None
        # 制御情報 + マップ情報の場合
        info = list(map(int, buffer[1:].decode('ascii')))
        return control, info

    def username(self):
        """
        ユーザ名を送信します
        """
        return self.send_command(self._username.encode('utf-8'))

    def get_ready(self):
        """
        ターン開始

        :return list(int): マップ情報
        """
        self.send_command(b'gr')
        return self.receive()

    def turn_end(self):
        """
        ターン終了
        """
        self.send_command(const.TURN_END)

    def walk_right(self):
        """右に移動

        :return list(int): マップ情報
        """
        self.send_command(b'wr')
        return self.receive()

    def walk_left(self):
        """左に移動

        :return list(int): マップ情報
        """
        self.send_command(b'wl')
        return self.receive()

    def walk_up(self):
        """上に移動

        :return list(int): マップ情報
        """
        self.send_command(b'wu')
        return self.receive()

    def walk_down(self):
        """下に移動

        :return list(int): マップ情報
        """
        self.send_command(b'wd')
        return self.receive()

    def look_right(self):
        """探索(右)

        :return list(int): マップ情報
        """
        self.send_command(b'lr')
        return self.receive()

    def look_left(self):
        """探索(左)

        :return list(int): マップ情報
        """
        self.send_command(b'll')
        return self.receive()

    def look_up(self):
        """探索(上)

        :return list(int): マップ情報
        """
        self.send_command(b'lu')
        return self.receive()

    def look_down(self):
        """探索(下)

        :return list(int): マップ情報
        """
        self.send_command(b'ld')
        return self.receive()

    def search_right(self):
        """探索(直線右)

        :return list(int): マップ情報
        """
        self.send_command(b'sr')
        return self.receive()

    def search_left(self):
        """探索(直線左)

        :return list(int): マップ情報
        """
        self.send_command(b'sl')
        return self.receive()

    def search_up(self):
        """探索(直線上)

        :return list(int): マップ情報
        """
        self.send_command(b'su')
        return self.receive()

    def search_down(self):
        """探索(直線下)

        :return list(int): マップ情報
        """
        self.send_command(b'sd')
        return self.receive()

    def put_right(self):
        """ブロックを設置(右)

        :return list(int): マップ情報
        """
        self.send_command(b'pr')
        return self.receive()

    def put_left(self):
        """ブロックを設置(左)

        :return list(int): マップ情報
        """
        self.send_command(b'pl')
        return self.receive()

    def put_up(self):
        """ブロックを設置(上)

        :return list(int): マップ情報
        """
        self.send_command(b'pu')
        return self.receive()

    def put_down(self):
        """ブロックを設置(下)

        :return list(int): マップ情報
        """
        self.send_command(b'pd')
        return self.receive()
