from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QFile, QTextStream, QDate

from ui_accountabilityreports import Ui_AccountabilityReports

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
    
    def initCSS(self):
        file = QFile(":/Resources/accountabilityreports.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()

    def handleBtnExport(self):
        return

    def handleDateEdit(self):
        return
