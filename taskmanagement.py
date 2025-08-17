from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_taskmanagement import Ui_TaskManagement

class TaskManagement(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_TaskManagement()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.btnPlus.clicked.connect(self.handleBtnPlus)
        self.ui.btnMinus.clicked.connect(self.handleBtnMinus)

        self.initCSS()
    
    def initCSS(self):
        file = QFile(":/Resources/taskmanagement.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()

    def handleBtnPlus(self):
        return
    
    def handleBtnMinus(self):
        return
