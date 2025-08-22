from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_passwordreset import Ui_PasswordReset
import global_vars

class PasswordReset(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_PasswordReset()
        self.ui.setupUi(self)
        self.parent = parent

        self.initCSS()
        self.ui.btnEnter.clicked.connect(self.handleBtnEnter)
        self.ui.btnClose.clicked.connect(self.handleBtnClose)
    
    def initCSS(self):
        file = QFile(":/Resources/passwordreset.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def handleBtnEnter(self):
        cur_pass = self.ui.edtCurPass.text()
        new_pass = self.ui.edtNewPass.text()
        confirm_pass = self.ui.edtConfirm.text()

        stored_pass = global_vars.settings.value("password", "root")

        if cur_pass != stored_pass:
            QMessageBox.warning(self, "Error", "Current password is wrong.")
            return

        if not new_pass:
            QMessageBox.warning(self, "Error", "New password cannot be empty.")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Error", "Confirm password does not match.")
            return

        global_vars.settings.setValue("password", new_pass)

        self.ui.edtCurPass.clear()
        self.ui.edtNewPass.clear()
        self.ui.edtConfirm.clear()
        self.accept()
    
    def handleBtnClose(self):
        self.reject()
