from pico2d import *
from BOTTLE import BOTTLE
import random

class BOSS():
    TYPE = 'BOSS'
    DIRECT_LEFT, DIRECT_RIGHT, DIRECT_UP, DIRECT_DOWN = 0, 1, 2, 3
    STATE_WALK, STATE_ANGRY, STATE_DEAD, STATE_AFRAID = 9, 7, 5, None
    STATE_STUCK_GREEN, STATE_STUCK_YELLOW, STATE_STUCK_RED, STATE_PON, STATE_NONE = None, None, 3, 1, 99
    PIXEL_PER_METER = (10.0 / 0.3)
    MOVE_SPEED_KMPH = 14.0
    XSIZE, YSIZE = 300, 380
    sprite = None
    sounds = None
    def __init__(self, x ,y):
        self.stayTime = 6.0
        self.x = x
        self.y = y
        self.health = 25
        self.change_moveSpeed()
        self.isAttack = 0
        self.direct = random.randint(0, 1)
        self.yDirect = random.randint(2, 3)
        self.state = self.STATE_WALK
        self.frame, self.totalFrame = 0, 0
        self.actionPerTime = 0.0
        self.frameTime = 0.0
        self.stateTemp = None
        if BOSS.sprite == None:
            BOSS.sprite = load_image('sprite\\Enemy\\boss.png')
        if BOSS.sounds == None:
            BOSS.sounds = load_wav('GameSound\\Character\\bossAttack.wav')
            BOSS.sounds.set_volume(32)
        self.xSprite = 64
        self.ySprite = 64
        self.numSprite = 8
        self.change_actionPerTime()


    def change_moveSpeed(self):
        moveSpeedMPM = self.MOVE_SPEED_KMPH * 1000.0 / 60.0
        moveSpeedMPS = moveSpeedMPM / 60.0
        self.moveSpeedPPS = moveSpeedMPS * self.PIXEL_PER_METER


    def change_actionPerTime(self):
        if self.state == self.STATE_STUCK_RED:
            timePerAction = 2.5
        else:
            timePerAction = 1.5


        self.actionPerTime = 1.0 / timePerAction


    def get_bb(self):
        return self.x - self.XSIZE * 3 / 9, self.y - self.YSIZE / 2, self.x + self.XSIZE * 3 / 9, self.y + self.YSIZE * 3 / 9


    def get_bb_left(self):
        return self.x - self.XSIZE * 3 / 9


    def get_bb_right(self):
        return self.x + self.XSIZE * 3 / 9


    def get_bb_top(self):
        return self.y + self.YSIZE * 3 / 9


    def get_bb_bottom(self):
        return self.y - self.YSIZE / 2


    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def handle_walk(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
                self.isAttack = 5
                self.sounds.play()
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
                self.isAttack = 5
                self.sounds.play()
        if self.yDirect == self.DIRECT_UP:
            self.y = min(675 - self.YSIZE / 2, self.y + self.moveSpeedPPS * self.frameTime)
            if self.y == 675 - self.YSIZE / 2:
                self.yDirect = self.DIRECT_DOWN
        elif self.yDirect == self.DIRECT_DOWN:
            self.y = max(self.YSIZE / 2 + 25, self.y - self.moveSpeedPPS * self.frameTime)
            if self.y == self.YSIZE / 2 + 25:
                self.yDirect = self.DIRECT_UP



    def handle_angry(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime * 1.5)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
                self.isAttack = 5
                self.sounds.play()
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime * 1.5)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
                self.isAttack = 5
                self.sounds.play()
        if self.yDirect == self.DIRECT_UP:
            self.y = min(675 - self.YSIZE / 2, self.y + self.moveSpeedPPS * self.frameTime * 1.5)
            if self.y == 675 - self.YSIZE / 2:
                self.yDirect = self.DIRECT_DOWN
        elif self.yDirect == self.DIRECT_DOWN:
            self.y = max(self.YSIZE / 2 + 25, self.y - self.moveSpeedPPS * self.frameTime * 1.5)
            if self.y == self.YSIZE / 2 + 25:
                self.yDirect = self.DIRECT_UP


    def handle_dead(self):
        if self.direct == self.DIRECT_LEFT:
            self.x = max(self.XSIZE/2 + 50, self.x - self.moveSpeedPPS * self.frameTime)
            if self.x == self.XSIZE/2 + 50:
                self.direct = self.DIRECT_RIGHT
        elif self.direct == self.DIRECT_RIGHT:
            self.x = min(1200 - self.XSIZE/2 - 50, self.x + self.moveSpeedPPS * self.frameTime)
            if self.x == 1200 - self.XSIZE/2 - 50:
                self.direct = self.DIRECT_LEFT
        self.y += self.moveSpeedPPS * self.frameTime * 0.5
        if 999 <= self.totalFrame:
            self.state = self.STATE_NONE


    def handle_stuck(self):
        if 25 <= self.totalFrame:
            self.frame = self.totalFrame = 0
            self.state = self.STATE_ANGRY
            self.health = 10
            self.direct = random.randint(0, 1)
            self.change_actionPerTime()


    def handle_pon(self):
        if self.frame == 4:
            self.state = self.STATE_DEAD


    def handle_none(self):
        pass


    handle_state = {
        STATE_WALK: handle_walk,
        STATE_ANGRY: handle_angry,
        STATE_DEAD: handle_dead,
        STATE_STUCK_RED: handle_stuck,
        STATE_PON: handle_pon,
        STATE_NONE: handle_none
    }


    def update(self, frameTime):
        self.frameTime = frameTime
        #change frames
        self.totalFrame += self.numSprite * self.actionPerTime * self.frameTime
        self.frame = int(self.totalFrame) % self.numSprite
        #change state
        if self.stayTime == 0:
            self.handle_state[self.state](self)
        else:
            self.stayTime -= frameTime
            if self.stayTime < 0:
                self.stayTime = 0
        # make attack
        if 0 < self.isAttack:
            self.isAttack -= 1
            if self.direct == self.DIRECT_LEFT:
                return BOTTLE(self.x - self.XSIZE / 2, self.y, ((-1)**self.isAttack) * (self.isAttack/4), self.direct)
            else:
                return BOTTLE(self.x + self.XSIZE / 2, self.y, ((-1)**self.isAttack) * (self.isAttack/4), self.direct)


    def draw(self):
        self.sprite.clip_draw(self.xSprite * self.frame, self.ySprite * (self.state - self.direct), self.xSprite, self.ySprite, self.x, self.y, self.XSIZE, self.YSIZE)


    def isPop(self):
        if self.state == self.STATE_NONE:
            return True
        else:
            return False