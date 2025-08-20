from PySide6.QtWidgets import QWidget, QTableWidgetItem, QFileDialog
from PySide6.QtCore import Qt, QFile, QTextStream, QDate

from ui_accountabilityreports import Ui_AccountabilityReports

from openpyxl import Workbook

class AccountabilityReports(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_AccountabilityReports()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.btnExport.clicked.connect(self.handleBtnExport)
        self.ui.dateEdit.dateChanged.connect(self.handleDateEdit)

        self.initCSS()
        self.ui.dateEdit.setDate(QDate.currentDate())
        self.loadLogs()
        self.ui.tableWidget.verticalHeader().setVisible(False)
        self.ui.tableWidget.setColumnWidth(1, 140)
        self.ui.tableWidget.setColumnWidth(2, 370)
    
    def initCSS(self):
        file = QFile(":/Resources/accountabilityreports.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def loadLogs(self):
        date = self.ui.dateEdit.date().toPython()
        logs = self.parent.funcLoadLogs(date)
        self.ui.tableWidget.setRowCount(0)
        row = 0
        for log in logs:
            self.ui.tableWidget.insertRow(row)
            item = QTableWidgetItem(log['task']['time'])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 0, item)

            item = QTableWidgetItem(log['task']['title'])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 1, item)

            item = QTableWidgetItem(log['task']['description'])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 2, item)

            user_str = str(log["user"]['username']) if log.get("user") else "None"
            item = QTableWidgetItem(user_str)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 3, item)

            item = QTableWidgetItem(log['status'])
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 4, item)

            time_str = log["timestamp"].strftime("%H:%M")
            item = QTableWidgetItem(time_str)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.ui.tableWidget.setItem(row, 5, item)

            row = row + 1

    def handleBtnExport(self):
        str = self.ui.dateEdit.date().toPython().strftime("%Y-%m-%d")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Excel File",
            str,
            "Excel Files (*.xlsx);"
        )

        wb = Workbook()
        ws = wb.active
        ws.title = "Alarm Time"
        ws["A1"] = "Title"
        ws["B1"] = "Description"
        ws["C1"] = "User"
        ws["D1"] = "Status"
        ws["E1"] = "Processed"
        row = self.ui.tableWidget.rowCount()
        for i in range(row):
            ws.append((
                self.ui.tableWidget.item(i, 0).text(),
                self.ui.tableWidget.item(i, 1).text(),
                self.ui.tableWidget.item(i, 2).text(),
                self.ui.tableWidget.item(i, 3).text(),
                self.ui.tableWidget.item(i, 4).text(),
                self.ui.tableWidget.item(i, 5).text(),
            ))
        wb.save(file_path)

    def handleDateEdit(self, date):
        self.loadLogs()
