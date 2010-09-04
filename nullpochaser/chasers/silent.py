from nullpochaser.chasers import CHaser
from nullpochaser.const import TYPE_ENEMY

class SilentChaser(CHaser):
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
