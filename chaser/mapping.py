from . import const


class MapCell:
    """
    マップの1セルの情報

    更新履歴を持ちます
    """
    def __init__(self, celltype, turn):
        """
        :param celltype: セルの種別
        :param turn: 何ターン目か
        """
        self._celltype = celltype
        self._turn = turn
        self.history = []

    @property
    def celltype(self):
        return self._celltype

    @property
    def turn(self):
        return self._turn

    def is_floor(self):
        """マップパーツ: 床
        """
        return self._celltype == const.TYPE_FLOOR

    def is_character(self):
        """マップパーツ: キャラクタ
        """
        return self._celltype == const.TYPE_CHARACTER

    def is_block(self):
        """マップパーツ: ブロック
        """
        return self._celltype == const.TYPE_BLOCK

    def is_item(self):
        """マップパーツ: アイテム
        """
        return self._celltype == const.TYPE_ITEM

    def update(self, celltype, turn):
        """セルの情報を更新
        """
        # 現在のセル情報を履歴へ追加
        self.history.append((self._celltype, self.turn))
        # 新しい情報に更新
        self._celltype = celltype
        self._turn = turn


class Map(dict):
    """
    マップ情報を管理するためのクラス
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        # 開始時、(0, 0)床
        self[(0, 0)] = MapCell(const.TYPE_FLOOR, 0)

    @property
    def top(self):
        """保持している座標のY方向の最大値(上方)
        """
        return max([p[1] for p in self])

    @property
    def bottom(self):
        """保持している座標のY方向の最小値(下方)
        """
        return min([p[1] for p in self])

    @property
    def left(self):
        """保持している座標のX方向の最小値(左方)
        """
        return min([p[0] for p in self])

    @property
    def right(self):
        """保持している座標のX方向の最大値(右方)
        """
        return max([p[0] for p in self])

    @property
    def width(self):
        """マップの幅を返します

        保持している座標のX方向の範囲
        """
        return self.right - self.left + 1

    @property
    def height(self):
        """マップの高さを返します

        保持している座標のY方向の範囲
        """
        return self.top - self.bottom + 1

    def add(self, position, celltype, turn):
        """マップに情報を追加します
        """
        if position in self:
            cell = self[position]
            cell.update(celltype, turn)
        else:
            self[position] = MapCell(celltype, turn)

    def add_surround(self, self_position, info, turn):
        """周囲情報をマップに追加します
        """
        cursor = 0
        left = self_position[0] - 1
        top = self_position[1] + 1
        for y_increment in [0, 1, 2]:
            for x_increment in [0, 1, 2]:
                position = (left + x_increment, top - y_increment)
                self.add(position, info[cursor], turn)
                cursor += 1

    def as_text(self, self_postion=None):
        """
        文字列表現でマップを返す

        X: 壁
        E: 敵
        #: 自キャラクター(self_postionを指定した場合)
        *: アイテム
        _: 床
        空白: 情報なし
        """
        lines = []
        top = self.top
        left = self.left
        for y_increment in range(self.height):
            line = ""
            for x_increment in range(self.width):
                position = (left + x_increment, top - y_increment)
                cell = self.get(position)
                if position == self_postion:
                    out = "#"
                elif cell is None:
                    out = " "
                elif cell.is_floor():
                    out = "_"
                elif cell.is_character():
                    out = "E"
                elif cell.is_block():
                    out = "X"
                elif cell.is_item():
                    out = "*"
                line += out
            lines.append(line)
        return "\n".join(lines)

    def __str__(self):
        return self.as_text()
