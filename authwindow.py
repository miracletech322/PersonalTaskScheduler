from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_authwindow import Ui_AuthWindow
from passwordreset import PasswordReset
import global_vars

class AuthWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_AuthWindow()
        self.ui.setupUi(self)
        self.parent = parent

        self.initCSS()
        self.ui.btnEnter.clicked.connect(self.handleBtnEnter)
        self.ui.btnClose.clicked.connect(self.handleBtnClose)
        self.ui.btnReset.clicked.connect(self.handleBtnReset)
    
    def initCSS(self):
        file = QFile(":/Resources/authwindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def handleBtnEnter(self):
        str = self.ui.edtPassword.text()
        if str == global_vars.settings.value("password", "root"):
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Login Failed",
                "The password you entered is wrong."
            )
            self.reject()
    
    def handleBtnClose(self):
        self.reject()
    
    def handleBtnReset(self):
        dlg = PasswordReset(self)
        dlg.exec()
