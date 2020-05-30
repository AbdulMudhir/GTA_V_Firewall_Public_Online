# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'public_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 800)
        MainWindow.setMaximumSize(QtCore.QSize(400, 800))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.firewall_settings = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("font-size:15px;\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 178, 102, 255), stop:0.55 rgba(235, 148, 61, 255), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
"border:no;\n"
"border-bottom:1px solid black;\n"
"")
        self.firewall_settings.addWidget(self.label)
        self.gta_v_file_path = QtWidgets.QHBoxLayout()
        self.lineEdit = QtWidgets.QLineEdit(self.frame)


        self.gta_v_file_path.addWidget(self.lineEdit)
        self.file_path = QtWidgets.QPushButton(self.frame)
        self.gta_v_file_path.addWidget(self.file_path)
        self.firewall_settings.addLayout(self.gta_v_file_path)
        self.ip_address_layout = QtWidgets.QVBoxLayout()
        self.ip_address_options = QtWidgets.QHBoxLayout()
        self.add_ip_address = QtWidgets.QPushButton(self.frame)
        self.ip_address_options.addWidget(self.add_ip_address)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.ip_address_options.addWidget(self.pushButton)

        self.ip_address_layout.addLayout(self.ip_address_options)
        self.ip_address_edit_text = QtWidgets.QLineEdit(self.frame)
        self.ip_address_layout.addWidget(self.ip_address_edit_text)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.ip_address_layout.addWidget(self.pushButton_2)
        self.firewall_settings.addLayout(self.ip_address_layout)
        self.tableView = QtWidgets.QTableView(self.frame)

        self.firewall_settings.addWidget(self.tableView)
        self.gridLayout_3.addLayout(self.firewall_settings, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.buttons = QtWidgets.QHBoxLayout()
        self.firewall_button = QtWidgets.QPushButton(self.centralwidget)

        self.firewall_button.setMinimumSize(QtCore.QSize(25, 50))
        self.firewall_button.setMaximumSize(QtCore.QSize(218, 50))
        self.buttons.addWidget(self.firewall_button)
        self.resource_monitor_button = QtWidgets.QPushButton(self.centralwidget)

        self.resource_monitor_button.setMinimumSize(QtCore.QSize(25, 50))
        self.resource_monitor_button.setMaximumSize(QtCore.QSize(217, 50))

        self.buttons.addWidget(self.resource_monitor_button)
        self.gridLayout_2.addLayout(self.buttons, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Firewall Settings"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "File Path"))
        self.file_path.setText(_translate("MainWindow", "GTA V Path"))
        self.add_ip_address.setText(_translate("MainWindow", "Add IP Address"))
        self.pushButton.setText(_translate("MainWindow", "Remove IP Address"))
        self.ip_address_edit_text.setPlaceholderText(_translate("MainWindow", "IP Address", "IP Address"))
        self.pushButton_2.setText(_translate("MainWindow", "Scan Lobby IP Address"))
        self.firewall_button.setText(_translate("MainWindow", "Firewall Mode"))
        self.resource_monitor_button.setText(_translate("MainWindow", "Resource Monitor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
