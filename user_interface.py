# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'public_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from pathlib import Path
import json, os
import firewall


class Ui_MainWindow(object):

    def __init__(self):

        self.settings_file = {}
        self.firewall_active = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 800)
        MainWindow.setMaximumSize(QtCore.QSize(400, 600))
        # main screen
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)

        # setting the base frame as the main window
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        # setting the grid for the frame
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)

        # a vertical layout to store settings widgets
        self.firewall_settings = QtWidgets.QVBoxLayout()
        # setting a frame for the settings
        self.label = QtWidgets.QLabel(self.frame)
        # adding a label in the vertical box
        self.firewall_settings.addWidget(self.label)

        # create  file path horizontal layout
        self.gta_v_file_path = QtWidgets.QHBoxLayout()
        # directory path, will be used to retrieve the gta path for creating the firewall rule
        self.file_path_directory = QtWidgets.QLineEdit(self.frame)

        self.file_path_directory.setText(self.settings_file.get("GTA_FILE_PATH"))

        self.gta_v_file_path.addWidget(self.file_path_directory)

        # will be used to get gta v .exe if user is doesn't have copy paste
        self.file_path = QtWidgets.QPushButton(self.frame)

        self.file_path.clicked.connect(self.get_file_path)

        self.gta_v_file_path.addWidget(self.file_path)

        # adding the the gta v file path layout to firewall setting menu
        self.firewall_settings.addLayout(self.gta_v_file_path)

        self.create_setting_file()

        # create 2 seperate layout one for the layout and other is for holding the buttons
        self.ip_address_layout = QtWidgets.QVBoxLayout()

        # layout for holding the add and remove button
        self.ip_address_options = QtWidgets.QHBoxLayout()
        self.ip_address_options.setSpacing(0)

        self.add_ip_address_button = QtWidgets.QPushButton(self.frame)
        self.add_ip_address_button.clicked.connect(self.add_ip_address)

        self.ip_address_options.addWidget(self.add_ip_address_button)

        self.remove_ip_address_button = QtWidgets.QPushButton(self.frame)
        self.remove_ip_address_button.clicked.connect(self.remove_ip_address)

        self.ip_address_options.addWidget(self.remove_ip_address_button)

        self.ip_address_layout.addLayout(self.ip_address_options)
        self.ip_address_edit_text = QtWidgets.QLineEdit(self.frame)

        self.ip_address_layout.addWidget(self.ip_address_edit_text)
        self.scan_lobby_ip = QtWidgets.QPushButton(self.frame)

        self.ip_address_layout.addWidget(self.scan_lobby_ip)

        add_remove_firewall_layout = QtWidgets.QHBoxLayout()

        add_remove_firewall_layout.setSpacing(0)

        self.add_firewall_rule_button = QtWidgets.QPushButton()
        self.add_firewall_rule_button.setText("Add Firewall Rule")
        add_remove_firewall_layout.addWidget(self.add_firewall_rule_button)

        self.remove_firewall_rule_button = QtWidgets.QPushButton()
        self.remove_firewall_rule_button.setText("Remove Firewall Rule")
        add_remove_firewall_layout.addWidget(self.remove_firewall_rule_button)

        self.add_firewall_rule_button.clicked.connect(self.add_firewall)
        self.remove_firewall_rule_button.clicked.connect(self.remove_firewall)

        self.firewall_settings.addLayout(add_remove_firewall_layout)

        self.firewall_settings.addLayout(self.ip_address_layout)

        self.tableView = QtWidgets.QTableView(self.frame)

        self.firewall_settings.addWidget(self.tableView)

        self.gridLayout_3.addLayout(self.firewall_settings, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.buttons = QtWidgets.QHBoxLayout()
        self.firewall_button = QtWidgets.QPushButton(self.centralwidget)
        self.firewall_button.setText("Firewall Mode (OFF)")
        self.firewall_button.clicked.connect(self.firewall_mode)
        self.firewall_button.setStyleSheet("background-color:red;")

        self.firewall_button.setMinimumSize(QtCore.QSize(25, 50))
        self.firewall_button.setMaximumSize(QtCore.QSize(218, 50))
        self.buttons.addWidget(self.firewall_button)
        self.resource_monitor_button = QtWidgets.QPushButton(self.centralwidget)

        self.resource_monitor_button.setMinimumSize(QtCore.QSize(25, 50))
        self.resource_monitor_button.setMaximumSize(QtCore.QSize(217, 50))

        self.buttons.addWidget(self.resource_monitor_button)
        self.gridLayout_2.addLayout(self.buttons, 2, 0, 1, 1)

        # will be used to display that a firewall does not exist
        if firewall.firewall_exist():
            self.add_firewall_rule_button.setStyleSheet("background-color:#00FF00;")
            self.remove_firewall_rule_button.setStyleSheet("background-color:red;")

            self.enable_firewall_settings_buttons()
        else:
            self.remove_firewall_rule_button.setStyleSheet("background-color:red;")
            self.add_firewall_rule_button.setStyleSheet("background-color:red;")
            self.disable_firewall_settings_buttons()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def firewall_mode(self):

        if not self.firewall_active:
            self.firewall_active = True
            firewall.enable_firewall_rule()
            self.firewall_button.setText("Firewall Mode (ON)")
            self.firewall_button.setStyleSheet("background-color:#00FF00;")

        else:
            self.firewall_active = False
            firewall.disable_firewall_rule()
            self.firewall_button.setText("Firewall Mode (OFF)")
            self.firewall_button.setStyleSheet("background-color:red;")

    def add_ip_address(self):

        ip_address = self.ip_address_edit_text.text()

        if firewall.valid_ip_address(ip_address):

            if not firewall.ip_address_exist_in_scope(ip_address):
                firewall.add_white_list(ip_address)
            else:
                # for debugging
                print("ip address already exist")

    def remove_ip_address(self):
        ip_address = self.ip_address_edit_text.text()

        if firewall.valid_ip_address(ip_address):

            if firewall.ip_address_exist_in_scope(ip_address):
                firewall.remove_white_list(ip_address)
            else:
                # for debugging
                print("ip address doesn't exist")

    def get_file_path(self):

        gta_file_path = self.settings_file.get("GTA_FILE_PATH")

        home_directory = str(Path.home()) if not gta_file_path else gta_file_path

        file_dialog = QtWidgets.QFileDialog.getOpenFileName(self.frame, "Open file", home_directory,
                                                            "executable(*.exe)")
        file_path, _ = file_dialog

        file_path_format = os.path.realpath(file_path)

        if file_path and file_path != self.settings_file.get("GTA_FILE_PATH"):
            self.file_path_directory.setText(file_path_format)
            self.settings_file["GTA_FILE_PATH"] = os.path.realpath(file_path_format)

            json.dump(self.settings_file, open("settings.json", "w"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Firewall Settings"))
        self.file_path_directory.setPlaceholderText(_translate("MainWindow", "File Path"))
        self.file_path.setText(_translate("MainWindow", "GTA V Path"))
        self.add_ip_address_button.setText(_translate("MainWindow", "Add IP Address (optional)"))
        self.remove_ip_address_button.setText(_translate("MainWindow", "Remove IP Address"))
        self.ip_address_edit_text.setPlaceholderText(_translate("MainWindow", "IP Address", "IP Address"))
        self.scan_lobby_ip.setText(_translate("MainWindow", "Scan Lobby IP Address"))
        self.resource_monitor_button.setText(_translate("MainWindow", "Resource Monitor"))

    def add_firewall(self):

        added_firewall_rule = firewall.add_firewall_rule(self.file_path_directory.text())

        if added_firewall_rule:
            self.add_firewall_rule_button.setStyleSheet("background-color:#00FF00;")
            self.enable_firewall_settings_buttons()

        else:
            self.add_firewall_rule_button.setStyleSheet("background-color:red;")

    def remove_firewall(self):

        remove_firewall_rule = firewall.delete_firewall_rule()
        if remove_firewall_rule:
            self.disable_firewall_settings_buttons()

    def disable_firewall_settings_buttons(self):
        self.add_ip_address_button.setDisabled(True)
        self.remove_ip_address_button.setDisabled(True)
        self.add_firewall_rule_button.setDisabled(False)
        self.remove_firewall_rule_button.setDisabled(True)
        self.ip_address_edit_text.setDisabled(True)
        self.firewall_button.setDisabled(True)

        if self.firewall_active:
            self.firewall_active = False
            self.firewall_button.setText("Firewall Mode (OFF)")
            self.firewall_button.setStyleSheet("background-color:red;")

    def enable_firewall_settings_buttons(self):
        self.ip_address_edit_text.setDisabled(False)
        self.firewall_button.setDisabled(False)

        self.add_firewall_rule_button.setDisabled(True)
        self.remove_firewall_rule_button.setDisabled(False)
        self.add_ip_address_button.setDisabled(False)
        self.remove_ip_address_button.setDisabled(False)
        if not self.firewall_active:
            self.firewall_button.setText("Firewall Mode (OFF)")
            self.firewall_button.setStyleSheet("background-color:red;")





    def create_setting_file(self):

        current_cwd = os.getcwd()

        try:
            self.settings_file = json.load(open("settings.json"))
            gta_v_file_path = self.settings_file.get("GTA_FILE_PATH")
            self.file_path_directory.setText(gta_v_file_path)

        except FileNotFoundError:

            json_settings = {"GTA_FILE_PATH": ""}
            update_setting_file = json.dump(json_settings, open("settings.json", "w"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
