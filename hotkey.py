from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout, QMainWindow, QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from pynput.keyboard import Key, Listener
import re

StyleSheet = '''
QPushButton#BlueButton {
    background-color: #E1E1E1;
    border:1px solid #ADADAD;
}

QPushButton:hover {
    background-color: #E4EFF9;
    border:1px solid #0C7BD4;
    color: #000;
}


'''

StyleSheetSelected = '''

QPushButton {
    background-color: yellow;
    border:1px solid 	#666600;

}

QPushButton:hover {
    background-color: yellow;
    border:2px solid black;
    color: #000;
}



'''


class HotKey(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setFixedWidth(400)
        self.setWindowIcon(QtGui.QIcon("gta_icon.png"))
        self.setWindowTitle("GTA V SOLO KIT - HotKeys")
        # to check if a user is still setting a hotkey
        self.setting_key = False

    def setup_ui(self):
        main_layout = QGridLayout()

        firewall_on_hot_key = QLabel("Firewall On")
        firewall_on_hot_key.setStyleSheet("border:0.5px solid black;")

        firewall_off_hot_key = QLabel("Firewall Off")
        firewall_off_hot_key.setStyleSheet("border:1px solid black;")

        resource_monitor_key = QLabel("Resource Monitor")
        resource_monitor_key.setStyleSheet("border:1px solid black;")

        self.resource_monitor_button = QPushButton(self)
        self.resource_monitor_button.setText("F10")
        self.resource_monitor_button.clicked.connect(self.hot_key_resource_monitor)
        self.resource_monitor_button.setFixedSize(100, 23)


        self.firewall_on_button = QPushButton(self)
        self.firewall_on_button.setText("F11")
        self.firewall_on_button.clicked.connect(self.hot_key_firewall_on)
        self.firewall_on_button.setFixedSize(100, 23)

        self.firewall_off_button = QPushButton(self)
        self.firewall_off_button.clicked.connect(self.hot_key_firewall_off)
        self.firewall_off_button.setText("F12")
        self.firewall_off_button.setFixedSize(100, 23)

        option_label = QLabel("Options")
        hot_key_label = QLabel("HotKeys")
        # row and column
        main_layout.addWidget(option_label, 0, 0)
        main_layout.addWidget(hot_key_label, 0, 1)
        main_layout.addWidget(self.firewall_on_button, 1, 1)
        main_layout.addWidget(firewall_on_hot_key, 1, 0)

        main_layout.addWidget(firewall_off_hot_key, 2, 0)
        main_layout.addWidget(self.firewall_off_button, 2, 1)

        main_layout.addWidget(self.resource_monitor_button, 3, 1)
        main_layout.addWidget(resource_monitor_key, 3, 0)

        main_layout.setHorizontalSpacing(10)

        main_layout.setColumnStretch(0, 2)

        widget = QWidget()
        widget.setLayout(main_layout)
        # to be used when listening for keys to be assigned to
        self.worker_thread = WorkerThread(self)
        self.worker_thread.finished.connect(self.changeTextButton)

        self.setCentralWidget(widget)

    def hot_key_resource_monitor(self):

        self.resource_monitor_button.setText("Select a hotkey...")
        self.resource_monitor_button.setStyleSheet(StyleSheetSelected)

        if not self.worker_thread.listening_for_key:

            self.worker_thread.button = self.resource_monitor_button
            self.worker_thread.start()

        else:
            self.worker_thread.button.setStyleSheet(StyleSheet)
            self.worker_thread.button.setText("None")
            self.worker_thread.key_listner.stop()
            # terminate the previous thread and start a new one
            self.worker_thread.button = self.resource_monitor_button
            self.worker_thread.start()

    def hot_key_firewall_on(self):

        self.firewall_on_button.setText("Select a hotkey...")
        self.firewall_on_button.setStyleSheet(StyleSheetSelected)

        if not self.worker_thread.listening_for_key:

            self.worker_thread.button = self.firewall_on_button
            self.worker_thread.start()

        else:
            self.worker_thread.button.setStyleSheet(StyleSheet)
            self.worker_thread.button.setText("None")
            self.worker_thread.key_listner.stop()
            # terminate the previous thread and start a new one
            self.worker_thread.button = self.firewall_on_button
            self.worker_thread.start()

    def hot_key_firewall_off(self):

        self.firewall_off_button.setText("Select a hotkey...")
        self.firewall_off_button.setStyleSheet(StyleSheetSelected)

        if not self.worker_thread.listening_for_key:

            self.worker_thread.button = self.firewall_off_button
            self.worker_thread.start()

        else:
            self.worker_thread.button.setStyleSheet(StyleSheet)
            self.worker_thread.button.setText("None")
            self.worker_thread.key_listner.stop()
            # terminate the previous thread and start a new one
            self.worker_thread.button = self.firewall_off_button
            self.worker_thread.start()

    def changeTextButton(self, key):
        if key == "Key.esc":
            self.worker_thread.button.setText("None")
            self.worker_thread.button.setStyleSheet(StyleSheet)
        else:
            format_key = key.replace("Key.", "").title()

            self.worker_thread.button.setText(format_key)
            self.worker_thread.button.setStyleSheet(StyleSheet)


class WorkerThread(QThread):
    finished = pyqtSignal('QString')

    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.listening_for_key = False
        self.button = None

    def on_press(self, key):
        if key == Key.esc:
            self.finished.emit(str(key))
        else:
            self.finished.emit(str(key))


        self.key_listner.stop()
        self.listening_for_key = False

    def on_release(self, key):
        self.finished.emit(str(key))

    def run(self):
        self.listening_for_key = True
        # Collect events until released
        self.key_listner = Listener(on_press=self.on_press, on_release=self.on_release)
        self.key_listner.start()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    hot_key_window = HotKey()
    hot_key_window.show()
    sys.exit(app.exec_())
