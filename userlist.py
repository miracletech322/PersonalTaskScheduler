from PySide6.QtWidgets import QWidget, QPushButton
from PySide6.QtCore import QFile, QTextStream

from ui_userlist import Ui_UserList

class UserList(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_UserList()
        self.ui.setupUi(self)
        self.parent = parent

        self.initCSS()
        self.loadUser()

    def initCSS(self):
        file = QFile(":/Resources/userlist.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
        
    def loadUser(self):
        userList = self.parent.funcLoadUser()
        for user in userList:
            btn = QPushButton(user['username'])
            btn.setProperty("userId", str(user['_id']))
            # btn.clicked.connect(self.handleBtnClick)
            self.ui.verticalLayout.addWidget(btn)
    
    def handleBtnClick(self):
        btn = self.sender()
        userId = btn.property("userId")
        username = btn.text()
        self.parent.funcUserSign(username, userId)