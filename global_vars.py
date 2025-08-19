from PySide6.QtCore import QSettings

settings = QSettings("MiracleTech", "PersonalTaskScheduler")
app_theme = settings.value("theme", "Dark Mode")
app_title = settings.value("title", "PersonalTaskScheduler")