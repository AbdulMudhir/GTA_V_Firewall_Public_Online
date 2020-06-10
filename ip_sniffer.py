# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ip_scanner_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import firewall
import packetsniffer


class Ui_Dialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent)
        # will be used to pass information across to main window
        self.main_window = parent
        self.setupUi()

    def setupUi(self):
        self.resize(413, 648)
        self.setMinimumSize(QtCore.QSize(413, 648))
        self.setMaximumSize(QtCore.QSize(413, 648))

        self.network_interface = None
        self.network_name, self.network_description = packetsniffer.network_interfaces()

        self.gridLayout = QtWidgets.QGridLayout(self)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.add_ip_address = QtWidgets.QPushButton(self)
        self.add_ip_address.clicked.connect(self.add_ip_address_from_table)
        self.interface_options = QtWidgets.QComboBox(self)
        self.setWindowIcon(QIcon('gta_icon.png'))
        self.setupInterfaces()

        self.tableWidget.setColumnCount(1)
        # prevent tables from  being edited
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["IP Address"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.scanning_buttons = QtWidgets.QPushButton(self)
        self.scanning_buttons.clicked.connect(self.scanIPAddressInLobby)
        self.scanning_buttons.setFocus()

        interface_label = QtWidgets.QLabel(self)
        interface_label.setText("Network Interface")

        self.verticalLayout.addWidget(interface_label)
        self.verticalLayout.addWidget(self.interface_options)
        self.verticalLayout.addWidget(self.scanning_buttons)
        self.verticalLayout.addWidget(self.add_ip_address)

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        # prevent from switching between main window while it is opened
        self.setWindowModality(Qt.ApplicationModal)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def setupInterfaces(self):

        if self.network_description:
            self.interface_options.addItems(self.network_description)

    def scanIPAddressInLobby(self):

        network_description_index = self.interface_options.currentIndex()

        network_name = self.network_name[network_description_index]

        sniffer = SnifferThread(self)
        sniffer.interface = network_name
        sniffer.ip_address.connect(self.ip_address_scanned)
        sniffer.start()

    def ip_address_scanned(self, ip_addresses):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(ip_addresses))

        for index ,ip_address in enumerate(ip_addresses):
            self.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(ip_address))


    def add_ip_address_from_table(self):

        ip_addresses = self.tableWidget.selectedItems()

        if len(ip_addresses) >= 1:
            add_ip_thread = AddIPThread(ip_addresses, self.main_window.update_table)
            add_ip_thread.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GTA V SOLO KIT"))
        self.scanning_buttons.setText(_translate("Dialog", "Scan Lobby"))
        self.add_ip_address.setText(_translate("Dialog", "Add IP Address"))


class AddIPThread(QThread):

    def __init__(self, ip_addresses, main_window_table, parent=None):
        super(AddIPThread, self).__init__(parent)
        self.ip_addresses_item = ip_addresses
        self.tableWidget = main_window_table

    def __del__(self):
        self.wait()

    def run(self):
        # create a list of ip address that do not exist on the table
        ip_addresses_text = [ip.text() for ip in self.ip_addresses_item if
                             not firewall.ip_address_exist_in_scope(ip.text())]

        if ip_addresses_text:
            ip_addresses = ",".join(ip_addresses_text)
            firewall.add_white_list(ip_addresses)

            self.tableWidget()


class SnifferThread(QThread):
    ip_address = pyqtSignal(list)

    def __init__(self, parent=None):
        super(SnifferThread, self).__init__(parent)
        self.interface = None

    def __del__(self):
        self.wait()

    def run(self):
        ip_address = packetsniffer.scan_ip_address()

        self.ip_address.emit(ip_address)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
