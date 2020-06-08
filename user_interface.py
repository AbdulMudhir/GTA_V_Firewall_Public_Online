# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'public_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ip_sniffer import Ui_Dialog
from pathlib import Path
import json, os
import firewall

from pynput.keyboard import Key, Listener, KeyCode, HotKey, GlobalHotKeys


class Ui_MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

        #  will be used to set up hot keys to turn on and off firewall
        changeFirewallStatus = GlobalHotKeys({'<f11>': self.turnOnFirewall,
                                              '<f12>': self.turnOffFirewall
                                              })
        changeFirewallStatus.start()

        self.tray_icon = QSystemTrayIcon(self)
        self.settings_file = {}
        # will  be used for setting hot keys
        self.firewall_active = False
        self.hold_control = False

        self.ip_address_scope = ""
        self.gta_icon = QIcon("gta_icon.png")
        self.setupUi()

        self.firewall_status()
        self.create_setting_file()
        self.setupTrayIcon()

    def setupUi(self):

        self.resize(400, 800)
        self.setMaximumSize(QtCore.QSize(400, 600))
        self.setWindowIcon(self.gta_icon)

        # main screen
        self.centralwidget = QtWidgets.QWidget(self)
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

        # create 2 separate layout one for the layout and other is for holding the buttons
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
        self.scan_lobby_ip.clicked.connect(self.displayLobbyScanWindow)

        self.ip_address_layout.addWidget(self.scan_lobby_ip)

        add_remove_firewall_layout = QtWidgets.QHBoxLayout()

        add_remove_firewall_layout.setSpacing(0)

        self.add_firewall_rule_button = QtWidgets.QPushButton()
        add_remove_firewall_layout.addWidget(self.add_firewall_rule_button)

        self.remove_firewall_rule_button = QtWidgets.QPushButton()
        add_remove_firewall_layout.addWidget(self.remove_firewall_rule_button)

        self.add_firewall_rule_button.clicked.connect(self.add_firewall)
        self.remove_firewall_rule_button.clicked.connect(self.remove_firewall)

        self.firewall_settings.addLayout(add_remove_firewall_layout)

        self.firewall_settings.addLayout(self.ip_address_layout)

        # will be used to display the ip address white listed
        self.tableView = QtWidgets.QTableWidget(self.frame)

        self.firewall_settings.addWidget(self.tableView)

        self.gridLayout_3.addLayout(self.firewall_settings, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)

        self.buttons = QtWidgets.QHBoxLayout()
        self.firewall_button = QtWidgets.QPushButton(self.centralwidget)
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

        self.tableView.setColumnCount(1)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.tableView.setHorizontalHeaderLabels(["IP Address"])

        # second window for scanning lobby ip _ add
        self.Dialog = QtWidgets.QDialog(self)
        self.second_window = Ui_Dialog()
        self.second_window.setupUi(self.Dialog)



        self.setCentralWidget(self.centralwidget)
        self.focusWidget()
        self.setTextForButtons()

    def displayLobbyScanWindow(self):

        self.Dialog.show()


    def showWindow(self):
        self.show()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()

    def firewall_status(self):

        # will be used to display that a firewall does not exist
        if firewall.firewall_exist():
            self.ip_address_scope = firewall.firewall_scopes_list().split(",")
            self.enable_firewall_settings_buttons()
            self.tableView.setRowCount(len(self.ip_address_scope))
            self.update_table()
            self.update_firewall_button_status()

        else:

            self.disable_firewall_settings_buttons()

    def update_firewall_button_status(self):

        self.firewall_active = firewall.firewall_active()

        if self.firewall_active:
            self.firewall_button.setText("Firewall Mode (ON)")
            self.firewall_button.setStyleSheet("background-color:#00FF00;")
        else:
            self.firewall_button.setText("Firewall Mode (OFF)")
            self.firewall_button.setStyleSheet("background-color:red;")

    # check events from application
    def changeEvent(self, event):
        # check for events tht causes windows state to change
        if event.type() == QtCore.QEvent.WindowStateChange:
            # check if it has been minimised
            if self.windowState() & QtCore.Qt.WindowMinimized:
                # ignore the event
                event.ignore()
                # create new event
                self.hide()
                self.tray_icon.showMessage("GTA V TOOLKIT", "Application has been minimised to tray",
                                           QSystemTrayIcon.NoIcon, 2000)

    def turnOnFirewall(self):
        if firewall.firewall_exist():

            if not self.firewall_active:
                print("user held control and f1")
                self.tray_icon.showMessage(self.windowTitle(), "Firewall On")
                firewall.enable_firewall_rule()
                self.update_firewall_button_status()

    def turnOffFirewall(self):

        if firewall.firewall_exist():

            if self.firewall_active:
                print("user held control and f2")
                self.tray_icon.showMessage(self.windowTitle(), "Firewall off")
                firewall.disable_firewall_rule()
                self.update_firewall_button_status()

    def setupTrayIcon(self):
        self.tray_icon.setIcon(self.gta_icon)

        tray_menu = QMenu()
        exit_Application = tray_menu.addAction("Exit")
        exit_Application.triggered.connect(self.close)
        exit_Application.setIcon(QIcon("exit"))

        show_application = tray_menu.addAction("Show")
        show_application.triggered.connect(self.showWindow)
        show_application.setIcon(QIcon("show"))

        self.tray_icon.show()

        self.tray_icon.setContextMenu(tray_menu)

    def setTextForButtons(self):
        self.firewall_button.setText("Firewall Mode (OFF)")
        self.add_firewall_rule_button.setText("Add Firewall Rule")
        self.remove_firewall_rule_button.setText("Remove Firewall Rule")
        self.setWindowTitle("GTA V SOLO KIT")
        self.label.setText("Firewall Settings")
        self.file_path_directory.setPlaceholderText("File Path")
        self.file_path.setText("GTA V Path")
        self.add_ip_address_button.setText("Add IP Address (optional)")
        self.remove_ip_address_button.setText("Remove IP Address")
        self.ip_address_edit_text.setPlaceholderText("IP Address")
        self.scan_lobby_ip.setText("Scan Lobby IP Address")
        self.resource_monitor_button.setText("Resource Monitor")

    def update_table(self):

        self.ip_address_scope = firewall.ip_address_without_scope()

        self.tableView.setRowCount(len(self.ip_address_scope))

        if not self.ip_address_scope:
            self.tableView.setRowCount(1)
            self.tableView.setItem(0, 0, QtWidgets.QTableWidgetItem("Any"))

        else:
            for index, ip_address in enumerate(self.ip_address_scope):
                self.tableView.setItem(index, 0, QtWidgets.QTableWidgetItem(ip_address))

    def firewall_mode(self):

        if not self.firewall_active:
            firewall.enable_firewall_rule()
            self.update_firewall_button_status()
        else:
            firewall.disable_firewall_rule()
            self.update_firewall_button_status()

    def add_ip_address(self):

        ip_address = self.ip_address_edit_text.text().strip()

        if firewall.valid_ip_address(ip_address):

            whitelist = AddIPThread(ip_address, self.update_table)
            whitelist.start()

        else:
            # for debugging
            print("ip address already exist")

    def remove_ip_address(self):
        # ip_address = self.ip_address_edit_text.text()
        selected_ip_address = self.tableView.selectedItems()

        if selected_ip_address:

            if len(selected_ip_address) > 1:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("Confirm")
                message_box.setText("Are you sure you want to delete?")
                message_box.setIcon(QtWidgets.QMessageBox.Critical)
                message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                message_box.buttonClicked.connect(self.messageBoxConfirmationRemoval)
                message_box.exec_()

            else:
                firewall.remove_white_list(selected_ip_address[0].text())
                self.update_table()

        else:
            pass

    def messageBoxConfirmationRemoval(self, button):
        if button.text() == "&Yes":
            worker_thread = RemoveIPThread(self.tableView, self.update_table)

            worker_thread.start()

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

    def add_firewall(self):

        added_firewall_rule = firewall.add_firewall_rule(self.file_path_directory.text())

        if added_firewall_rule:
            self.enable_firewall_settings_buttons()
            self.update_table()

    def remove_firewall(self):

        remove_firewall_rule = firewall.delete_firewall_rule()
        if remove_firewall_rule:
            self.disable_firewall_settings_buttons()
            self.tableView.setRowCount(0)
            self.ip_address_edit_text.setText("")

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

            json_settings = {"GTA_FILE_PATH": "",
                             "IP_Address": {
                             }

                             }

            self.settings_file = json_settings
            update_setting_file = json.dump(json_settings, open("settings.json", "w"))


class RemoveIPThread(QThread):

    def __init__(self, tableWidget, update_table, parent=None):
        super(RemoveIPThread, self).__init__(parent)
        self.tableView = tableWidget
        self.update_table = update_table

    def __del__(self):
        self.wait()

    def run(self):
        # loop through the ip address selected
        for ip_address in self.tableView.selectedItems():
            firewall.remove_white_list(ip_address.text())

        self.update_table()


class AddIPThread(QThread):

    def __init__(self, ip_address, update_table, parent=None):
        super(AddIPThread, self).__init__(parent)
        self.ip_address = ip_address
        self.update_table = update_table

    def __del__(self):
        self.wait()

    def run(self):
        if not firewall.ip_address_exist_in_scope(self.ip_address):
            firewall.add_white_list(self.ip_address)
            self.update_table()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
