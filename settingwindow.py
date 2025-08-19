from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtCore import Qt, QFile, QTextStream
from PySide6.QtGui import QPixmap

from ui_settingwindow import Ui_SettingWindow
import global_vars

class SettingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)
        self.parent = parent

        self.ui.btnClose.clicked.connect(self.handleBtnClose)
        self.ui.btnSave.clicked.connect(self.handleBtnSave)
        self.ui.btnChoose.clicked.connect(self.handleBtnChoose)

        self.initCSS()

        pixmap = QPixmap(global_vars.app_dir + "/assets/app.png")
        pixmap = pixmap.scaled(
            self.ui.labelLogo.width(),
            self.ui.labelLogo.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.ui.labelLogo.setPixmap(pixmap)
        self.ui.edtAppTitle.setText(global_vars.app_title)
        self.fileName = global_vars.app_dir + "/assets/app.png"
    
    def initCSS(self):
        file = QFile(":/Resources/settingwindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()
    
    def handleBtnClose(self):
        self.reject()
    
    def handleBtnSave(self):
        self.accept()

    def handleBtnChoose(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open PNG File",
            "",
            "PNG Images (*.png);;All Files (*)"
        )
        if file_name:
            self.fileName = file_name
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(
                self.ui.labelLogo.width(),
                self.ui.labelLogo.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.ui.labelLogo.setPixmap(pixmap)
