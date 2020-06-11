# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'public_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ip_sniffer import Ui_Dialog
from pathlib import Path
import json, os
import firewall
import hotkey
from suspendprocess import GTASuspend
import ctypes, os

from pynput.keyboard import GlobalHotKeys


class Ui_MainWindow(QMainWindow):
    height = 600
    width = 400
    window_title = "GTA V SOLO KIT"

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        self.tray_icon = QSystemTrayIcon(self)
        self.settings_file = {}
        # will  be used for setting hot keysvisu
        self.firewall_active = False
        self.hold_control = False

        self.ip_address_scope = ""
        self.setupUi()

        self.firewall_status()
        self.create_setting_file()
        self.setupTrayIcon()
        self.set_up_help_window()
        self.update_global_hot_key()

        if not self.is_admin:
            self.notAdmin()

    def setupUi(self):
        # second window for scanning lobby ip _ add
        self.second_window = Ui_Dialog(self)
        self.gta_icon = QIcon("gta_icon.png")

        self.resize(self.width, self.height)
        self.setMaximumSize(QtCore.QSize(self.width, self.height))
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
        self.resource_monitor_button.clicked.connect(self.suspend_gta)

        self.resource_monitor_button.setMinimumSize(QtCore.QSize(25, 50))
        self.resource_monitor_button.setMaximumSize(QtCore.QSize(217, 50))

        self.buttons.addWidget(self.resource_monitor_button)
        self.gridLayout_2.addLayout(self.buttons, 2, 0, 1, 1)

        self.tableView.setColumnCount(1)

        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.tableView.setHorizontalHeaderLabels(["IP Address"])

        # prevent tables from  being edited
        self.tableView.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        menu_bar = self.menuBar()
        setting_menu = menu_bar.addAction("Keyboard Shortcut Settings")
        setting_menu.triggered.connect(self.display_shortcut_window)

        help_window = menu_bar.addAction("Help")
        help_window.triggered.connect(self.displayHelpScreen)
        self.help_dialog = QtWidgets.QDialog(self)

        self.gta_process = GTASuspend(self)
        self.gta_process.seconds.connect(self.seconds_process_down)

        self.shortcut_window = hotkey.HotKey(self)

        self.setCentralWidget(self.centralwidget)
        self.focusWidget()
        self.setTextForButtons()

    def seconds_process_down(self, seconds):

        self.resource_monitor_button.setText(f"GTA V Will Resume Process in {seconds}")

        if seconds == 0:
            self.resource_monitor_button.setText("Resource Monitor")

    def notAdmin(self):
        self.firewall_button.setDisabled(True)
        self.add_firewall_rule_button.setDisabled(True)
        self.remove_firewall_rule_button.setDisabled(True)
        self.add_ip_address_button.setDisabled(True)
        self.remove_ip_address_button.setDisabled(True)
        self.file_path_directory.setDisabled(True)
        self.file_path.setDisabled(True)
        self.ip_address_edit_text.setDisabled(True)
        self.tableView.setDisabled(True)

        self.second_window.add_ip_address.setDisabled(True)

        pop_up = QtWidgets.QDialog(self)
        pop_up.setWindowTitle(self.window_title+" - Run as Admin")
        layout = QtWidgets.QVBoxLayout()


        button = QtWidgets.QPushButton(self)
        button.setText("Okay")
        button.clicked.connect(lambda e: pop_up.close())

        pop_up.setFixedSize(300,70)
        button.setFixedSize(50,30)

        message = QtWidgets.QLabel("Please run as administrator to use some of the features")

        layout.addWidget(message, alignment=QtCore.Qt.AlignCenter)

        layout.addWidget(button, alignment=QtCore.Qt.AlignCenter)

        pop_up.setLayout(layout)

        pop_up.show()

    def suspend_gta(self):

        if not self.gta_process.isRunning():
            self.gta_process.start()

    def update_global_hot_key(self):

        self.hot_keys = json.load(open("settings.json", "r")).get("Hot_Key")

        method_calls = [self.turnOnFirewall, self.turnOffFirewall, self.suspend_gta]

        # remove the need to assign function if no key has been assigned

        hot_keys = {f"<{key}>": method_calls[index]
                    for index, (name, key) in enumerate(self.hot_keys.items()) if key != "None"}

        #  will be used to set up hot keys to turn on and off firewall
        self.changeFirewallStatus = GlobalHotKeys(hot_keys)
        self.changeFirewallStatus.start()

    def display_shortcut_window(self):

        self.shortcut_window.show()

    def set_up_help_window(self):

        self.help_dialog.setWindowTitle(self.window_title + "- HELP")
        layout = QtWidgets.QHBoxLayout()
        instruction = QtWidgets.QLabel("Instruction\n"
                                       "1. Add Firewall Rule\n"
                                       "2. Join a public lobby\n"
                                       "3. Turn on the Firewall (you can use shortcut key in game default key = F11)\n"
                                       "Give it few seconds(5) and everyone should be kicked out, If not "
                                       "simply turn off\n and on the firewall \n(using this application) to update GTA "
                                       "\n\n"
                                       "Adding your friends"
                                       "\nFollow the above instructions until you're in a solo lobby\n"
                                       "1. Turn off firewall\n"
                                       "2. Get your friends to join your solo lobby\n"
                                       "3. Add their IP address manually or use the Scan Lobby IP Address feature\n"
                                       "4. Turn on Firewall\n"
                                       "\nIf you're using the Scan Lobby IP Address\n"
                                       "1. Get your friends to join your solo public lobby (firewall off first)\n"
                                       "2. Click on Scan Lobby IP Address\n"
                                       "3. Click on Scan Lobby\n"
                                       "4. Select the IP address and click on Add IP address"
                                       "5. Turn on Firewall "
                                       "\n\nIf you have any questions, feel free to contact me on discord @ Hunter#2950"


                                       "")

        layout.addWidget(instruction)

        self.help_dialog.setFixedHeight(310)
        self.help_dialog.setFixedWidth(420)

        self.help_dialog.setLayout(layout)

    def displayHelpScreen(self):

        # prevent from switching between main window while it is opened
        self.help_dialog.show()

    def displayLobbyScanWindow(self):
        self.second_window.show()

    # used for tray icon to bring window back up
    def showWindow(self):
        self.show()
        # display the window  and brings it to focus when brought back up by tray icon
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)

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
                self.tray_icon.showMessage(self.windowTitle(), "Firewall On")
                firewall.enable_firewall_rule()
                self.update_firewall_button_status()

    def turnOffFirewall(self):

        if firewall.firewall_exist():

            if self.firewall_active:
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
        self.setWindowTitle(self.window_title)
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

        if not self.ip_address_scope:
            self.tableView.setRowCount(1)
            self.tableView.setItem(0, 0, QtWidgets.QTableWidgetItem("Private Session - None Allowed"))
        else:
            # remove the "private session not allowed Row"
            self.tableView.removeRow(0)
            self.tableView.setRowCount(len(self.ip_address_scope))

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

            whitelist = AddIPThread(ip_address, parent=self)
            whitelist.start()


        else:
            # for debugging
            print("ip address already exist")

    def remove_ip_address(self):
        # ip_address = self.ip_address_edit_text.text()
        selected_ip_address = self.tableView.selectedItems()

        if selected_ip_address:
            # will be displayed if multiple IP address were selected
            if len(selected_ip_address) > 1:
                message_box = QtWidgets.QMessageBox(self)
                message_box.setWindowTitle("Confirm")
                message_box.setText("Are you sure you want to delete?")
                message_box.setIcon(QtWidgets.QMessageBox.Critical)
                message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                message_box.buttonClicked.connect(self.messageBoxConfirmationRemoval)
                message_box.exec_()

            elif selected_ip_address[0].text() != "Private Session - None Allowed":

                firewall.remove_white_list(selected_ip_address[0].text())
                self.update_table()



        else:
            pass

    def messageBoxConfirmationRemoval(self, button):
        if button.text() == "&Yes":
            worker_thread = RemoveIPThread(self)
            worker_thread.selected_ip_address = self.tableView.selectedItems()
            worker_thread.finished.connect(lambda status: self.update_table())

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
                             },
                             "Hot_Key": {"F_ON": "F11",
                                         "F_OFF": "F12",
                                         "R_M": "F10"

                                         }

                             }

            self.settings_file = json_settings
            update_setting_file = json.dump(json_settings, open("settings.json", "w"))


class RemoveIPThread(QThread):

    finished = pyqtSignal(str)

    def __init__(self, parent=None):
        super(RemoveIPThread, self).__init__(parent)
        self.selected_ip_address = None

    def run(self):
        # get the strings value of the table rows
        ip_addresses = ",".join([ip.text() for ip in self.selected_ip_address])

        firewall.remove_white_list(ip_addresses)

        self.finished.emit("finished")


class AddIPThread(QThread):

    def __init__(self, ip_address, parent=None):
        super(AddIPThread, self).__init__(parent)
        self.ip_address = ip_address
        self.main_window = parent

    def __del__(self):
        self.wait()

    def run(self):
        if not firewall.ip_address_exist_in_scope(self.ip_address):
            firewall.add_white_list(self.ip_address)

            self.main_window.update_table()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
