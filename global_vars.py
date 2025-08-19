from PySide6.QtCore import QSettings, QCoreApplication
import os

settings = QSettings("MiracleTech", "PersonalTaskScheduler")
app_dir = os.path.dirname(os.path.abspath(__file__))
app_theme = settings.value("theme", "Dark Mode")
app_title = settings.value("title", "PersonalTaskScheduler")