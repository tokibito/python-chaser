# coding: utf-8
import logging

from nullpochaser.utils import strarr_to_intarr
from nullpochaser.maps import CHaserMap

class ConnectionCloseSignal(Exception):
    pass

FLAG_CONNECTION_CLOSE = 0

class CHaser(object):
    def __init__(self, connection, username):
        self.connection = connection
        self._username = username
        self.x = 0
        self.y = 0
        self.turn = 0
        self.map = CHaserMap()
        self.setUp()

    def command(self, cmd):
        logging.info('send command [%s]' % cmd)
        return self.connection.send('%s\n' % cmd)

    def receive(self):
        result = self.connection.recv().strip()
        logging.info('data received [%s]' % result)
        return result

    def receive_info(self):
        """
        receiveした後マップ情報をint列で返す
        終了フラグがあった場合は終了シグナルを発行
        """
        result = self.receive()
        info = strarr_to_intarr(result)
        if info[0] == FLAG_CONNECTION_CLOSE:
            raise ConnectionCloseSignal
        return info[1:]

    ################
    # 補助コマンド
    ################
    def username(self):
        return self.command(self._username)

    def getReady(self):
        self.command('gr')
        return self.receive_info()

    def turnEnd(self):
        self.command('#')

    ################
    # 移動系
    ################
    def walkRight(self):
        self.command('wr')
        self.x += 1
        return self.receive_info()

    def walkLeft(self):
        self.command('wl')
        self.x -= 1
        return self.receive_info()

    def walkUp(self):
        self.command('wu')
        self.y += 1
        return self.receive_info()

    def walkDown(self):
        self.command('wd')
        self.y -= 1
        return self.receive_info()

    ################
    # 広範囲探索
    ################
    def lookRight(self):
        self.command('lr')
        return self.receive_info()

    def lookLeft(self):
        self.command('ll')
        return self.receive_info()

    def lookUp(self):
        self.command('lu')
        return self.receive_info()

    def lookDown(self):
        self.command('ld')
        return self.receive_info()

    ################
    # 前方探索
    ################
    def searchRight(self):
        self.command('sr')
        return self.receive_info()

    def searchLeft(self):
        self.command('sl')
        return self.receive_info()

    def searchUp(self):
        self.command('su')
        return self.receive_info()

    def searchDown(self):
        self.command('sd')
        return self.receive_info()

    ################
    # ブロック設置
    ################
    def putRight(self):
        self.command('pr')
        return self.receive_info()

    def putLeft(self):
        self.command('pl')
        return self.receive_info()

    def putUp(self):
        self.command('pu')
        return self.receive_info()

    def putDown(self):
        self.command('pd')
        return self.receive_info()

    def getPos(self):
        """
        位置を返す
        """
        return (self.x, self.y)
    position = property(getPos)

    def start(self):
        """
        実行ループ
        """
        self.username()

        try:
            while True:
                try:
                    # @が来るまで待つ
                    buf = self.receive()
                    if not buf.startswith('@'):
                        continue
                    # getReadyして周囲の情報を取得
                    info = self.getReady()
                    # ユーザ定義の記述ポイントへ
                    # マップ情報のみ渡す
                    self.run(info)
                    self.turnEnd()
                except KeyboardInterrupt:
                    break
                except ConnectionCloseSignal:
                    break
        finally:
            self.tearDown()

    def run(self, info):
        raise NotImplementedError

    def setUp(self):
        """
        初期化用
        """

    def tearDown(self):
        """
        終了前処理
        """
