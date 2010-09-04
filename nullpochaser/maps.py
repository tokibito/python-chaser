# coding: utf-8
from nullpochaser.const import TYPE_FLOOR, TYPE_ENEMY, TYPE_BLOCK, TYPE_ITEM

# 履歴は多すぎても多分意味ないので
MAX_HISTORY_COUNT = 5

class MapCell(object):
    """
    マップの1セルの情報
    いつ更新されたかと更新履歴を持つ
    """
    def __init__(self, celltype, turn):
        self._celltype = celltype
        self._turn = turn
        self.history = []

    @property
    def celltype(self):
        return self._celltype

    @property
    def turn(self):
        return self._turn

    @property
    def is_floor(self):
        return self.celltype == TYPE_FLOOR

    @property
    def is_enemy(self):
        return self.celltype == TYPE_ENEMY

    @property
    def is_block(self):
        return self.celltype == TYPE_BLOCK

    @property
    def is_item(self):
        return self.celltype == TYPE_ITEM

    def update(self, celltype, turn):
        self.history.append((self.celltype, self.turn))
        # 最大数を超えないように切り詰め
        self.history = self.history[len(self.history) - MAX_HISTORY_COUNT:]
        self._celltype = celltype
        self._turn = turn

class CHaserMap(object):
    """
    フィールドマップ
    """
    def __init__(self):
        self.data = {
            (0, 0): TYPE_FLOOR,
        }

    def getXList(self):
        """
        マッピング済みのX座標のリストを返す
        """
        return sorted([position[0] for position in self.data])

    def getYList(self):
        """
        マッピング済みのY座標のリストを返す
        """
        return sorted([position[1] for position in self.data])

    def getLeft(self):
        """
        一番左のX座標
        """
        return min(self.getXList())

    def getRight(self):
        """
        一番右のX座標
        """
        return max(self.getXList())

    def getUp(self):
        """
        一番上のY座標
        """
        return max(self.getYList())

    def getDown(self):
        """
        一番下のY座標
        """
        return min(self.getYList())

    def getWidth(self):
        """
        マップの幅
        """
        return self.getRight() - self.getLeft() + 1
    width = property(getWidth)

    def getHeight(self):
        """
        マップの高さ
        """
        return self.getUp() - self.getDown() + 1
    height = property(getHeight)

    def getCell(self, position, gt_turn=None):
        """
        指定位置の情報を取得
        gt_turnを指定すると指定ターン以前の場合はNoneを返す
        """
        cell = self.data.get(position)
        if gt_turn and cell and cell.turn < gt_turn:
            return
        return cell

    def updateCell(self, position, celltype, turn):
        """
        指定位置の情報を更新
        """
        cell = self.getCell(position)
        if not cell:
            self.data[position] = MapCell(celltype, turn)
        else:
            cell.update(celltype, turn)

    def displayText(self, gt_turn=None):
        """
        文字列表現でマップを返す
        X: 壁
        E: 敵
        *: アイテム
        空白: 床
        #: 情報なし
        """
        # マップの上下左右取得
        l, r, u, d = self.getLeft(), self.getRight(), self.getUp(), self.getDown()
        text = ''
        # 左上から生成
        for y in reversed(range(d, u + 1)):
            for x in range(l, r + 1):
                cell = self.getCell((x, y), gt_turn=gt_turn)
                if not cell:
                    text += '?'
                elif cell.is_floor:
                    text += '_'
                elif cell.is_enemy:
                    text += 'E'
                elif cell.is_block:
                    text += 'X'
                elif cell.is_item:
                    text += '*'
            text += '\n'
        return text
