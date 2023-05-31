import os
import random
import numpy as np

Task_number = 320

Pages_capacity = 10

Page_count = int(Task_number / Pages_capacity)

disk_memory = [i for i in range(Task_number)]


def build_task_list():
    task_list = [random.randint(0, 319)]
    i = 0
    while len(task_list) < 320:
        if task_list[i] < 319:
            task_list.append(task_list[i] + 1)
        else:
            task_list.append(0)
        if task_list[i] < (int(Task_number * 0.25)):
            task_list.append(random.randint(int(Task_number * 0.75), 319))
        elif task_list[i] > (int(Task_number * 0.75)):
            task_list.append(random.randint(0, int(Task_number * 0.25)))
        else:
            task_list.append(random.randint(0, 319))
        i += 2
    return task_list


Task_list = build_task_list()


class Page:
    def __init__(self):
        self.page_content = []
        self.page_size = 10

    def allocate(self, memory, itr):
        self.page_content = memory[itr:(itr + 10)]

    def searchPage(self, task):
        if task in self.page_content:
            for i in range(self.page_size):
                if task == self.page_content[i]:
                    return i
        else:
            return -1


disk_pages = [Page() for i in range(32)]
for i in range(32):
    disk_pages[i].allocate(disk_memory, i * 10)


class page_Table:
    def __init__(self, capacity):
        self.capacity = capacity
        self.latelyused = []  # 最近使用过则置0
        self.page = []
        self.page_loss = 0

    def load_FIFO(self, task):
        page = disk_pages[task // 10]
        if page in self.page:
            pass
        else:
            if len(self.page) < 4:
                self.page.append(page)
            else:
                self.page.pop(0)
                self.page.append(page)
            self.page_loss += 1

    def load_LRU(self, task):
        page = disk_pages[task // 10]
        if len(self.latelyused) != 0:
            for i in range(len(self.latelyused)):
                self.latelyused[i] += 1
        if page in self.page:
            for i in range(len(self.page)):
                if page == self.page[i]:
                    self.latelyused[i] = 0
            pass
        else:
            if len(self.latelyused) == 0:
                self.page.append(page)
                self.latelyused.append(0)
            else:
                idx = np.argmax(np.array(self.latelyused))
                if len(self.latelyused) >= 4:
                    if self.latelyused[idx] != 0:
                        self.page.pop(idx)
                        self.latelyused.pop(idx)
                        self.page.append(page)
                        self.latelyused.append(0)
                else:
                    self.page.append(page)
                    self.latelyused.append(0)
            self.page_loss += 1


table = page_Table(4)  # 4页目录
end = 0

while end != '1':
    mode = input("请选择请求内存的置换算法：0为FIFO，1为LRU\n")

    while mode > '1' or mode < '0':
        print("您的输入有误，请重新输入")
        mode = input()

    mode = int(mode)

    if mode:
        for i in Task_list:
            table.load_LRU(i)
    else:
        for i in Task_list:
            table.load_FIFO(i)

    print("调页次数：%d" % table.page_loss)
    print("缺页率：\n %.1f %%" % ((table.page_loss / (Task_number + 1)) * 100))

    end = input("是否结束模拟？是:1，否:0\n")
    while end > '1' or end < '0':
        print("您的输入有误，请重新输入")
        end = input()
    table.page_loss = 0
    os.system('cls')

os.system('pause')
