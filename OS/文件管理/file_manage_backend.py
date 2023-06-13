import bitarray
import os
from datetime import datetime
import pickle

BLOCK_NUM = 2 ** 10
BLOCK_SIZE = 4  # 4KB

FREE = 0
OCCUPIED = 1

FAT_AVAILABLE = -2
FAT_FILEEND = -1


class FCB:
    def __init__(self, name, access_time, update_time, length, address=None):
        self.name = name
        self.address = address  # 记录在FAT的起始位置
        self.access_time = access_time
        self.update_time = update_time
        self.length = length

    pass


class Disk:
    def __init__(self):
        self.disk = []  # 硬盘置空
        for i in range(BLOCK_NUM):
            self.disk.append("")  # 防止超范围


class freeSpace:
    def __init__(self):
        self.map = bitarray.bitarray(BLOCK_NUM)
        self.map.setall(FREE)
    pass


class FAT:
    def __init__(self):
        self.FAT_Size = BLOCK_SIZE
        self.table = []
        for i in range(BLOCK_NUM):
            self.table.append(FAT_AVAILABLE)

    pass


class folder:  # 只向下
    def __init__(self, name: str, create_time):
        self.folder_name = name
        self.folder_children = []  # 记录文件夹内文件夹
        self.FCB_children = []  # 记录文件夹内文件
        self.create_time = self.update_time = create_time


class file_content:
    def __init__(self):
        self.root = folder("/", datetime.now())

    pass


class fileSystem:
    def __init__(self, imitated_disk=None):
        self.path = imitated_disk
        if imitated_disk and os.path.exists(imitated_disk):
            f = open(imitated_disk, "rb")
            self.FAT = pickle.load(f)
            self.Disk = pickle.load(f)
            self.file_content = pickle.load(f)
            self.freeSpace = pickle.load(f)
            f.close()
        else:
            self.FAT = FAT()
            self.Disk = Disk()
            self.file_content = file_content()
            self.freeSpace = freeSpace()
            self.create_folder(self.file_content.root, "文件夹1", datetime.now())
            self.create_file("文件1", self.file_content.root, datetime.now())

    def find_free(self):
        return self.freeSpace.map.find(FREE)

    def create_file(self, new_name, parent_folder: folder, create_time):
        # 查找是否出现重名，若是则修改新名字
        for every in parent_folder.FCB_children:
            if new_name == every.name:
                new_name += "(1)"
        parent_folder.FCB_children.append(FCB(new_name, create_time, create_time, 0))
        pass

    def open_file(self, fcb):
        if fcb.address is None:
            return FAT_FILEEND
        else:
            cursor = fcb.address
            return cursor

    def write_close(self, fcb, new_data):
        cursor = fcb.address
        fcb.length = len(new_data)

        while len(new_data) != 0:
            n_cursor = self.find_free()
            if n_cursor == -1:  # 不存在空闲空间
                raise AssertionError("空间不足！")
            if cursor is None:  # 建立新的文件索引
                fcb.address = n_cursor
                self.freeSpace.map[n_cursor] = OCCUPIED
                self.FAT.table[n_cursor] = FAT_FILEEND
                self.Disk.disk[n_cursor] = new_data[:BLOCK_SIZE]
            elif cursor != FAT_FILEEND:  # 覆盖原本的块
                n_cursor = self.FAT.table[cursor]
                self.Disk.disk[cursor] = new_data[:BLOCK_SIZE]
            elif cursor == FAT_FILEEND:  # 填充到新的块
                self.FAT.table[n_cursor] = cursor
                self.freeSpace.map[n_cursor] = OCCUPIED
                self.FAT.table[n_cursor] = FAT_FILEEND
                self.Disk.disk[n_cursor] = new_data[:BLOCK_SIZE]
            new_data = new_data[BLOCK_SIZE:]
            if cursor == FAT_FILEEND:
                cursor = FAT_FILEEND
            else:
                cursor = n_cursor

            fcb.update_time = datetime.now()

    def open_read(self, fcb):
        cursor = self.open_file(fcb)
        if cursor is not None:
            file_data = self.Disk.disk[cursor]
        else:
            file_data = ""
        while cursor != FAT_FILEEND:
            file_data += self.Disk.disk[self.FAT.table[cursor]]
            cursor = self.FAT.table[cursor]
        return file_data

    def file_delete(self, fcb, p_folder: folder = None):
        cursor = fcb.address

        if cursor is not None:  # 证明文件存在
            while cursor != FAT_FILEEND:
                self.freeSpace.map[cursor] = FREE
                self.Disk.disk[cursor] = ""

                n_cursor = self.FAT.table[cursor]
                self.FAT.table[cursor] = FAT_AVAILABLE

                cursor = n_cursor

        if p_folder is not None:
            p_folder.FCB_children.remove(fcb)

    def Format(self):
        self.FAT = FAT()
        self.Disk = Disk()
        self.file_content = file_content()
        self.freeSpace = freeSpace()

    def create_folder(self, p_folder: folder, name, create_time):
        for i in p_folder.folder_children:
            if i.folder_name == name:
                name += "(1)"

        p_folder.folder_children.append(folder(name, create_time))
        p_folder.update_time = create_time
        pass

    def delete_folder(self, deleted_folder: folder):
        for each in deleted_folder.folder_children:
            self.delete_folder(each)
            deleted_folder.folder_children.remove(each)
        for each in deleted_folder.FCB_children:
            self.file_delete(each)
            deleted_folder.FCB_children.remove(each)
        pass

    def save_to_local(self):
        f = open(self.path, "wb")
        pickle.dump(self.FAT, f)
        pickle.dump(self.Disk, f)
        pickle.dump(self.file_content, f)
        pickle.dump(self.freeSpace, f)

    def rename_folder(self, name: str, c_folder: folder, update_time):
        c_folder.folder_name = name
        c_folder.update_time = update_time
        return 1

    def rename_file(self, name: str, c_file: FCB, c_folder: folder, update_time):
        c_file.name = name
        c_file.update_time = update_time
        c_folder.update_time = update_time
        return 1
