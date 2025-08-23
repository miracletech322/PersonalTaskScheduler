from PySide6.QtCore import Qt, QFile, QTextStream, QTimer, Signal
from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMdiSubWindow, QMessageBox, QDialog, QApplication, QMenu
from PySide6.QtGui import QIcon, QPixmap, QAction
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
from authwindow import AuthWindow

from ui_mainwindow import Ui_MainWindow
import global_vars

class MainWindow(QMainWindow):
    themeChanged = Signal()

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

    def initSystemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(global_vars.app_dir + "/assets/app.png"))

        # Context menu (with parent to avoid GC)
        # tray_menu = QMenu(self)

        # exit_action = QAction("Exit", self)
        # exit_action.triggered.connect(QApplication.instance().quit)
        # tray_menu.addAction(exit_action)

        # self.tray_icon.setContextMenu(tray_menu)
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
        # self.slt_handleCheckTask()

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

        url = ":/Resources/mainwindow.qss"
        if global_vars.app_theme == "Light Mode":
            self.ui.chkAppMode.setChecked(True)
            url = ":/Resources/mainwindow_light.qss"

        file = QFile(url)
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
        self.tableLogs = self.db["logs"]

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
        dlg = AuthWindow(self)
        if dlg.exec() == QDialog.Rejected:
            return
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
        if self.ui.btnUserName.text() == "CLOCK IN":
            self.handleBtnUserList()
        else:
            reply = QMessageBox.question(self, "Clock Out", f'Do you want to clock out from "{self.ui.btnUserName.text()}" account?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
            else:
                self.ui.btnUserName.setText("CLOCK IN")
    
    def handleBtnSetting(self):
        dlg = AuthWindow(self)
        if dlg.exec() == QDialog.Rejected:
            return

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
            global_vars.app_theme = "Light Mode"
        else:
            global_vars.settings.setValue("theme", "Dark Mode")
            global_vars.app_theme = "Dark Mode"
            
        self.initCSS()
        self.themeChanged.emit()

    def slt_handleCheckTask(self):
        now = datetime.now()
        time_str = now.strftime("%H:%M")
        taskList = self.funcFindTask(time_str)
        now = datetime.now()
        for task in taskList:
            if task['description'] == "AUTO CLOCK OUT":
                self.ui.btnUserName.setProperty("userId", "")
                self.ui.btnUserName.setText("CLOCK IN")
                continue

            # if task['time'] == "08:00" and task['description'] == "ENABLE DAY SHIFT CLOCK IN":
            #     self.ui.btnUserName.setProperty("userId", "68a24744637ac75ed99189e2")
            #     self.ui.btnUserName.setText("Day Shift")
            
            # if task['time'] == "22:00" and task['description'] == "ENABLE NIGHT SHIFT CLOCK IN":
            #     self.ui.btnUserName.setProperty("userId", "68a24748637ac75ed99189e3")
            #     self.ui.btnUserName.setText("Night Shift")

            self.alertWindow.setContentData({
                'title': task['title'],
                'description': task['description'],
                'taskId': str(task['_id']),
                'userId': self.ui.btnUserName.property("userId"),
                'manual': task['manual'],
            })
            self.alertWindow.showFullScreen()
            self.alertWindow.exec()

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
        self.ui.btnUserName.setText(username + " - CLOCK OUT")

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
    
    def funcLoadLogs(self, filter_date=None):
        match_stage = {}
        if filter_date:
            # Start and end of the day
            start = datetime.combine(filter_date, datetime.min.time())
            end = datetime.combine(filter_date, datetime.max.time())
            match_stage = {"$match": {"timestamp": {"$gte": start, "$lte": end}}}

        pipeline = []

        if match_stage:
            pipeline.append(match_stage)

        pipeline.extend([
            {
                "$addFields": {
                    "taskObjId": {
                        "$cond": [
                            {"$ifNull": ["$taskId", False]},
                            {"$toObjectId": "$taskId"},
                            None
                        ]
                    },
                    "userObjId": {
                        "$cond": [
                            {"$ifNull": ["$userId", False]},
                            {"$toObjectId": "$userId"},
                            None
                        ]
                    }
                }
            },
            {
                "$lookup": {
                    "from": "users",
                    "localField": "userObjId",
                    "foreignField": "_id",
                    "as": "user"
                }
            },
            {"$unwind": {"path": "$user", "preserveNullAndEmptyArrays": True}},
            {
                "$lookup": {
                    "from": "tasks",
                    "localField": "taskObjId",
                    "foreignField": "_id",
                    "as": "task"
                }
            },
            {"$unwind": {"path": "$task", "preserveNullAndEmptyArrays": True}},
            {
                "$project": {
                    "_id": 1,
                    "status": 1,
                    "timestamp": 1,
                    "userId": 1,
                    "taskId": 1,
                    "user": "$user",
                    "task": "$task"
                }
            }
        ])

        result = list(self.tableLogs.aggregate(pipeline))
        return result

    def funcConfirmAlert(self, taskId, userId):
        log = {
            "taskId": taskId,
            "userId": userId,
            "status": "Confirmed",
            "timestamp": datetime.now()
        }
        result = self.tableLogs.insert_one(log)
    
    def funcYesAlert(self, taskId, userId):
        log = {
            "taskId": taskId,
            "userId": userId,
            "status": "Yes",
            "timestamp": datetime.now()
        }
        result = self.tableLogs.insert_one(log)

    def funcNoAlert(self, taskId, userId):
        log = {
            "taskId": taskId,
            "userId": userId,
            "status": "No",
            "timestamp": datetime.now()
        }
        result = self.tableLogs.insert_one(log)
    
    def funcMissed(self, taskId, userId):
        log = {
            "taskId": taskId,
            "userId": userId,
            "status": "Missed",
            "timestamp": datetime.now()
        }
        result = self.tableLogs.insert_one(log)
