# coding: utf-8
from nullpochaser.const import TYPE_FLOOR, TYPE_BLOCK, TYPE_ITEM

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

    def update(self, celltype, turn):
        self.history.append((self.celltype, self.turn))
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
