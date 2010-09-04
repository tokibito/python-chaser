# coding: utf-8
import logging

from nullpochaser.const import *
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

    def _update_map_normal(self, info):
        """
        通常の周囲8マスの情報でマップを更新
        """
        def _update(cell_y, line_info):
            for idx, celltype in enumerate(line_info):
                cell_x = self.x - 1 + idx
                self.map.updateCell(position=(cell_x, cell_y), celltype=celltype, turn=self.turn)
        # 1列目
        _update(self.y + 1, info[:3])
        # 2列目
        _update(self.y, info[3:6])
        # 3列目
        _update(self.y - 1, info[6:9])

    def _update_map_look(self, info, direction):
        """
        lookコマンドの情報でマップを更新
        """
        def _update(func_cell_x, func_cell_y, line_info):
            for idx, celltype in enumerate(line_info):
                cell_x = func_cell_x(idx)
                cell_y = func_cell_y(idx)
                self.map.updateCell(position=(cell_x, cell_y), celltype=celltype, turn=self.turn)
        if direction == LEFT:
            # 1列目
            _update(lambda idx: self.x - 3 + idx, lambda idx: self.y + 1, info[:3])
            # 2列目
            _update(lambda idx: self.x - 3 + idx, lambda idx: self.y, info[3:6])
            # 3列目
            _update(lambda idx: self.x - 3 + idx, lambda idx: self.y - 1, info[6:9])
        elif direction == RIGHT:
            # 1列目
            _update(lambda idx: self.x + 1 + idx, lambda idx: self.y + 1, info[:3])
            # 2列目
            _update(lambda idx: self.x + 1 + idx, lambda idx: self.y, info[3:6])
            # 3列目
            _update(lambda idx: self.x + 1 + idx, lambda idx: self.y - 1, info[6:9])
        elif direction == UP:
            # 1列目
            _update(lambda idx: self.x - 1 + idx, lambda idx: self.y + 3, info[:3])
            # 2列目
            _update(lambda idx: self.x - 1 + idx, lambda idx: self.y + 2, info[3:6])
            # 3列目
            _update(lambda idx: self.x - 1 + idx, lambda idx: self.y + 1, info[6:9])
        elif direction == DOWN:
            # 1列目
            _update(lambda idx: self.x - 1 + idx, lambda idx: self.y - 3, info[:3])
            # 2列目
            _update(lambda idx: self.x - 1 + idx, lambda idx: self.y - 2, info[3:6])
            # 3列目
            _update(lambda idx: self.x - 1 + idx, lambda idx: self.y - 1, info[6:9])

    def _update_map_search(self, info, direction):
        """
        searchコマンドの情報でマップを更新
        direction: 方向
        """
        def _update(func_cell_x, func_cell_y):
            for idx, celltype in enumerate(info):
                cell_x = func_cell_x(idx)
                cell_y = func_cell_y(idx)
                self.map.updateCell(position=(cell_x, cell_y), celltype=celltype, turn=self.turn)
        if direction == LEFT:
            _update(lambda idx: self.x - 1 - idx, lambda idx: self.y)
        elif direction == RIGHT:
            _update(lambda idx: self.x + 1 + idx, lambda idx: self.y)
        elif direction == UP:
            _update(lambda idx: self.x, lambda idx: self.y + 1 + idx)
        elif direction == DOWN:
            _update(lambda idx: self.x, lambda idx: self.y - 1 - idx)

    ################
    # 補助コマンド
    ################
    def username(self):
        return self.command(self._username)

    def getReady(self):
        self.command('gr')
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def turnEnd(self):
        self.command('#')

    ################
    # 移動系
    ################
    def walkRight(self):
        self.command('wr')
        self.x += 1
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def walkLeft(self):
        self.command('wl')
        self.x -= 1
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def walkUp(self):
        self.command('wu')
        self.y += 1
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def walkDown(self):
        self.command('wd')
        self.y -= 1
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    ################
    # 広範囲探索
    ################
    def lookRight(self):
        self.command('lr')
        info = self.receive_info()
        self._update_map_look(info, RIGHT)
        return info

    def lookLeft(self):
        self.command('ll')
        info = self.receive_info()
        self._update_map_look(info, LEFT)
        return info

    def lookUp(self):
        self.command('lu')
        info = self.receive_info()
        self._update_map_look(info, UP)
        return info

    def lookDown(self):
        self.command('ld')
        info = self.receive_info()
        self._update_map_look(info, DOWN)
        return info

    ################
    # 前方探索
    ################
    def searchRight(self):
        self.command('sr')
        info = self.receive_info()
        self._update_map_search(info, RIGHT)
        return info

    def searchLeft(self):
        self.command('sl')
        info = self.receive_info()
        self._update_map_search(info, LEFT)
        return info

    def searchUp(self):
        self.command('su')
        info = self.receive_info()
        self._update_map_search(info, UP)
        return info

    def searchDown(self):
        self.command('sd')
        info = self.receive_info()
        self._update_map_search(info, DOWN)
        return info

    ################
    # ブロック設置
    ################
    def putRight(self):
        self.command('pr')
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def putLeft(self):
        self.command('pl')
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def putUp(self):
        self.command('pu')
        info = self.receive_info()
        self._update_map_normal(info)
        return info

    def putDown(self):
        self.command('pd')
        info = self.receive_info()
        self._update_map_normal(info)
        return info

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
                    # ターン情報更新
                    self.turn += 1
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
