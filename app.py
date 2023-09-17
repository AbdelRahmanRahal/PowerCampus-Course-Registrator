'''

Copyright (c) 2023, AbdelRahman Rahal
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the same directory as this file.

'''
import sys

from PySide6.QtWidgets import QApplication

from gui import MainWindow


app: QApplication = QApplication(sys.argv)

window: MainWindow = MainWindow()
window.show()

app.exec()