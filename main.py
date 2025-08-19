import sys, os
from qasync import QEventLoop
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory
from PySide6.QtGui import QIcon
import asyncio
from mainwindow import MainWindow
import global_vars

if __name__ == "__main__":
    app = QApplication(sys.argv)
    key = "PersonalTaskScheduler"
    shared = QSharedMemory(key)
    if not shared.create(1):
        sys.exit(-1)

    app.setWindowIcon(QIcon(global_vars.app_dir + "/assets/app.png"))

    # app.setQuitOnLastWindowClosed(False)

    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    w = MainWindow()
    w.show()

    with loop:
        loop.run_forever()