# coding: utf-8
import random

from nullpochaser.chasers import CHaser
from nullpochaser.const import TYPE_ENEMY, TYPE_BLOCK

WALK_UP = 1
WALK_LEFT = 2
WALK_RIGHT = 3
WALK_DOWN = 4

class ActiveCHaser(CHaser):
    def safe_walk(self, info, direction):
        # �ǂ��Ȃ���Ύw������֐i��
        if direction == WALK_UP:
            if info[1] == TYPE_BLOCK:
                return False
            return self.walkUp()
        elif direction == WALK_LEFT:
            if info[3] == TYPE_BLOCK:
                return False
            return self.walkLeft()
        elif direction == WALK_RIGHT:
            if info[5] == TYPE_BLOCK:
                return False
            return self.walkRight()
        elif direction == WALK_DOWN:
            if info[7] == TYPE_BLOCK:
                return False
            return self.walkDown()

    def run(self, info):
        # �ŗD��:���ɂ�����u���b�N�u��
        if info[1] == TYPE_ENEMY:
            self.putUp()
        elif info[3] == TYPE_ENEMY:
            self.putLeft()
        elif info[5] == TYPE_ENEMY:
            self.putRight()
        elif info[7] == TYPE_ENEMY:
            self.putDown()
        else:
            # �����_���ŕǂ̂Ȃ�������
            # 1: ��, 2: ��, 3: �E, 4: ��
            while True:
                val = random.randint(1, 4)
                result = self.safe_walk(info, val)
                if result:
                    break
