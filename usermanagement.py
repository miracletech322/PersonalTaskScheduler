from PySide6.QtWidgets import QWidget, QMessageBox, QTableWidgetItem
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_usermanagement import Ui_UserManagement

class UserManagement(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_UserManagement()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.tableWidget.horizontalHeader().setVisible(False)
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.setColumnHidden(1, True)
        self.ui.tableWidget.setColumnWidth(0, 800)

        self.ui.btnPlus.clicked.connect(self.handleBtnPlus)
        self.ui.btnMinus.clicked.connect(self.handleBtnMinus)

        self.initCSS()
        self.loadUser()

    def initCSS(self):
        file = QFile(":/Resources/usermanagement.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def loadUser(self):
        row = 0
        userList = self.parent.funcLoadUser()
        for user in userList:
            self.ui.tableWidget.insertRow(row)
            item = QTableWidgetItem(user['username'])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 0, item)

            item = QTableWidgetItem(str(user['_id']))
            self.ui.tableWidget.setItem(row, 1, item)
            row = row + 1
    
    def handleBtnPlus(self):
        username = self.ui.edtUser.text()
        if username == "":
            QMessageBox.warning(self, "Input Error", "Please enter a username.")
            return

        len = self.ui.tableWidget.rowCount()
        exist = False
        for row in range(len):
            item = self.ui.tableWidget.item(row, 0)
            if item is not None:
                if item.text().lower() == username.lower():
                    exist = True
                    QMessageBox.warning(self, "Duplicate", f"'{username}' already exists!")
        
        if exist:
            return
    
        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row)
        userId = self.parent.funcInsertUser(username)

        item = QTableWidgetItem(username)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(row, 0, item)

        item = QTableWidgetItem(userId)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(row, 1, item)
        self.ui.edtUser.clear()

    def handleBtnMinus(self):
        index = self.ui.tableWidget.currentRow()
        if index < 0:
            QMessageBox.warning(self, "No Selection", "Please select a user to remove.")
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", f'Are you sure to delete selected user("{self.ui.tableWidget.item(index, 0).text()}")?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        userId = self.ui.tableWidget.item(index, 1).text()
        self.parent.funcDeleteUser(userId)

        self.ui.tableWidget.removeRow(index)