import queue


class Controller(object):
    def __init__(self):
        self.upDestination = queue.PriorityQueue(20)  # 上行队列
        self.downDestination = queue.PriorityQueue(20)  # 下行队列
