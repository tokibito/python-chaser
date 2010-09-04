from nullpochaser.chasers import CHaser
from nullpochaser.const import TYPE_ENEMY
from random import choice

class SilentCHaser(CHaser):
    def run(self, info):
        if info[1] == TYPE_ENEMY:
            self.putUp()
        elif info[3] == TYPE_ENEMY:
            self.putLeft()
        elif info[5] == TYPE_ENEMY:
            self.putRight()
        elif info[7] == TYPE_ENEMY:
            self.putDown()
        else:
            i = choice(range(8))
            if i == 0:
                self.searchLeft()
            elif i == 1:
                self.searchRight()
            elif i == 2:
                self.searchUp()
            elif i == 3:
                self.searchDown()
            elif i == 4:
                self.lookLeft()
            elif i == 5:
                self.lookRight()
            elif i == 6:
                self.lookUp()
            else:
                self.lookDown()
        print 'turn: %d, map size: %d x %d' % (self.turn, self.map.width, self.map.height)
        print self.map.displayText(position_self=self.position)
