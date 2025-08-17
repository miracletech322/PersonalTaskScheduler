from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_accountabilityreports import Ui_AccountabilityReports

class AccountabilityReports(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_AccountabilityReports()
        self.ui.setupUi(self)
        self.parent = parent

        self.initCSS()
    
    def initCSS(self):
        file = QFile(":/Resources/accountabilityreports.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
