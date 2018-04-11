import logging
from . import const
from . import exceptions

logger = logging.getLogger(__name__)


class Client:
    """コマンド送受信クライアント
    """
    def __init__(self, connection, username):
        self.connection = connection
        self.username = username

    def send_command(self, command):
        logging.info('send command [%s]', command)
        return self.connection.send('{}\n'.format(command))

    def _receive(self):
        buffer = self.connection.recv().strip()
        logging.info('data received [%s]', buffer)
        return buffer

    def receive(self):
        """
        receiveした後マップ情報をintのlistで返す
        終了フラグがあった場合は例外を発生させる
        """
        buffer = self._receive()
        values = list(map(int, buffer.decode('ascii')))
        if values[0] == const.GAME_FINISHED:
            raise exceptions.GameFinished
        return values
