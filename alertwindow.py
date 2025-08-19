from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt, QFile, QTextStream, QTimer, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

from ui_alertwindow import Ui_AlertWindow
from datetime import datetime
import global_vars

class AlertWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_AlertWindow()
        self.ui.setupUi(self)
        self.parent = parent
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)


        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.taskId = ""

        self.ui.btnConfirm.clicked.connect(self.handleBtnConfirm)
        self.ui.btnYes.clicked.connect(self.handleBtnYes)
        self.ui.btnNo.clicked.connect(self.handleBtnNo)

        self.initCSS()
        self.initLCD()
    
    def initCSS(self):
        file = QFile(":/Resources/alertwindow.qss")
        if file.open(QFile.ReadOnly | QFile.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            self.setStyleSheet(stylesheet)
            file.close()

    def initLCD(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.slt_updateDateTime)
        self.timer.start(1000)
        self.slt_updateDateTime()

    def slt_updateDateTime(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ui.lcdDateTime.display(current_time)

    def setContentData(self, data):
        self.taskId = data['taskId']
        QTimer.singleShot(15 * 60 * 1000, self.close)
        self.ui.labelTitle.setText(data['title'])
        self.ui.labelDescription.setText(data['description'])
        self.handlePlaySound()
    
    def handlePlaySound(self):
        url = QUrl.fromLocalFile(global_vars.app_dir + "/assets/alarm.mp3")
        self.player.setSource(url)
        self.player.setLoops(QMediaPlayer.Loops.Infinite)

        self.player.play()

    def handleStopSound(self):
        self.player.stop()

    def handleBtnConfirm(self):
        self.parent.funcConfirmAlert(self.taskId)
        self.close()
    
    def handleBtnYes(self):
        self.parent.funcYesAlert(self.taskId)
        self.close()

    def handleBtnNo(self):
        self.parent.funcNoAlert(self.taskId)
        self.close()

    def closeEvent(self, event):
        self.handleStopSound()
        event.accept()
