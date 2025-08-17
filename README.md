# PersonalTaskScheduler

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyside6-rcc resources/resources.qrc -o resources_rc.py
pyside6-uic mainwindow.ui -o ui_mainwindow.py
pyside6-uic usermanagement.ui -o ui_usermanagement.py
pyside6-uic userlist.ui -o ui_userlist.py
py main.py

pyside6-designer mainwindow.ui
pyside6-designer usermanagement.ui

pyinstaller --onefile --windowed main.py