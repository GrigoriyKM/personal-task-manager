from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QTextEdit, \
    QPushButton, QLineEdit, QComboBox, QLabel


class TaskCreation(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        left, top, height, width = 700, 250, 300, 250
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("add task")
        layout_v_tc = QVBoxLayout(self)
        layout_h1_tc = QHBoxLayout(self)
        layout_h2_tc = QHBoxLayout(self)
        layout_h3_tc = QHBoxLayout(self)

        self.task_name = QLineEdit()
        self.task_name.setPlaceholderText('Enter task name')
        spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.priority = QComboBox()
        self.priority.setCurrentIndex(0)
        self.priority.addItems(('high', 'medium', "low"))

        layout_h1_tc.addWidget(self.task_name, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_h1_tc.addSpacerItem(spacer)
        layout_h1_tc.addWidget(self.priority, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_v_tc.addLayout(layout_h1_tc)
        self.label1 = QLabel('Estimated time: ')
        self.day = QLineEdit()
        self.regex = r"^[1-9]\d*$"
        validator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(self.regex)
        )
        self.day.setValidator(validator)
        self.day.setText("0")
        self.label2 = QLabel('d')
        self.hour = QLineEdit()
        self.hour.setValidator(validator)
        self.hour.setText("0")
        self.label3 = QLabel('h')
        layout_h2_tc.addWidget(self.label1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_tc.addWidget(self.day, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_tc.addWidget(self.label2, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_tc.addWidget(self.hour, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_h2_tc.addWidget(self.label3, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_v_tc.addLayout(layout_h2_tc)
        self.description_box = QTextEdit()
        layout_v_tc.addWidget(self.description_box, 0, QtCore.Qt.AlignmentFlag.AlignCenter)

        layout_h3_tc.addSpacerItem(spacer)
        self.create_task_button = QPushButton("create")
        self.create_task_button.setDisabled(True)
        self.cancel_create_task_button = QPushButton("cancel")
        layout_h3_tc.addWidget(self.create_task_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_h3_tc.addWidget(self.cancel_create_task_button, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_v_tc.addLayout(layout_h3_tc)

    def enable_create_task_button(self):
        name = self.task_name.text()
        if name != '':
            self.create_task_button.setEnabled(True)
            self.task_name.setText(name)
        else:
            self.create_task_button.setDisabled(True)

    def close_task_creation_window(self):
        self.task_name.clear()
        self.close()
