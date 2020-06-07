# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ip_scanner_ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import Qt
import packetsniffer

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(413, 648)
        Dialog.setMinimumSize(QtCore.QSize(413, 648))
        Dialog.setMaximumSize(QtCore.QSize(413, 648))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.add_ip_address = QtWidgets.QPushButton(Dialog)
        self.interface_options = QtWidgets.QComboBox(Dialog)
        self.setupInterfaces()

        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 5, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.scanning_buttons = QtWidgets.QPushButton(Dialog)
        self.scanning_buttons.setFocus()


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

    def


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GTA V SOLO KIT"))
        self.scanning_buttons.setText(_translate("Dialog", "Start"))
        self.add_ip_address.setText(_translate("Dialog", "Add IP Address"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
