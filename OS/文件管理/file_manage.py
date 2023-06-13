from datetime import datetime

import sys
import file_manage_backend
from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QTextOption, QCursor
from PyQt6.QtCore import QModelIndex
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QVBoxLayout, QHBoxLayout, \
    QPlainTextEdit, QMainWindow, QMessageBox, QInputDialog, QTreeView, QAbstractItemView, QMenu

from qt_material import apply_stylesheet


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view_of_tree = QTreeView()
        self.label_1 = QLabel("选中文件内容：")
        self.editor = QPlainTextEdit()
        self.save_button = QPushButton("保存")
        self.file_manage = file_manage_backend.fileSystem("file_manage")
        self.now_path = []
        self.selected_file = None
        self.selected_folder = None
        self.p_selected_folder = None

        self.setup_ui()

    def setup_ui(self):

        self.resize(800, 600)
        self.setWindowTitle("文件管理")

        menu = self.menuBar()

        fileMenu = menu.addMenu("文件")
        fileMenu.addAction(QIcon('icon/create_file.png'), "新建文件", self.create_file)
        fileMenu.addAction(QIcon('icon/delete.png'), "删除文件", self.delete_file)
        fileMenu.addAction(QIcon('icon/rename.png'), "重命名文件", self.rename_file)  # 改icon

        folderMenu = menu.addMenu("文件夹")
        folderMenu.addAction(QIcon('icon/create_folder.png'), "新建文件夹", self.create_folder)
        folderMenu.addAction(QIcon('icon/delete.png'), "删除文件夹", self.delete_folder)
        folderMenu.addAction(QIcon('icon/rename.png'), "重命名文件夹", self.rename_folder)  # 改icon

        formatMenu = menu.addMenu("格式化")
        formatMenu.addAction(QIcon('icon/format.png'), "格式化", self.format)

        widget_1 = QWidget()
        vertical_1 = QVBoxLayout()
        widget_1.setLayout(vertical_1)
        self.setCentralWidget(widget_1)

        self.update_view_tree()
        self.view_of_tree.expandAll()

        horizon_1 = QHBoxLayout()
        horizon_1.addWidget(self.view_of_tree)
        vertical_1.addLayout(horizon_1)

        self.label_1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # ?

        self.editor.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)  # ?

        self.save_button.clicked.connect(self.save_file)

        vertical_2 = QVBoxLayout()
        vertical_2.addWidget(self.label_1)
        vertical_2.addWidget(self.editor)
        vertical_2.addWidget(self.save_button)
        horizon_1.addLayout(vertical_2)

        self.view_of_tree.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.view_of_tree.customContextMenuRequested.connect(self.call_menu_right_click)

    def append_item(self, root: QStandardItem, src: file_manage_backend.folder):
        for each in src.folder_children:
            child_model = QStandardItem(each.folder_name)
            root.appendRow(child_model)
            # BFS
            self.append_item(child_model, each)
        for each in src.FCB_children:
            child_model = QStandardItem(each.name)
            root.appendRow(child_model)

    def build_model_for_tree(self) -> QStandardItemModel:
        model = QStandardItemModel()
        header = QStandardItem()
        header.setText('这里你可以看到文件的树形结构：')
        model.setHorizontalHeaderItem(0, header)
        root = QStandardItem(self.file_manage.file_content.root.folder_name)
        model.appendRow(root)
        self.append_item(root, self.file_manage.file_content.root)
        return model

    def update_text_edit(self):
        if self.selected_file is not None:
            data = self.file_manage.open_read(self.selected_file)
            self.editor.setEnabled(True)
            self.editor.setPlainText(data)
        else:
            self.editor.setPlainText("您选中的是文件夹哦")
            self.editor.setEnabled(False)

    def update_view_tree(self):
        self.view_of_tree.setModel(self.build_model_for_tree())
        self.view_of_tree.expandAll()  # ?
        self.view_of_tree.selectionModel().currentChanged.connect(self.find_selected_one_click)

        self.view_of_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.view_of_tree.header().setStretchLastSection(True)
        self.view_of_tree.horizontalScrollBar().setEnabled(True)
        self.view_of_tree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.view_of_tree.verticalScrollBar().setEnabled(True)
        self.view_of_tree.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        pass

    def update_all(self):
        self.update_text_edit()
        self.update_view_tree()

    def find_selected_one_click(self, cur_node: QModelIndex):
        idx_in_folder = cur_node.row()
        self.now_path = []

        while cur_node.data() is not None:
            self.now_path.insert(0, cur_node.data())
            cur_node = cur_node.parent()

        cursor = self.file_manage.file_content.root
        for each in range(len(self.now_path) - 1):
            for every in cursor.folder_children:
                if every.folder_name == self.now_path[each]:
                    cursor = every
                    break
        if len(self.now_path) != 1:
            if (len(cursor.folder_children) - 1) < idx_in_folder \
                    and cursor.size() != 0:
                self.selected_file = cursor.FCB_children[idx_in_folder - len(cursor.folder_children)]
                self.selected_folder = cursor
                self.label_1.setText(self.selected_file.name + " 修改时间：" + str(
                    self.selected_file.update_time.strftime("%Y-%m-%d %H:%M:%S")))
            else:
                self.selected_file = None
                if len(cursor.folder_children) != 0:
                    self.selected_folder = cursor.folder_children[idx_in_folder]
                    self.p_selected_folder = cursor
                self.label_1.setText(self.selected_folder.folder_name + " 修改时间：" + str(
                    self.selected_folder.update_time.strftime("%Y-%m-%d %H:%M:%S")))
        else:
            self.selected_file = None
            self.selected_folder = self.file_manage.file_content.root
            self.p_selected_folder = None
            self.label_1.setText(self.selected_folder.folder_name + " 修改时间：" + str(
                self.selected_folder.update_time.strftime("%Y-%m-%d %H:%M:%S")))

        self.update_text_edit()

        if self.selected_file is not None:
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def call_menu_right_click(self):
        if self.selected_file == self.selected_folder:
            return

        submenu = QMenu()
        if self.selected_file is not None:
            submenu.addAction(QIcon('icon/delete.png'), "删除文件", self.delete_file)
            submenu.addAction(QIcon('icon/rename.png'), "重命名文件", self.rename_file)
        elif self.selected_folder is not None:
            submenu.addAction(QIcon('icon/create_file.png'), "创建文件", self.create_file)
            submenu.addAction(QIcon('icon/create_folder.png'), "创建文件夹", self.create_folder)
            submenu.addAction(QIcon('icon/delete.png'), "删除文件夹", self.delete_folder)
            submenu.addAction(QIcon('icon/rename.png'), "重命名文件夹", self.rename_folder)

        submenu.exec(QCursor.pos())
        submenu.show()

    def create_file(self):
        new_name, ok = QInputDialog.getText(self, '新建文件', "请输入文件名称：")
        if ok:
            if new_name == "":
                QMessageBox.warning(self, '错误！', "文件名不能为空！")
            elif self.selected_folder is None:
                QMessageBox.warning(self, '错误！', "请先选中要新建文件的文件夹！")
            else:
                self.file_manage.create_file(new_name, self.selected_folder, datetime.now())
                self.update_all()

    def create_folder(self):
        new_name, ok = QInputDialog.getText(self, '新建文件夹', "请输入文件夹名称：")
        if ok:
            if new_name == "":
                QMessageBox.warning(self, '错误！', "文件夹名不能为空！")
            elif self.selected_folder is None:
                QMessageBox.warning(self, '错误！', "请先选中要新建文件夹的文件夹！")
            elif new_name == (each.folder_name for each in self.selected_folder.folder_children):
                QMessageBox.warning(self, '错误！', "已存在同名文件夹！")
            else:
                self.file_manage.create_folder(self.selected_folder, new_name, datetime.now())
                self.update_all()

    def delete_file(self):
        ans = QMessageBox.question(self, '删除文件', "您确定要删除吗？")
        if ans == QMessageBox.StandardButton.Yes:
            if self.selected_file is None:
                QMessageBox.warning(self, '错误！', "您未选中任何文件！")
            else:
                self.file_manage.file_delete(self.selected_file, self.selected_folder)
                self.selected_file = None
                self.update_all()

    def delete_folder(self):
        ans = QMessageBox.question(self, '删除文件夹', "您确定要删除吗？")
        if ans == QMessageBox.StandardButton.Yes:
            if self.selected_folder is None:
                QMessageBox.warning(self, '错误！', "您未选中任何文件夹！")
            elif self.selected_folder.folder_name == "/":
                QMessageBox.warning(self, '错误！', "根文件夹不可删除！")
            else:
                self.file_manage.delete_folder(self.selected_folder)
                self.p_selected_folder.folder_children.remove(self.selected_folder)
                self.update_all()

    def rename_folder(self):
        new_name, ok = QInputDialog.getText(self, '重命名文件夹', "请输入文件夹名称：")
        if ok:
            if new_name == "":
                QMessageBox.warning(self, '错误！', "文件夹名不能为空！")
            elif self.selected_folder is None:
                QMessageBox.warning(self, '错误！', "请先选中要重命名的文件夹！")
            else:
                self.file_manage.rename_folder(new_name, self.selected_folder, datetime.now())
                self.update_all()

    def rename_file(self):
        new_name, ok = QInputDialog.getText(self, '重命名文件', "请输入文件名称：")
        if ok:
            if new_name == "":
                QMessageBox.warning(self, '错误！', "文件名不能为空！")
            elif self.selected_folder is None:
                QMessageBox.warning(self, '错误！', "请先选中要重命名的文件！")
            elif new_name == (each.folder_name for each in self.selected_folder.FCB_children):
                QMessageBox.warning(self, '错误！', "已存在同名文件！")
            else:
                self.file_manage.rename_file(new_name, self.selected_file, self.selected_folder, datetime.now())
                self.update_all()

    def save_file(self):
        self.file_manage.write_close(self.selected_file, self.editor.toPlainText())

    def save(self):
        self.file_manage.save_to_local()
        pass

    def format(self):
        ans = QMessageBox.question(self, '格式化', "此操作会丢失所有数据，您确定要格式化吗？")
        if ans == QMessageBox.StandardButton.Yes:
            self.file_manage.Format()
            self.selected_folder = self.file_manage.file_content.root
            self.selected_file = None
            self.now_path = [self.selected_folder.folder_name]
            self.update_all()

    def closeEvent(self, event):
        self.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    M = Main_window()

    apply_stylesheet(app, theme='dark_blue.xml')

    M.show()
    sys.exit(app.exec())
