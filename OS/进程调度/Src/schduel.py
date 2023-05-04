import time
import queue
import threading
import PyQt6.QtCore as QtC
from PyQt6.QtCore import QThread, QTimer

import ui_elevator as ui
import Main_Window as M_w

Lock_1 = threading.Lock()

INF = 999
maxFloor = 20  # 最高楼层

floor = 1  # 楼层数 [1,20]
inGuestFloor = None  # 内部用户目标楼层
wantUp = 0  # 用户上行
wantDown = 0  # 用户下行

# 首先，定义状态
warning = 1  # 警报状态 for 报警按钮
openDoor = 1  # 开门状态 for 开门按钮 & 抵达目标
closeDoor = 0  # 关门状态 for 关门按钮 & 上/行 默认
upGoing = 1  # 上行状态
downGoing = 2  # 下行状态
static = 0  # 静止状态 默认

freshTime = 0.1


def renewMessage(elevator_, level):
    if level > elevator_.nowFloor:
        elevator_.upDestination.put([level, level])
    elif level < elevator_.nowFloor:
        elevator_.downDestination.put([maxFloor - level, level])  # ([优先级,元素])


def tofloor_outside(elevator_, level, index):  # producer
    renewMessage(elevator_, level)
    if elevator_.status == static:
        if elevator_.upDestination.empty() and not elevator_.downDestination.empty():
            thread = threading.Thread(target=isdown_outside, args=[elevator_, index])
            thread.start()
        elif elevator_.downDestination.empty() and not elevator_.upDestination.empty():
            thread = threading.Thread(target=isup_outside, args=[elevator_, index])
            thread.start()


def isup_outside(elevator_, index):  # consumer
    if not elevator_.status == upGoing:
        elevator_.status = upGoing
    elevator_.emitWay(index, elevator_.status)
    while not elevator_.upDestination.empty():
        while elevator_.nowFloor != elevator_.upDestination.queue[0][1] and elevator_.status == upGoing:
            time.sleep(freshTime)  # 如果在上升，那么0.1秒上升一层
            elevator_.nowFloor += 1
            print(elevator_.nowFloor)
            elevator_.chooseToEmit(index)
        elevator_.emitFloor()
        elevator_.upDestination.get()
        time.sleep(freshTime * 5)
        elevator_.status = upGoing
    elevator_.status = static
    elevator_.emitWay(index, elevator_.status)
    if not elevator_.downDestination.empty():
        elevator_.status = upGoing
        thread = threading.Thread(target=isdown_outside, args=[elevator_, index])
        thread.start()
        thread.join()


def isdown_outside(elevator_, index):  # consumer
    if not elevator_.status == downGoing:
        elevator_.status = downGoing
    elevator_.emitWay(index, elevator_.status)
    while not elevator_.downDestination.empty():
        while elevator_.nowFloor != elevator_.downDestination.queue[0][1] and elevator_.status == downGoing:
            time.sleep(freshTime)  # 如果在下降，那么0.1秒下降一层
            elevator_.nowFloor -= 1
            print(elevator_.nowFloor)
            elevator_.chooseToEmit(index)
        elevator_.emitFloor()
        elevator_.downDestination.get()
        time.sleep(freshTime * 5)
        elevator_.status = downGoing
    elevator_.status = static
    elevator_.emitWay(index, elevator_.status)
    if not elevator_.upDestination.empty():
        elevator_.status = upGoing
        thread = threading.Thread(target=isup_outside, args=[elevator_, index])
        thread.start()
        thread.join()
        
def isclose_outside(elevator_, index):
    elevator_.statusDoor = closeDoor
    print("in close")
    if index == 1:
        elevator_.door_1.emit("关门")
    elif index == 2:
        elevator_.door_2.emit("关门")
    elif index == 3:
        elevator_.door_3.emit("关门")
    elif index == 4:
        elevator_.door_4.emit("关门")
    elif index == 5:
        elevator_.door_5.emit("关门")
    time.sleep(freshTime * 5)
    if index == 1:
        elevator_.door_1.emit("待机")
    elif index == 2:
        elevator_.door_2.emit("待机")
    elif index == 3:
        elevator_.door_3.emit("待机")
    elif index == 4:
        elevator_.door_4.emit("待机")
    elif index == 5:
        elevator_.door_5.emit("待机")


class elevator(QThread):
    timer = QTimer()

    floor_1 = QtC.pyqtSignal(int, name="floor_1")
    floor_2 = QtC.pyqtSignal(int, name="floor_2")
    floor_3 = QtC.pyqtSignal(int, name="floor_3")
    floor_4 = QtC.pyqtSignal(int, name="floor_4")
    floor_5 = QtC.pyqtSignal(int, name="floor_5")
    door_1 = QtC.pyqtSignal(str, name="door_1")
    door_2 = QtC.pyqtSignal(str, name="door_2")
    door_3 = QtC.pyqtSignal(str, name="door_3")
    door_4 = QtC.pyqtSignal(str, name="door_4")
    door_5 = QtC.pyqtSignal(str, name="door_5")
    direction_1 = QtC.pyqtSignal(str, name="direction_1")
    direction_2 = QtC.pyqtSignal(str, name="direction_2")
    direction_3 = QtC.pyqtSignal(str, name="direction_3")
    direction_4 = QtC.pyqtSignal(str, name="direction_4")
    direction_5 = QtC.pyqtSignal(str, name="direction_5")
    switch = QtC.pyqtSignal(int, name="switch")
    # 共享电梯楼层信息：
    shareMessage = set()

    def __init__(self):
        super().__init__()
        self.status = static
        self.statusDoor = closeDoor
        self.nowFloor = 1  # 电梯所在楼层 默认为1层
        # 此为不互联的电梯消息队列：
        self.upDestination = queue.PriorityQueue(20)  # 上行终点队列
        self.downDestination = queue.PriorityQueue(20)  # 下行终点队列

    def toFloor(self, level, index):  # 内部用户调度电梯 要并发
        if level in self.shareMessage:
            return
        else:
            self.shareMessage.add(level)
        thread = threading.Thread(target=tofloor_outside, args=[self, level, index])
        print("Elevator Start")
        thread.start()

    def renewQueue(self, level):
        if level in self.shareMessage:
            return
        else:
            self.shareMessage.add(level)
        thread = threading.Thread(target=renewMessage, args=[self, level])
        print("renew start")
        thread.start()

    def refresh(self):
        if self.upDestination.empty() and self.downDestination.empty():
            self.status = static
        elif not self.upDestination.empty():
            self.status = upGoing
        elif not self.downDestination.empty():
            self.status = downGoing

    def chooseToEmit(self, index):
        print("emit start")
        if index == 1:
            self.floor_1.emit(self.nowFloor)
        elif index == 2:
            self.floor_2.emit(self.nowFloor)
        elif index == 3:
            self.floor_3.emit(self.nowFloor)
        elif index == 4:
            self.floor_4.emit(self.nowFloor)
        elif index == 5:
            self.floor_5.emit(self.nowFloor)
        print("emit pass")

    def emitFloor(self):
        self.switch.emit(self.nowFloor)
        
    def emitWay(self, index, how):
        if index == 1:
            if how == upGoing:
                self.direction_1.emit("上行")
            elif how == downGoing:
                self.direction_1.emit("下行")
            elif how == static:
                self.direction_1.emit("待机")
        elif index == 2:
            if how == upGoing:
                self.direction_2.emit("上行")
            elif how == downGoing:
                self.direction_2.emit("下行")
            elif how == static:
                self.direction_2.emit("待机")
        elif index == 3:
            if how == upGoing:
                self.direction_3.emit("上行")
            elif how == downGoing:
                self.direction_3.emit("下行")
            elif how == static:
                self.direction_3.emit("待机")
        elif index == 4:
            if how == upGoing:
                self.direction_4.emit("上行")
            elif how == downGoing:
                self.direction_4.emit("下行")
            elif how == static:
                self.direction_4.emit("待机")
        elif index == 5:
            if how == upGoing:
                self.direction_5.emit("上行")
            elif how == downGoing:
                self.direction_5.emit("下行")
            elif how == static:
                self.direction_5.emit("待机")

    def isWarning(self, index):  # 进入停运状态（警报触发）
        self.status = warning
        if index == 1:
            self.door_1.emit("禁用")
        elif index == 2:
            self.door_2.emit("禁用")
        elif index == 3:
            self.door_3.emit("禁用")
        elif index == 4:
            self.door_4.emit("禁用")
        elif index == 5:
            self.door_5.emit("禁用")

    def isOpen(self, index):
        self.statusDoor = openDoor
        if index == 1:
            self.door_1.emit("开门")
        elif index == 2:
            self.door_2.emit("开门")
        elif index == 3:
            self.door_3.emit("开门")
        elif index == 4:
            self.door_4.emit("开门")
        elif index == 5:
            self.door_5.emit("开门")

    def isClose(self, index):
        thread = threading.Thread(target=isclose_outside, args=[self, index])
        thread.start()


arrayElevator = [elevator() for _ in range(5)]
# 一些想法：
# 电梯本身是互斥资源，但是互斥量为5
mutexElevateSrc = 5
# 但对于单个电梯自身也是互斥的
mutexEach = 1

dist = INF


# 外部用户请求电梯:

def iWantAElevator(howtogo, outguestfloor):  # 请求一部电梯  请求时附带上/下行参数——这个参数可以考虑精简 producer
    global dist
    bestElevator = elevator()
    # 针对从同一楼层发出的请求，电梯都可以接收
    # 但是会优先调度距离发起请求的楼层最近的电梯
    # 前提是无故障，即未进入warning状态
    # 那么如果5台都满足以上调度条件，则如何选择电梯？
    # 1. 人数非满
    # 2. 距离最近 √
    # 换句话说，调度的条件有3：
    Lock_1.acquire()
    for E in arrayElevator:
        if not E.status == warning:
            if E.nowFloor < outguestfloor and E.status == upGoing and howtogo == wantUp:
                # 对于当前电梯执行的任务出现优先级调度
                # 优先度根据电梯与请求楼层的距离来定义，越小则优先级越高
                if dist > outguestfloor - E.nowFloor:  # 循环迭代计算最小者
                    dist = outguestfloor - E.nowFloor
                    bestElevator = E
            if E.nowFloor > outguestfloor and E.status == downGoing and howtogo == wantDown:
                if dist > outguestfloor - E.nowFloor:  # 循环迭代计算最小者
                    dist = outguestfloor - E.nowFloor
                    bestElevator = E
    Lock_1.release()
    bestElevator.start()
    if bestElevator.status == static:
        bestElevator.toFloor(outguestfloor)  # 决定最优电梯后，调度该电梯 同时切换电梯状态
    else:
        bestElevator.renewQueue(outguestfloor)
