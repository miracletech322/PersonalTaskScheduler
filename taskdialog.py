from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QFile, QTextStream, QTime

from ui_taskdialog import Ui_TaskDialog

class TaskDialog(QDialog):
    def __init__(self, parent=None, time = "", title = "", description = "", manual = "", taskId = ""):
        super().__init__()
        self.ui = Ui_TaskDialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.btnAccept.clicked.connect(self.handleBtnAccept)
        self.ui.btnReject.clicked.connect(self.handleBtnReject)

        self.title = ""
        self.description = ""
        self.time = ""
        self.manual = "No"
        self.taskId = ""

        if taskId != "":
            self.title = title
            self.description = description
            self.time = time
            self.manual = manual
            self.taskId = taskId
            self.ui.edtDescription.setText(description)
            self.ui.edtTitle.setText(title)
            if manual == "Yes":
                self.ui.chkManual.setChecked(True)
            self.ui.timeEdit.setTime(QTime.fromString(time, "hh:mm"))

        self.initCSS()
    
    def initCSS(self):
        file = QFile(":/Resources/taskdialog.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def handleBtnAccept(self):
        self.title = self.ui.edtTitle.text()
        self.description = self.ui.edtDescription.text()
        self.time = self.ui.timeEdit.time()

        if not self.title:
            QMessageBox.warning(self, "Missing Title", "Please enter a title.")
            return

        if not self.description:
            QMessageBox.warning(self, "Missing Description", "Please enter a description.")
            return

        if self.ui.chkManual.isChecked():
            self.manual = "Yes"
        else:
            self.manual = "No"
        
        self.accept()

    def handleBtnReject(self):
        self.reject()