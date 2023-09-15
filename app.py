import sys

from PySide6.QtWidgets import QApplication

from gui import MainWindow


app: QApplication = QApplication(sys.argv)

window: MainWindow = MainWindow()
window.show()

app.exec()