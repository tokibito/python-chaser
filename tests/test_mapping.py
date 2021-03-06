import pytest

from chaser import const


class TestMapCell:
    @pytest.fixture
    def target(self):
        from chaser.mapping import MapCell as target
        return target

    def test_property(self, target):
        cell = target(const.TYPE_FLOOR, 1)
        assert cell.celltype == const.TYPE_FLOOR
        assert cell.turn == 1

    def test_is_floor(self, target):
        cell = target(const.TYPE_FLOOR, 1)
        assert cell.is_floor()
        assert not cell.is_character()
        assert not cell.is_block()
        assert not cell.is_item()

    def test_is_character(self, target):
        cell = target(const.TYPE_CHARACTER, 1)
        assert not cell.is_floor()
        assert cell.is_character()
        assert not cell.is_block()
        assert not cell.is_item()

    def test_is_block(self, target):
        cell = target(const.TYPE_BLOCK, 1)
        assert not cell.is_floor()
        assert not cell.is_character()
        assert cell.is_block()
        assert not cell.is_item()

    def test_is_item(self, target):
        cell = target(const.TYPE_ITEM, 1)
        assert not cell.is_floor()
        assert not cell.is_character()
        assert not cell.is_block()
        assert cell.is_item()

    def update(self, target):
        cell = target(const.TYPE_FLOOR, 1)
        cell.update(const.TYPE_BLOCK, 2)
        assert cell.celltype == const.TYPE_BLOCK
        assert cell.history[0] == (const.TYPE_FLOOR, 1)


class TestMap:
    @pytest.fixture
    def target(self):
        from chaser.mapping import Map as target
        return target

    def test_str(self, target):
        map = target()
        actual = str(map)
        expected = "_"
        assert actual == expected

    def test_add_surround(self, target):
        map = target()
        map.add_surround((0, 0), [0, 1, 2, 3, 0, 0, 0, 0, 0], 1)
        actual = map.as_text((0, 0))
        expected = "_EX\n*#_\n___"
        assert actual == expected
