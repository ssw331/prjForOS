import PyQt6.QtCore as QtC
import PyQt6.QtWidgets as QtW
import parse

import ui_elevator as ui
import schduel

index = 1
# 首先，定义状态
warning = 1  # 警报状态 for 报警按钮
openDoor = 1  # 开门状态 for 开门按钮 & 抵达目标
closeDoor = 0  # 关门状态 for 关门按钮 & 上/行 默认
upGoing = 1  # 上行状态
downGoing = 2  # 下行状态
static = 0  # 静止状态 默认


# 剩余工作：
# 1. 上下行提示


class M_Window(QtW.QMainWindow):
    # 警告 这里定义的东西是被各个对象共享的
    signal_1 = QtC.pyqtSignal(int, name="signal_1")
    signal_2 = QtC.pyqtSignal(int, name="signal_2")
    signal_3 = QtC.pyqtSignal(int, name="signal_3")
    signal_4 = QtC.pyqtSignal(int, name="signal_4")
    signal_5 = QtC.pyqtSignal(int, name="signal_5")
    doorsignal_1 = QtC.pyqtSignal(str, name="doorsignal_1")
    doorsignal_2 = QtC.pyqtSignal(str, name="doorsignal_2")
    doorsignal_3 = QtC.pyqtSignal(str, name="doorsignal_3")
    doorsignal_4 = QtC.pyqtSignal(str, name="doorsignal_4")
    doorsignal_5 = QtC.pyqtSignal(str, name="doorsignal_5")
    directsignal_1 = QtC.pyqtSignal(int, name="signal_1")
    directsignal_2 = QtC.pyqtSignal(int, name="signal_2")
    directsignal_3 = QtC.pyqtSignal(int, name="signal_3")
    directsignal_4 = QtC.pyqtSignal(int, name="signal_4")
    directsignal_5 = QtC.pyqtSignal(int, name="signal_5")
    forswitch_1 = QtC.pyqtSignal(int, name="forswitch_1")
    forswitch_2 = QtC.pyqtSignal(int, name="forswitch_2")
    forswitch_3 = QtC.pyqtSignal(int, name="forswitch_3")
    forswitch_4 = QtC.pyqtSignal(int, name="forswitch_4")
    forswitch_5 = QtC.pyqtSignal(int, name="forswitch_5")
    howToGo = QtC.pyqtSignal(int)
    whereToGo = QtC.pyqtSignal(int)
    E = [schduel.elevator() for _n in range(5)]  # 准备5个电梯线程

    def __init__(self):
        super().__init__()
        self.ui = ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.signal_1 = self.E[0].floor_1
        self.signal_2 = self.E[1].floor_2
        self.signal_3 = self.E[2].floor_3
        self.signal_4 = self.E[3].floor_4
        self.signal_5 = self.E[4].floor_5
        self.doorsignal_1 = self.E[0].door_1
        self.doorsignal_2 = self.E[1].door_2
        self.doorsignal_3 = self.E[2].door_3
        self.doorsignal_4 = self.E[3].door_4
        self.doorsignal_5 = self.E[4].door_5
        self.directsignal_1 = self.E[0].direction_1
        self.directsignal_2 = self.E[1].direction_2
        self.directsignal_3 = self.E[2].direction_3
        self.directsignal_4 = self.E[3].direction_4
        self.directsignal_5 = self.E[4].direction_5
        self.signal_1.connect(self.ui.lcdNumber_1.display)
        self.signal_2.connect(self.ui.lcdNumber_2.display)
        self.signal_3.connect(self.ui.lcdNumber_3.display)
        self.signal_4.connect(self.ui.lcdNumber_4.display)
        self.signal_5.connect(self.ui.lcdNumber_5.display)
        self.doorsignal_1.connect(self.ui.textBrowser_6.setText)
        self.doorsignal_2.connect(self.ui.textBrowser_7.setText)
        self.doorsignal_3.connect(self.ui.textBrowser_8.setText)
        self.doorsignal_4.connect(self.ui.textBrowser_9.setText)
        self.doorsignal_5.connect(self.ui.textBrowser_10.setText)
        self.directsignal_1.connect(self.ui.textBrowser_6.setText)
        self.directsignal_2.connect(self.ui.textBrowser_7.setText)
        self.directsignal_3.connect(self.ui.textBrowser_8.setText)
        self.directsignal_4.connect(self.ui.textBrowser_9.setText)
        self.directsignal_5.connect(self.ui.textBrowser_10.setText)
        self.forswitch_1 = self.E[0].switch
        self.forswitch_2 = self.E[1].switch
        self.forswitch_3 = self.E[2].switch
        self.forswitch_4 = self.E[3].switch
        self.forswitch_5 = self.E[4].switch
        self.ui.pushButton_0.clicked.connect(self.needAElevator)
        self.ui.pushButton_116.clicked.connect(self.needAElevator)

        for thread in self.E:
            thread.start()
        self.floors = [(self.ui.pushButton_1, self.ui.pushButton_2, self.ui.pushButton_3, self.ui.pushButton_4,
                        self.ui.pushButton_5, self.ui.pushButton_6, self.ui.pushButton_7, self.ui.pushButton_8,
                        self.ui.pushButton_9, self.ui.pushButton_10, self.ui.pushButton_11, self.ui.pushButton_12,
                        self.ui.pushButton_13, self.ui.pushButton_14, self.ui.pushButton_15, self.ui.pushButton_16,
                        self.ui.pushButton_17, self.ui.pushButton_18, self.ui.pushButton_19, self.ui.pushButton_20),
                       (self.ui.pushButton_21, self.ui.pushButton_22, self.ui.pushButton_23, self.ui.pushButton_24,
                        self.ui.pushButton_25, self.ui.pushButton_26, self.ui.pushButton_27, self.ui.pushButton_28,
                        self.ui.pushButton_29, self.ui.pushButton_30, self.ui.pushButton_31, self.ui.pushButton_32,
                        self.ui.pushButton_33, self.ui.pushButton_34, self.ui.pushButton_35, self.ui.pushButton_36,
                        self.ui.pushButton_37, self.ui.pushButton_38, self.ui.pushButton_39, self.ui.pushButton_40),
                       (self.ui.pushButton_41, self.ui.pushButton_42, self.ui.pushButton_43, self.ui.pushButton_44,
                        self.ui.pushButton_45, self.ui.pushButton_46, self.ui.pushButton_47, self.ui.pushButton_48,
                        self.ui.pushButton_49, self.ui.pushButton_50, self.ui.pushButton_51, self.ui.pushButton_52,
                        self.ui.pushButton_53, self.ui.pushButton_54, self.ui.pushButton_55, self.ui.pushButton_56,
                        self.ui.pushButton_57, self.ui.pushButton_58, self.ui.pushButton_59, self.ui.pushButton_60),
                       (self.ui.pushButton_61, self.ui.pushButton_62, self.ui.pushButton_63, self.ui.pushButton_64,
                        self.ui.pushButton_65, self.ui.pushButton_66, self.ui.pushButton_67, self.ui.pushButton_68,
                        self.ui.pushButton_69, self.ui.pushButton_70, self.ui.pushButton_71, self.ui.pushButton_72,
                        self.ui.pushButton_73, self.ui.pushButton_74, self.ui.pushButton_75, self.ui.pushButton_76,
                        self.ui.pushButton_77, self.ui.pushButton_78, self.ui.pushButton_79, self.ui.pushButton_80),
                       (self.ui.pushButton_81, self.ui.pushButton_82, self.ui.pushButton_83, self.ui.pushButton_84,
                        self.ui.pushButton_85, self.ui.pushButton_86, self.ui.pushButton_87, self.ui.pushButton_88,
                        self.ui.pushButton_89, self.ui.pushButton_90, self.ui.pushButton_91, self.ui.pushButton_92,
                        self.ui.pushButton_93, self.ui.pushButton_94, self.ui.pushButton_95, self.ui.pushButton_96,
                        self.ui.pushButton_97, self.ui.pushButton_98, self.ui.pushButton_99, self.ui.pushButton_100)
                       ]
        self.display = [(self.ui.pushButton_1, self.ui.pushButton_21, self.ui.pushButton_41, self.ui.pushButton_61,
                         self.ui.pushButton_81),
                        (self.ui.pushButton_2, self.ui.pushButton_22, self.ui.pushButton_42, self.ui.pushButton_62,
                         self.ui.pushButton_82),
                        (self.ui.pushButton_3, self.ui.pushButton_23, self.ui.pushButton_43, self.ui.pushButton_63,
                         self.ui.pushButton_83),
                        (self.ui.pushButton_4, self.ui.pushButton_24, self.ui.pushButton_44, self.ui.pushButton_64,
                         self.ui.pushButton_84),
                        (self.ui.pushButton_5, self.ui.pushButton_25, self.ui.pushButton_45, self.ui.pushButton_65,
                         self.ui.pushButton_85),
                        (self.ui.pushButton_6, self.ui.pushButton_26, self.ui.pushButton_46, self.ui.pushButton_66,
                         self.ui.pushButton_86),
                        (self.ui.pushButton_7, self.ui.pushButton_27, self.ui.pushButton_47, self.ui.pushButton_67,
                         self.ui.pushButton_87),
                        (self.ui.pushButton_8, self.ui.pushButton_28, self.ui.pushButton_48, self.ui.pushButton_68,
                         self.ui.pushButton_88),
                        (self.ui.pushButton_9, self.ui.pushButton_29, self.ui.pushButton_49, self.ui.pushButton_69,
                         self.ui.pushButton_89),
                        (self.ui.pushButton_10, self.ui.pushButton_30, self.ui.pushButton_50, self.ui.pushButton_70,
                         self.ui.pushButton_90),
                        (self.ui.pushButton_11, self.ui.pushButton_31, self.ui.pushButton_51, self.ui.pushButton_71,
                         self.ui.pushButton_91),
                        (self.ui.pushButton_12, self.ui.pushButton_32, self.ui.pushButton_52, self.ui.pushButton_72,
                         self.ui.pushButton_92),
                        (self.ui.pushButton_13, self.ui.pushButton_33, self.ui.pushButton_53, self.ui.pushButton_73,
                         self.ui.pushButton_93),
                        (self.ui.pushButton_14, self.ui.pushButton_34, self.ui.pushButton_54, self.ui.pushButton_74,
                         self.ui.pushButton_94),
                        (self.ui.pushButton_15, self.ui.pushButton_35, self.ui.pushButton_55, self.ui.pushButton_75,
                         self.ui.pushButton_95),
                        (self.ui.pushButton_16, self.ui.pushButton_36, self.ui.pushButton_56, self.ui.pushButton_76,
                         self.ui.pushButton_96),
                        (self.ui.pushButton_17, self.ui.pushButton_37, self.ui.pushButton_57, self.ui.pushButton_77,
                         self.ui.pushButton_97),
                        (self.ui.pushButton_18, self.ui.pushButton_38, self.ui.pushButton_58, self.ui.pushButton_78,
                         self.ui.pushButton_98),
                        (self.ui.pushButton_19, self.ui.pushButton_39, self.ui.pushButton_59, self.ui.pushButton_79,
                         self.ui.pushButton_99),
                        (self.ui.pushButton_20, self.ui.pushButton_40, self.ui.pushButton_60, self.ui.pushButton_80,
                         self.ui.pushButton_100),
                        ]
        self.btn_warning = [self.ui.pushButton_103, self.ui.pushButton_106, self.ui.pushButton_109,
                            self.ui.pushButton_112, self.ui.pushButton_115]
        self.btn_open = [self.ui.pushButton_101, self.ui.pushButton_104, self.ui.pushButton_107,
                         self.ui.pushButton_110, self.ui.pushButton_113]
        self.btn_close = [self.ui.pushButton_102, self.ui.pushButton_105, self.ui.pushButton_108,
                          self.ui.pushButton_111, self.ui.pushButton_114]
        for btn_row in self.floors:
            for btn in btn_row:
                btn.clicked.connect(self.chooseFloor)
        for btn in self.btn_warning:
            btn.clicked.connect(self.toWarning)
        for btn in self.btn_open:
            btn.clicked.connect(self.openDoor)
        for btn in self.btn_close:
            btn.clicked.connect(self.closeDoor)
        self.forswitch_1.connect(self.Switch)
        self.forswitch_2.connect(self.Switch)
        self.forswitch_3.connect(self.Switch)
        self.forswitch_4.connect(self.Switch)
        self.forswitch_5.connect(self.Switch)

    def Switch(self, i):
        print(i)
        print("Switch Begin")
        for btn in self.display[i - 1]:
            btn.setEnabled(True)

    def chooseFloor(self):
        global index
        sender = self.sender()
        p = parse.parse("pushButton_{}", sender.objectName())
        # sender.setEnabled(False)
        if int(p[0]) % 20 == 0:
            index = int(p[0]) // 20
            if self.E[index - 1].status == static:
                self.E[index - 1].toFloor(20, index)
            else:
                self.E[index - 1].renewQueue(20)
            for btn in self.display[20 - 1]:
                btn.setEnabled(False)
            if self.E[index - 1].nowFloor == 20:
                for btn in self.display[20 - 1]:
                    btn.setEnabled(True)
        else:
            index = int(p[0]) // 20 + 1
            if self.E[index - 1].status == static:
                self.E[index - 1].toFloor(int(p[0]) - (index - 1) * 20, index)
            else:
                self.E[index - 1].renewQueue(int(p[0]) - (index - 1) * 20)
            for btn in self.display[int(p[0]) - (index - 1) * 20 - 1]:
                btn.setEnabled(False)
            if self.E[index - 1].nowFloor == int(p[0]) - (index - 1) * 20:
                for btn in self.display[int(p[0]) - (index - 1) * 20 - 1]:
                    btn.setEnabled(True)
        # 下面两行是没啥用的，可以删去
        if (not self.E[index - 1].started) or self.E[index - 1].status == static:
            self.E[index - 1].start()
        # self.timer.start(500)
        if self.E[index - 1].status == upGoing:
            print("upgoing\n")
        elif self.E[index - 1].status == downGoing:
            print("downgoing\n")

    # 外部用户请求电梯:
    def needAElevator(self):
        dist = 999
        bestElevator = 1
        sender = self.sender()
        p = parse.parse("pushButton_{}", sender.objectName())
        # 针对从同一楼层发出的请求，电梯都可以接收
        # 但是会优先调度距离发起请求的楼层最近的电梯
        # 前提是无故障，即未进入warning状态
        # 那么如果5台都满足以上调度条件，则如何选择电梯？
        # 1. 人数非满
        # 2. 距离最近 √
        # 换句话说，调度的条件有3：
        for i in range(5):
            if not self.E[i].status == warning:
                if self.E[i].nowFloor < int(self.ui.spinBox.cleanText()) and self.E[i].status == upGoing and p[0] == \
                        '0':
                    # 对于当前电梯执行的任务出现优先级调度
                    # 优先度根据电梯与请求楼层的距离来定义，越小则优先级越高
                    if dist > abs(int(self.ui.spinBox.cleanText()) - self.E[i].nowFloor):  # 循环迭代计算最小者
                        dist = abs(int(self.ui.spinBox.cleanText()) - self.E[i].nowFloor)
                        bestElevator = i
                elif self.E[i].nowFloor > int(self.ui.spinBox.cleanText()) and self.E[i].status == downGoing and p[0] \
                        == '116':
                    if dist > abs(int(self.ui.spinBox.cleanText()) - self.E[i].nowFloor):  # 循环迭代计算最小者
                        dist = abs(int(self.ui.spinBox.cleanText()) - self.E[i].nowFloor)
                        bestElevator = i
                elif self.E[i].status == static:
                    if dist > abs(int(self.ui.spinBox.cleanText()) - self.E[i].nowFloor):  # 循环迭代计算最小者
                        dist = abs(int(self.ui.spinBox.cleanText()) - self.E[i].nowFloor)
                        bestElevator = i
            else:
                print("All Elevators shut down.")
        if not self.E[bestElevator].started:
            self.E[bestElevator].start()
        if self.E[bestElevator].status == static:
            self.E[bestElevator].toFloor(int(self.ui.spinBox.cleanText()), bestElevator + 1)
            # 决定最优电梯后，调度该电梯 同时切换电梯状态
        else:
            self.E[bestElevator].renewQueue(int(self.ui.spinBox.cleanText()))

    def toWarning(self):
        sender = self.sender()
        p = parse.parse("pushButton_{}", sender.objectName())
        i = int((int(p[0]) - 103) / 3)
        for btn in self.floors[i]:
            btn.setEnabled(False)
        self.btn_open[i].setEnabled(False)
        self.btn_close[i].setEnabled(False)
        print(i)
        self.E[i].isWarning(i + 1)

    def openDoor(self):
        sender = self.sender()
        p = parse.parse("pushButton_{}", sender.objectName())
        i = int((int(p[0]) - 101) / 3)
        print(i)
        if self.E[i].status == static:
            for btn in self.floors[i]:
                btn.setEnabled(False)
            self.E[i].isOpen(i + 1)

    def closeDoor(self):
        sender = self.sender()
        p = parse.parse("pushButton_{}", sender.objectName())
        i = int((int(p[0]) - 102) / 3)
        print(i)
        for btn in self.floors[i]:
            btn.setEnabled(True)
        self.E[i].isClose(i + 1)
