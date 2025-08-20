from PySide6.QtWidgets import QWidget, QDialog, QTableWidgetItem, QMessageBox
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_taskmanagement import Ui_TaskManagement
from taskdialog import TaskDialog

class TaskManagement(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_TaskManagement()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.tableWidget.verticalHeader().setVisible(False)
        # self.ui.tableWidget.horizontalHeader().setVisible(False)
        self.ui.tableWidget.setColumnWidth(1, 200)
        self.ui.tableWidget.setColumnWidth(2, 500)
        self.ui.tableWidget.setColumnHidden(4, True)

        self.ui.tableWidget.cellDoubleClicked.connect(self.handleEditTask)
        self.ui.btnPlus.clicked.connect(self.handleBtnPlus)
        self.ui.btnMinus.clicked.connect(self.handleBtnMinus)

        self.initCSS()
        self.loadTask()
    
    def initCSS(self):
        file = QFile(":/Resources/taskmanagement.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def loadTask(self):
        taskList = self.parent.funcLoadTask()
        row = 0
        for task in taskList:
            self.ui.tableWidget.insertRow(row)
            item = QTableWidgetItem(task['time'])
            self.ui.tableWidget.setItem(row, 0, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(task['title'])
            self.ui.tableWidget.setItem(row, 1, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(task['description'])
            self.ui.tableWidget.setItem(row, 2, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(task['manual'])
            self.ui.tableWidget.setItem(row, 3, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(str(task['_id']))
            self.ui.tableWidget.setItem(row, 4, item)
            row = row + 1

    def handleBtnPlus(self):
        dlg = TaskDialog(self)
        if QDialog.Rejected == dlg.exec():
            return

        taskId = self.parent.funcCreateTask(dlg.title, dlg.description, dlg.time.toString("hh:mm"), dlg.manual)
        row = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row)

        item = QTableWidgetItem(dlg.time.toString("hh:mm"))
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(row, 0, item)

        item = QTableWidgetItem(dlg.title)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(row, 1, item)

        item = QTableWidgetItem(dlg.description)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(row, 2, item)

        item = QTableWidgetItem(dlg.manual)
        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        self.ui.tableWidget.setItem(row, 3, item)
        
        self.ui.tableWidget.setItem(row, 4, QTableWidgetItem(taskId))

    def handleBtnMinus(self):
        index = self.ui.tableWidget.currentRow()
        if index < 0:
            QMessageBox.warning(self, "No Selection", "Please select a task to remove.")
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", f'Are you sure to delete selected task("{self.ui.tableWidget.item(index, 0).text()}")?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        taskId = self.ui.tableWidget.item(index, 4).text()
        self.parent.funcDeleteTask(taskId)

        self.ui.tableWidget.removeRow(index)
    
    def handleEditTask(self, row, column):
        time = self.ui.tableWidget.item(row, 0).text()
        title = self.ui.tableWidget.item(row, 1).text()
        description = self.ui.tableWidget.item(row, 2).text()
        manual = self.ui.tableWidget.item(row, 3).text()
        taskId = self.ui.tableWidget.item(row, 4).text()
        dlg = TaskDialog(self, time, title, description, manual, taskId)
        if dlg.exec() == QDialog.Rejected:
            return
        
        if self.parent.funcUpdateTask(dlg.time, dlg.title, dlg.description, dlg.manual, dlg.taskId):
            item = QTableWidgetItem(dlg.time.toString("hh:mm"))
            self.ui.tableWidget.setItem(row, 0, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(dlg.title)
            self.ui.tableWidget.setItem(row, 1, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(dlg.description)
            self.ui.tableWidget.setItem(row, 2, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            item = QTableWidgetItem(dlg.manual)
            self.ui.tableWidget.setItem(row, 3, item)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
