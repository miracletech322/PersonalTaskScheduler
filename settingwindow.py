from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QFile, QTextStream

from ui_settingwindow import Ui_SettingWindow

class SettingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_SettingWindow()
        self.ui.setupUi(self)
        self.parent = parent

        self.initCSS()
    
    def initCSS(self):
        file = QFile(":/Resources/settingwindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()