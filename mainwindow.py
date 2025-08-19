from PySide6.QtCore import Qt, QFile, QTextStream, QTimer
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMdiSubWindow, QMessageBox, QDialog, QApplication
from PySide6.QtGui import QIcon, QPixmap
from pymongo import MongoClient

from bson import ObjectId
from qasync import asyncSlot
from datetime import datetime
import shutil

from userlist import UserList
from usermanagement import UserManagement
from taskmanagement import TaskManagement
from accountabilityreports import AccountabilityReports
from alertwindow import AlertWindow
from settingwindow import SettingWindow

from ui_mainwindow import Ui_MainWindow
import global_vars

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
        self.ui.btnSetting.clicked.connect(self.handleBtnSetting)
        self.ui.chkAppMode.toggled.connect(self.handleModeToggle)

        self.initSystemTray()
        self.initCSS()
        self.initMongoDB()
        self.initLCD()
        self.initMinutelyTimer()
        self.handleBtnUserList()
        self.alertWindow = AlertWindow(self)

        self.ui.labelAppMode.setVisible(False)
        self.ui.chkAppMode.setVisible(False)

    def initSystemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(global_vars.app_dir + "/assets/app.png"))
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.slt_trayIconActivated)
    
    def initLCD(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.slt_updateDateTime)
        self.timer.start(1000)
        self.slt_updateDateTime()

    def initMinutelyTimer(self):
        self.globalTimer = QTimer()
        self.globalTimer.timeout.connect(self.slt_handleCheckTask)
        self.globalTimer.start(1000 * 60)
        self.slt_handleCheckTask()

    def initCSS(self):
        self.setWindowTitle(global_vars.app_title)
        self.ui.labelTitle.setText(global_vars.app_title)
        pixmap = QPixmap(global_vars.app_dir + "/assets/app.png")
        pixmap = pixmap.scaled(
            self.ui.labelLogo.width(),
            self.ui.labelLogo.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.ui.labelLogo.setPixmap(pixmap)
        self.tray_icon.setIcon(QIcon(global_vars.app_dir + "/assets/app.png"))
        app = QApplication.instance()
        if app is not None:
            app.setWindowIcon(QIcon(global_vars.app_dir + "/assets/app.png"))


        file = QFile(":/Resources/mainwindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()

    def initMongoDB(self):
        self.client = MongoClient("mongodb+srv://miracletech322:HgqjOfh0QjIAWJDN@cluster0.b1te6ax.mongodb.net/")
        self.db = self.client["sample_mflix"]
        self.tableUsers = self.db["users"]
        self.tableTasks = self.db["tasks"]

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

        widget = TaskManagement(self)
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(sub)
        sub.showMaximized()
    
    def handleBtnAccountabilityReports(self):
        self.ui.btnUserList.setStyleSheet("")
        self.ui.btnUserManagement.setStyleSheet("")
        self.ui.btnTaskManagement.setStyleSheet("")
        self.ui.btnAccountabilityReports.setStyleSheet("background-color: #9933cc;")

        widget = AccountabilityReports(self)
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.mdiArea.addSubWindow(sub)
        sub.showMaximized()
    
    def handleBtnUserName(self):
        if self.ui.btnUserName.text() == "Sign In":
            self.handleBtnUserList()
        else:
            reply = QMessageBox.question(self, "Sign Out", f'Do you want to sign out from "{self.ui.btnUserName.text()}" account?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            else:
                self.ui.btnUserName.setText("Sign In")
    
    def handleBtnSetting(self):
        dlg = SettingWindow(self)
        if dlg.exec() == QDialog.Rejected:
            return
        
        global_vars.settings.setValue("title", dlg.ui.edtAppTitle.text())
        global_vars.app_title = dlg.ui.edtAppTitle.text()
        if dlg.fileName != global_vars.app_dir + "/assets/app.png":
            shutil.copy2(dlg.fileName, global_vars.app_dir + "/assets/app.png")
        self.initCSS()

    def handleModeToggle(self, toggle):
        if toggle:
            global_vars.settings.setValue("theme", "Light Mode")
        else:
            global_vars.settings.setValue("theme", "Dark Mode")
        self.initCSS()

    def slt_handleCheckTask(self):
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        taskList = self.funcFindTask(time_str)
        now = datetime.now()
        for task in taskList:
            self.alertWindow.setContentData({
                'title': task['title'],
                'description': task['description'],
                'taskId': str(task['_id']),
            })
            self.alertWindow.showFullScreen()

    def slt_updateDateTime(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.lcdDateTime.display(current_time)

    def slt_trayIconActivated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

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

        QMessageBox.information(self, "Login", f"Welcome {username}! You have successfully signed in.")

    def funcCreateTask(self, title, description, time, manual):
        taskId = self.tableTasks.insert_one({
            "title": title,
            "description": description,
            "time": time,
            "manual": manual
        }).inserted_id
        return str(taskId)

    def funcUpdateTask(self, time, title, description, manual, taskId):
        res = self.tableTasks.update_one(
            {
                "_id": ObjectId(taskId)
            },
            {
                "$set": {
                    "title": title,
                    "description": description,
                    "time": time.toString("hh:mm"),
                    "manual": manual
                }
            }
        )
        return res.modified_count > 0

    def funcDeleteTask(self, taskId):
        self.tableTasks.delete_one({
            "_id": ObjectId(taskId)
        })

    def funcLoadTask(self):
        all_tasks = list(self.tableTasks.find())
        return all_tasks
    
    def funcFindTask(self, time_str):
        matched = list(self.tableTasks.find({"time": time_str}))
        return matched

    def funcConfirmAlert(self, taskId):
        print(f"funcConfirmAlert: {taskId}")
    
    def funcYesAlert(self, taskId):
        print(f"funcYesAlert: {taskId}")

    def funcNoAlert(self, taskId):
        print(f"functionNoAlert: {taskId}")
