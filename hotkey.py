from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5 import QtWidgets , QtGui
from PyQt5.QtCore import QThread





class HotKey(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setFixedWidth(400)
        self.setWindowIcon(QtGui.QIcon("gta_icon.png"))
        self.setWindowTitle("GTA V SOLO KIT - HotKeys")


    def setup_ui(self):


        main_layout = QGridLayout()




        firewall_on_hot_key = QLabel("Firewall On")
        firewall_on_hot_key.setStyleSheet("border:0.5px solid black;")


        firewall_off_hot_key = QLabel("Firewall Off")
        firewall_off_hot_key.setStyleSheet("border:1px solid black;")

        resource_monitor_key = QLabel("Resource Monitor")
        resource_monitor_key.setStyleSheet("border:1px solid black;")

        resource_monitor_button = QPushButton(self)
        resource_monitor_button.setText("F10")


        self.firewall_on_button = QPushButton(self)
        self.firewall_on_button.setText("F11")
        self.firewall_on_button.clicked.connect(self.test)
        self.firewall_on_button.setFixedSize(100, 23)

        self.firewall_off_button = QPushButton(self)
        self.firewall_off_button.setText("F12")


        option_label = QLabel("Options")
        hot_key_label = QLabel("HotKeys")
        # row and column
        main_layout.addWidget(option_label, 0, 0)
        main_layout.addWidget(hot_key_label, 0, 1)
        main_layout.addWidget(self.firewall_on_button, 1,1)
        main_layout.addWidget(firewall_on_hot_key,1,0 )

        main_layout.addWidget(firewall_off_hot_key, 2, 0)
        main_layout.addWidget(self.firewall_off_button, 2, 1)

        main_layout.addWidget(resource_monitor_button, 3, 1)
        main_layout.addWidget(resource_monitor_key,  3, 0)

        main_layout.setHorizontalSpacing(10)

        main_layout.setColumnStretch(0,2)



        self.setLayout(main_layout)

    def test(self):
        self.firewall_on_button.setStyleSheet("background-color:yellow;border:0.5px solid black;")
        self.firewall_on_button.setText("Select a hotkey...")
        test = InputCheck(self)
        test.start()




    def keyPressEvent(self, key):
        pass


class InputCheck(QThread):

    def __init__(self, parent =None):
        super().__init__(parent)


    def __del__(self):
        self.wait()

    def run(self):
        key_stroke_found = False

        while not key_stroke_found:
            print("1")




if __name__ =="__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)


    hot_key_window = HotKey()
    hot_key_window.show()
    sys.exit(app.exec_())