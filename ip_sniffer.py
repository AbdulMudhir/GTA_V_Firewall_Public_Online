# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ip_scanner_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread
import packetsniffer


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.resize(413, 648)
        Dialog.setMinimumSize(QtCore.QSize(413, 648))
        Dialog.setMaximumSize(QtCore.QSize(413, 648))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.add_ip_address = QtWidgets.QPushButton(Dialog)
        self.interface_options = QtWidgets.QComboBox(Dialog)
        Dialog.setWindowIcon(QIcon('gta_icon.png'))
        self.setupInterfaces()

        self.tableWidget.setColumnCount(1)
        self.tableWidget.setHorizontalHeaderLabels(["IP Address"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.scanning_buttons = QtWidgets.QPushButton(Dialog)
        self.scanning_buttons.clicked.connect(self.scanIPAddressInLobby)
        self.scanning_buttons.setFocus()

        interface_label = QtWidgets.QLabel(Dialog)
        interface_label.setText("Network Interface")

        self.verticalLayout.addWidget(interface_label)
        self.verticalLayout.addWidget(self.interface_options)
        self.verticalLayout.addWidget(self.scanning_buttons)
        self.verticalLayout.addWidget(self.add_ip_address)

        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)

        # prevent from switching between main window while it is opened
        Dialog.setWindowModality(Qt.ApplicationModal)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def setupInterfaces(self):
        network_adapters = packetsniffer.network_interface

        if network_adapters:
            self.interface_options.addItems(network_adapters)

    def scanIPAddressInLobby(self):
        sniffer = SnifferThread(self.tableWidget, "Ethernet")
        sniffer.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GTA V SOLO KIT"))
        self.scanning_buttons.setText(_translate("Dialog", "Scan Lobby"))
        self.add_ip_address.setText(_translate("Dialog", "Add IP Address"))


class SnifferThread(QThread):

    def __init__(self, table, interface, parent=None):
        super(SnifferThread, self).__init__(parent)
        self.interface = interface
        self.table = table
        self.ip_address = None

    def __del__(self):
        self.wait()

    def run(self):
        self.ip_address = packetsniffer.scan_ip_address()

        self.table.setRowCount(len(self.ip_address))

        for index, ip_address in enumerate(self.ip_address):
            self.table.setItem(index, 0, QtWidgets.QTableWidgetItem(ip_address))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
