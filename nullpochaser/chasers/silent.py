from nullpochaser.chasers import CHaser
from nullpochaser.const import TYPE_ENEMY

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
            self.searchLeft()
        print 'turn: %d, map size: %d x %d' % (self.turn, self.map.width, self.map.height)
        print self.map.displayText()
