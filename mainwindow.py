from PySide6.QtCore import Qt, QFile, QTextStream, QTimer
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMdiSubWindow
from PySide6.QtGui import QIcon
from pymongo import MongoClient

from bson import ObjectId
from qasync import asyncSlot
from datetime import datetime

from ui_mainwindow import Ui_MainWindow
from userlist import UserList
from usermanagement import UserManagement

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnUserList.clicked.connect(self.handleBtnUserList)
        self.ui.btnUserManagement.clicked.connect(self.handleBtnUserManagement)
        self.ui.btnTaskManagement.clicked.connect(self.handleBtnTaskManagement)
        self.ui.btnAccountabilityReports.clicked.connect(self.handleBtnAccountabilityReports)
        self.ui.btnUserName.clicked.connect(self.handleBtnUserName)

        self.initCSS()
        self.initLCD()
        self.initSystemTray()
        self.initMongoDB()

    def initSystemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(":/Resources/app.png"))
        self.tray_icon.show()
    
    def initLCD(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.slt_updateDateTime)
        self.timer.start(1000)
        self.slt_updateDateTime()
    
    def initCSS(self):
        file = QFile(":/Resources/mainwindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()

    def initMongoDB(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["dbPersonalTaskScheduler"]
        self.tableUsers = self.db["users"]
        return

    def handleBtnUserList(self):
        self.ui.btnUserList.setStyleSheet("background-color: #9933cc;")
        self.ui.btnUserManagement.setStyleSheet("")
        self.ui.btnTaskManagement.setStyleSheet("")
        self.ui.btnAccountabilityReports.setStyleSheet("")

        self.ui.mdiArea.closeAllSubWindows()

        widget = UserList(self)
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(sub)
        sub.showMaximized()

    
    def handleBtnUserManagement(self):
        self.ui.btnUserList.setStyleSheet("")
        self.ui.btnUserManagement.setStyleSheet("background-color: #9933cc;")
        self.ui.btnTaskManagement.setStyleSheet("")
        self.ui.btnAccountabilityReports.setStyleSheet("")

        self.ui.mdiArea.closeAllSubWindows()

        widget = UserManagement(self)
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(sub)
        sub.showMaximized()

    def handleBtnTaskManagement(self):
        self.ui.btnUserList.setStyleSheet("")
        self.ui.btnUserManagement.setStyleSheet("")
        self.ui.btnTaskManagement.setStyleSheet("background-color: #9933cc;")
        self.ui.btnAccountabilityReports.setStyleSheet("")
    
    def handleBtnAccountabilityReports(self):
        self.ui.btnUserList.setStyleSheet("")
        self.ui.btnUserManagement.setStyleSheet("")
        self.ui.btnTaskManagement.setStyleSheet("")
        self.ui.btnAccountabilityReports.setStyleSheet("background-color: #9933cc;")
    
    def handleBtnUserName(self):
        return

    def slt_updateDateTime(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.lcdDateTime.display(current_time)

    def funcLoadUser(self):
        all_users = list(self.tableUsers.find())
        return all_users

    def funcInsertUser(self, username):
        userId = self.tableUsers.insert_one({
            "username": username
        }).inserted_id
        return str(userId)

    def funcDeleteUser(self, userId):
        self.tableUsers.delete_one({
            "_id": ObjectId(userId)
        })
    
    def funcUserSign(self, username, userId):
        self.ui.btnUserName.setProperty("userId", userId)
        self.ui.btnUserName.setText(username)
