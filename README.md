# PersonalTaskScheduler

```bash
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pyside6-rcc resources/resources.qrc -o resources_rc.py
pyside6-uic mainwindow.ui -o ui_mainwindow.py
pyside6-uic usermanagement.ui -o ui_usermanagement.py
pyside6-uic userlist.ui -o ui_userlist.py
pyside6-uic taskmanagement.ui -o ui_taskmanagement.py
pyside6-uic accountabilityreports.ui -o ui_accountabilityreports.py
pyside6-uic taskdialog.ui -o ui_taskdialog.py
pyside6-uic alertwindow.ui -o ui_alertwindow.py
pyside6-uic settingwindow.ui -o ui_settingwindow.py
pyside6-uic authwindow.ui -o ui_authwindow.py
pyside6-uic passwordreset.ui -o ui_passwordreset.py
py main.py

pyside6-designer mainwindow.ui
pyside6-designer usermanagement.ui
pyside6-designer userlist.ui
pyside6-designer taskmanagement.ui
pyside6-designer accountabilityreports.ui
pyside6-designer taskdialog.ui
pyside6-designer alertwindow.ui
pyside6-designer settingwindow.ui
pyside6-designer authwindow.ui
pyside6-designer passwordreset.ui
pyinstaller --windowed main.py