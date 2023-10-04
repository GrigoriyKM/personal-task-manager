import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, \
    QHBoxLayout, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, \
    QComboBox, QLabel, QLineEdit, QMessageBox, QHeaderView
from PyQt6 import QtCore, QtGui
from create_task import TaskCreation
from datetime import datetime
import time
from utils import TaskInfo


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        left, top, height, width = 400, 100, 600, 900
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("Personal Task Manager")
        self.task_creation_window = TaskCreation()
        # left side of the window
        layout_h1 = QHBoxLayout(self)
        layout_h1_v = QVBoxLayout(self)
        layout_h1_v_h = QHBoxLayout(self)
        # right side of the window
        layout_h2_v = QVBoxLayout(self)
        layout_h2_v_h1 = QHBoxLayout(self)
        layout_h2_v_h2 = QHBoxLayout(self)
        # widgets on the left
        self.task_widget = QTableWidget()
        self.task_widget.setRowCount(0)
        self.task_widget.setColumnCount(4)
        self.task_widget.setHorizontalHeaderLabels(['id', 'name', 'due date', 'priority'])
        self.task_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        # self.task_widget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.task_widget.horizontalHeader().setStretchLastSection(True)
        layout_h1_v.addWidget(self.task_widget)

        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.add_task_button = QPushButton("add")
        self.del_task_button = QPushButton("del")
        self.del_task_button.setDisabled(True)
        layout_h1_v_h.addSpacerItem(spacer)
        layout_h1_v_h.addWidget(self.add_task_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_h1_v_h.addWidget(self.del_task_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_h1_v.addLayout(layout_h1_v_h)
        layout_h1.addLayout(layout_h1_v)
        # widgets on the right
        self.label1 = QLabel('Estimated time: ')
        self.days = QLineEdit()
        self.regex = r"^[1-9]\d*$"
        validator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(self.regex)
        )
        self.days.setValidator(validator)
        self.days.setText("0")
        self.days.setDisabled(True)
        self.label2 = QLabel('d')
        self.hours = QLineEdit()
        self.hours.setValidator(validator)
        self.hours.setDisabled(True)
        self.hours.setText("0")
        self.label3 = QLabel('h')
        self.priority = QComboBox()
        self.priority.setCurrentIndex(0)
        self.priority.addItems(('high', 'medium', "low"))
        self.priority.setDisabled(True)
        layout_h2_v_h1.addWidget(self.priority, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_v_h1.addSpacerItem(spacer)
        layout_h2_v_h1.addWidget(self.label1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_v_h1.addWidget(self.days, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_v_h1.addWidget(self.label2, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_v_h1.addWidget(self.hours, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_v_h1.addWidget(self.label3, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        layout_h2_v.addLayout(layout_h2_v_h1)

        self.description_box = QTextEdit()
        self.description_box.setDisabled(True)
        layout_h2_v.addWidget(self.description_box)

        self.edit_task_button = QPushButton("edit")
        self.edit_task_button.setDisabled(True)
        layout_h2_v_h2.addSpacerItem(spacer)
        layout_h2_v_h2.addWidget(self.edit_task_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_h2_v.addLayout(layout_h2_v_h2)
        layout_h1.addLayout(layout_h2_v)

        widget = QWidget()
        widget.setLayout(layout_h1)
        self.setCentralWidget(widget)
        # load task data if exist
        try:
            with open("my_tasks.json") as file:
                self.task_info = json.load(file)
                print(self.task_info)
            with open("check_state_info.json") as file:
                self.check_state_info = json.load(file)
                self.load_data()
            with open("task_id.txt") as file:
                self.task_id = int(file.readline())
        except FileNotFoundError:
            self.task_info = {}
            self.task_id = 0
        # Task creation
        self.add_task_button.clicked.connect(self.show_task_creation_window)
        self.task_creation_window.task_name.textChanged.connect(self.task_creation_window.enable_create_task_button)
        self.task_creation_window.create_task_button.clicked.connect(self.add_task)
        self.task_creation_window.cancel_create_task_button.clicked.connect(
            self.task_creation_window.close_task_creation_window)
        # connecting rows on the left with description on the right
        self.task_widget.itemSelectionChanged.connect(self.show_task_info)
        self.description_box.textChanged.connect(lambda: self.edit_task_button.setEnabled(True))
        self.hours.textChanged.connect(lambda: self.edit_task_button.setEnabled(True))
        self.days.textChanged.connect(lambda: self.edit_task_button.setEnabled(True))
        self.priority.currentTextChanged.connect(lambda: self.edit_task_button.setEnabled(True))
        self.edit_task_button.clicked.connect(self.edit_task)
        # deleting rows in the task table
        self.task_widget.itemSelectionChanged.connect(self.enable_buttons)
        self.del_task_button.clicked.connect(self.delete_task)
        self.task_widget.clicked.connect(self.save_tasks)

    def add_task(self):
        if len(self.task_creation_window.day.text()) == 0 or len(self.task_creation_window.hour.text()) == 0:
            msg_box = QMessageBox()
            msg_box.setText('Please set a valid estimated time input. It cannot be empty. Fix the time and try again 😅')
            msg_box.setWindowTitle('YouTube Downloader')
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.exec()
        else:
            row_index = self.task_widget.rowCount()
            self.task_widget.insertRow(row_index)
            task_id = str(self.task_id)
            task_name = self.task_creation_window.task_name.text()
            task_description = self.task_creation_window.description_box.toPlainText()
            days, hours = self.task_creation_window.day.text(), self.task_creation_window.hour.text()
            due_date = datetime.fromtimestamp(time.time() + (24 * int(days) + int(hours))*3600)
            date_time = due_date.strftime("%m/%d/%Y, %H:%M")
            priority = self.task_creation_window.priority.currentText()
            self.task_info[task_id] = [task_name, date_time, priority, task_description, days, hours]
            item = QTableWidgetItem(task_id)
            item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.task_widget.setItem(row_index, 0, item)
            for i in range(1, 4):
                item = QTableWidgetItem(self.task_info[task_id][i-1])
                self.task_widget.setItem(row_index, i, item)
                if i > 1:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.task_id = self.task_id + 1  # to do unique id
            self.task_creation_window.description_box.clear()
            self.task_creation_window.day.setText('0')
            self.task_creation_window.hour.setText('0')
            self.task_creation_window.close_task_creation_window()
            self.save_tasks()

    def show_task_info(self):
        row = self.task_widget.currentRow()
        if row == -1:  # in case we delete last row
            self.task_id = 0
            self.description_box.clear()
            self.days.setText('0')
            self.hours.setText('0')
            self.priority.setCurrentIndex(0)
            self.description_box.setDisabled(True)
            self.days.setDisabled(True)
            self.hours.setDisabled(True)
            self.priority.setDisabled(True)
        else:
            task_id = self.task_widget.item(row, 0).text()
            description = self.task_info[task_id][TaskInfo.DESCRIPTION.value]
            days, hours = self.task_info[task_id][TaskInfo.DAYS.value], self.task_info[task_id][TaskInfo.HOURS.value]
            priority = self.task_widget.item(row, 3).text()
            self.description_box.setText(description)
            self.days.setText(days)
            self.hours.setText(hours)
            self.priority.setCurrentText(priority)
            self.description_box.setEnabled(True)
            self.days.setEnabled(True)
            self.hours.setEnabled(True)
            self.priority.setEnabled(True)

    def edit_task(self):
        row = self.task_widget.currentRow()
        task_id = self.task_widget.item(row, 0).text()
        description = self.description_box.toPlainText()
        self.task_info[task_id][TaskInfo.DESCRIPTION.value] = description
        if len(self.days.text()) == 0 or len(self.hours.text()) == 0:
            self.days.setText(self.task_info[task_id][TaskInfo.DAYS.value])
            self.hours.setText(self.task_info[task_id][TaskInfo.HOURS.value])
        if self.task_info[task_id][TaskInfo.NAME.value] != self.task_widget.item(row, 1).text():
            self.task_info[task_id][TaskInfo.NAME.value] = self.task_widget.item(row, 1).text()
        if self.task_info[task_id][TaskInfo.HOURS.value] != self.hours.text()\
                or self.task_info[task_id][TaskInfo.DAYS.value] != self.days.text():
            days, hours = self.days.text(), self.hours.text()
            due_date = datetime.fromtimestamp(time.time() + (24 * int(days) + int(hours)) * 3600)
            date_time = due_date.strftime("%m/%d/%Y, %H:%M")
            self.task_widget.item(row, 2).setText(date_time)
            self.task_info[task_id][TaskInfo.DATE.value] = date_time
            self.task_info[task_id][TaskInfo.DAYS.value] = days
            self.task_info[task_id][TaskInfo.HOURS.value] = hours
        if self.task_info[task_id][TaskInfo.PRIORITY.value] != self.priority.currentText():
            priority = self.priority.currentText()
            self.task_widget.item(row, 3).setText(priority)
            self.task_info[task_id][TaskInfo.PRIORITY.value] = priority
        self.edit_task_button.setDisabled(True)
        self.save_tasks()

    def show_task_creation_window(self):
        self.task_creation_window.show()

    def enable_buttons(self):
        if self.task_widget.rowCount() > 0:
            self.del_task_button.setEnabled(True)
        else:
            self.days.setDisabled(True)
            self.hours.setDisabled(True)
            self.description_box.setDisabled(True)
            self.priority.setDisabled(True)

    def delete_task(self):
        current_row = self.task_widget.row(self.task_widget.currentItem())
        task_id = self.task_widget.item(current_row, 0).text()
        self.task_widget.removeRow(current_row)
        self.del_task_button.setDisabled(True)
        self.edit_task_button.setDisabled(True)
        del self.task_info[task_id]
        self.save_tasks()

    def load_data(self):
        for row_index, task_id in enumerate(self.task_info.keys()):
            item = QTableWidgetItem(task_id)
            item.setCheckState(QtCore.Qt.CheckState.Checked if self.check_state_info[task_id]
                               else QtCore.Qt.CheckState.Unchecked)
            self.task_widget.insertRow(row_index)
            self.task_widget.setItem(row_index, 0, item)
            for i in range(1, 4):
                item = QTableWidgetItem(self.task_info[task_id][i - 1])
                self.task_widget.setItem(row_index, i, item)
                if i > 1:
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

    def save_tasks(self):
        tasks_to_save = {}
        check_state_info = {}
        for i in range(self.task_widget.rowCount()):
            is_checked = self.task_widget.item(i, 0).checkState() == QtCore.Qt.CheckState.Checked
            task_id = self.task_widget.item(i, 0).text()
            tasks_to_save[task_id] = self.task_info[task_id]
            check_state_info[task_id] = 1 if is_checked else 0
        with open("my_tasks.json", "w") as file:
            json.dump(tasks_to_save, file)
        with open("check_state_info.json", "w") as file:
            json.dump(check_state_info, file)
        with open("task_id.txt", "w") as file:
            file.write(str(self.task_id))


def main():
    app = QApplication(sys.argv)
    with open("Combinear.qss", 'r') as style_sheet_file:
        app.setStyleSheet(style_sheet_file.read())
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
